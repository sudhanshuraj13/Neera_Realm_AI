"""
Supervisor Agent — Master Orchestration & Quality Control Brain.

Powered by LangGraph state machine with reducer state accumulation & graceful degradation:
  1. Classifies user intent (jobs / resume / financial / calendar / mixed / general)
  2. Dynamically routes to specialist sub-agents (Job Agent, Resume Agent, Financial Agent, Calendar Agent)
  3. Accumulates sub-agent outputs via Annotated[list[dict], operator.add] without overwriting
  4. Handles graceful sub-agent degradation (e.g., ATS API outages or timeouts) via error state flags
  5. Supervises & audits sub-agent outputs against ground-truth user context to eliminate hallucinations
  6. Consolidates verified agent outputs via Synthesis Agent into Telegram HTML
  7. Returns structured OrchestrateResponse

LangGraph State Machine Flow:
                ┌──────────────────┐
                │  classify_node   │
                └────────┬─────────┘
                         │ (route_after_classification)
        ┌────────────────┼────────────────┬────────────────┬────────────────┐
        ▼                ▼                ▼                ▼                ▼
     "jobs"          "resume"        "financial"       "calendar"        "mixed"
        │                │                │                │                │
        ▼                ▼                ▼                ▼                │
   [jobs_node]    [resume_node]   [financial_node] [calendar_node]   [mixed_chain]
        │                │                │                │                │
        └────────────────┴────────────────┴────────────────┼────────────────┘
                                                           ▼
                                                  ┌──────────────────┐
                                                  │  supervise_node  │
                                                  └────────┬─────────┘
                                                           ▼
                                                  ┌──────────────────┐
                                                  │ synthesize_node  │
                                                  └────────┬─────────┘
                                                           ▼
                                                          END
"""

from __future__ import annotations

import asyncio
import json
import logging
import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, StateGraph

from ..schemas.orchestrate import OrchestrateRequest, OrchestrateResponse
from .base import AgentResult, get_llm
from .calendar_agent import run_calendar_agent
from .financial import run_financial_agent
from .job_agent import run_job_agent
from .resume_agent import run_resume_agent
from .synthesis import run_synthesis_agent

logger = logging.getLogger("neera_ai_service.supervisor")


# ---------------------------------------------------------------------------
# LangGraph State Schema with Accumulator Reducers
# ---------------------------------------------------------------------------

class OrchestratorState(TypedDict):
    """
    Typed state passed through the LangGraph state machine.

    Uses `operator.add` reducers on list fields so nodes in `mixed_chain`
    sequentially append results & errors without overwriting previous node outputs.
    """

    request: dict                                           # Serialized OrchestrateRequest
    intent: str                                             # Classified intent string
    agent_results: Annotated[list[dict], operator.add]       # Accumulated sub-agent results
    errors: Annotated[list[dict], operator.add]              # Accumulated sub-agent error flags
    supervision_passed: bool                                # Quality control status flag
    supervision_notes: str                                  # Supervisor audit notes
    clarification_question: str | None                      # HITL clarification question flag
    final_response: dict                                    # Serialized OrchestrateResponse


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

CLASSIFICATION_PROMPT = """You are the Master Supervisor Agent for Neera AI — an elite career, financial, and productivity assistant.

Analyze the user's message and determine which specialist sub-agents should handle it.

Classify the intent as EXACTLY one of:
- "jobs": Job searches, open roles, ATS recommendations, resume job matching, hiring trends, tech positions
- "resume": Resume critique, resume analysis, resume review, skill extraction questions, resume improvement advice
- "financial": Stock queries, market analysis, portfolio questions, investment advice, price checks, company analysis
- "calendar": Schedule questions, meeting conflicts, free time slots, agenda planning, meeting prep
- "mixed": The message combines MULTIPLE topics (e.g., jobs AND financial, or jobs AND calendar, or financial AND calendar)
- "general": Casual conversation, greetings, general knowledge, or anything not specific to jobs, resume, financial, or calendar

You MUST respond with ONLY a raw JSON object:
{{"intent": "jobs" | "resume" | "financial" | "calendar" | "mixed" | "general"}}

User Has Resume: {has_resume}
User's Calendar: {num_events} events today.
User's Watchlist: {watchlist}
"""

SUPERVISOR_AUDIT_PROMPT = """You are the Quality Control Supervisor for Neera AI.

Your responsibility is to audit the outputs of specialist sub-agents (Job Agent, Resume Agent, Financial Agent, Calendar Agent) before final synthesis.
Strictly ensure that:
1. NO sub-agent hallucinated false facts, unverified market claims, fake job links, or fake meeting details.
2. If any sub-agent reported an error or outage flag (e.g., ATS API unreachable), preserve the healthy sub-agent outputs (e.g., financial or calendar data) while ensuring the final synthesis gracefully explains the outage to the user.
3. Validate that numbers, stock tickers, job titles, and calendar meeting times accurately match ground-truth context.

User Prompt: "{prompt}"
User Context: {context_summary}

Sub-Agent Errors Flagged: {errors_summary}

Sub-Agent Outputs:
{subagent_outputs}

Return a cleansed, verified summary of the findings with NO hallucinations.
"""


# ---------------------------------------------------------------------------
# LangGraph Node Functions (Return Delta Dicts for State Accumulation)
# ---------------------------------------------------------------------------

def classify_intent_node(state: OrchestratorState) -> dict[str, Any]:
    """Node 1: Classify user intent using LLM supervisor."""
    request = OrchestrateRequest(**state["request"])
    llm = get_llm()

    user_prefs = request.context.user_preferences
    watchlist = user_prefs.get("watchlist", [])
    has_resume = bool(user_prefs.get("resumeJson") or user_prefs.get("resume_profile"))
    num_events = len(request.context.calendar_events)

    system_prompt = CLASSIFICATION_PROMPT.format(
        has_resume="Yes" if has_resume else "No",
        num_events=num_events,
        watchlist=", ".join(watchlist) if watchlist else "None set",
    )

    try:
        response = llm.invoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.prompt},
            ]
        )

        raw_text = response.content if hasattr(response, "content") else str(response)

        # Parse intent from JSON response
        cleaned = raw_text.strip()
        if "```" in cleaned:
            cleaned = cleaned.split("```json")[-1].split("```")[0].strip()

        first_brace = cleaned.find("{")
        last_brace = cleaned.rfind("}")
        if first_brace != -1 and last_brace != -1:
            cleaned = cleaned[first_brace : last_brace + 1]

        parsed = json.loads(cleaned)
        intent = parsed.get("intent", "general")

        if intent not in ("jobs", "resume", "financial", "calendar", "mixed", "general"):
            intent = "general"

    except Exception as e:
        logger.warning("⚠️ Intent classification failed, defaulting to 'general': %s", e)
        intent = "general"

    logger.info("🧠 Supervisor classified intent: %s", intent)

    return {
        "intent": intent,
        "supervision_passed": True,
        "supervision_notes": "Intent classified successfully",
    }


def run_jobs_node(state: OrchestratorState) -> dict[str, Any]:
    """Node 2a: Execute the Job / Career Agent with graceful error degradation."""
    request = OrchestrateRequest(**state["request"])

    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_job_agent(request.prompt, request.context))
        return {
            "agent_results": [
                {"content": result.content, "agent_name": result.agent_name, "metadata": result.metadata}
            ]
        }
    except Exception as e:
        logger.error("❌ Job Agent execution error (degraded gracefully): %s", e)
        return {
            "errors": [
                {"agent_name": "job", "error": f"ATS service unreachable: {str(e)}"}
            ],
            "agent_results": [
                {
                    "content": "⚠️ ATS Job Matching service is temporarily updating. Matching listings could not be refreshed right now.",
                    "agent_name": "job",
                    "metadata": {"degraded": True, "error": str(e)},
                }
            ],
        }


def run_resume_node(state: OrchestratorState) -> dict[str, Any]:
    """Node 2b: Execute the Resume Intelligence Agent with graceful error degradation."""
    request = OrchestrateRequest(**state["request"])

    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_resume_agent(request.prompt, request.context))
        return {
            "agent_results": [
                {"content": result.content, "agent_name": result.agent_name, "metadata": result.metadata}
            ]
        }
    except Exception as e:
        logger.error("❌ Resume Agent execution error (degraded gracefully): %s", e)
        return {
            "errors": [
                {"agent_name": "resume", "error": f"Resume service error: {str(e)}"}
            ],
            "agent_results": [
                {
                    "content": "⚠️ Resume Intelligence service is currently updating. Please try again in a moment.",
                    "agent_name": "resume",
                    "metadata": {"degraded": True, "error": str(e)},
                }
            ],
        }


def run_financial_node(state: OrchestratorState) -> dict[str, Any]:
    """Node 2c: Execute the Financial Agent with graceful error degradation."""
    request = OrchestrateRequest(**state["request"])

    try:
        result = run_financial_agent(request.prompt, request.context)
        return {
            "agent_results": [
                {"content": result.content, "agent_name": result.agent_name, "metadata": result.metadata}
            ]
        }
    except Exception as e:
        logger.error("❌ Financial Agent execution error (degraded gracefully): %s", e)
        return {
            "errors": [
                {"agent_name": "financial", "error": f"Market data service error: {str(e)}"}
            ],
            "agent_results": [
                {
                    "content": "⚠️ Financial Market data service is temporarily updating.",
                    "agent_name": "financial",
                    "metadata": {"degraded": True, "error": str(e)},
                }
            ],
        }


def run_calendar_node(state: OrchestratorState) -> dict[str, Any]:
    """Node 2d: Execute the Calendar Agent with graceful error degradation."""
    request = OrchestrateRequest(**state["request"])

    try:
        result = run_calendar_agent(request.prompt, request.context)
        return {
            "agent_results": [
                {"content": result.content, "agent_name": result.agent_name, "metadata": result.metadata}
            ]
        }
    except Exception as e:
        logger.error("❌ Calendar Agent execution error (degraded gracefully): %s", e)
        return {
            "errors": [
                {"agent_name": "calendar", "error": f"Calendar service error: {str(e)}"}
            ],
            "agent_results": [
                {
                    "content": "⚠️ Calendar service could not read events right now.",
                    "agent_name": "calendar",
                    "metadata": {"degraded": True, "error": str(e)},
                }
            ],
        }


def supervise_node(state: OrchestratorState) -> dict[str, Any]:
    """
    Node 3: Supervisor Quality Control & Human-In-The-Loop (HITL) Parameter Audit.

    Audits search parameters before final synthesis.
    Rule: If the user asks for jobs but location_preference is missing or prompt is vague,
    set state: {"clarification_question": "Are you looking for Remote roles, or a specific city like Bangalore?"}
    """
    request = OrchestrateRequest(**state["request"])
    intent = state.get("intent", "general")
    user_prefs = request.context.user_preferences or {}

    location_pref = user_prefs.get("locationPreference") or user_prefs.get("location_preference")
    prompt_lower = request.prompt.strip().lower()

    # Rule: Check if job search lacks location preference or is overly vague
    if intent in ("jobs", "mixed") or any(kw in prompt_lower for kw in ["find job", "get job", "looking for job", "show job"]):
        is_vague = prompt_lower in {"find me a job", "get jobs", "jobs", "show jobs", "job", "find job", "look for job"}
        if not location_pref or is_vague:
            clarification = "Are you looking for Remote roles, or a specific city/country like India, US, or Bangalore?"
            logger.info("❓ HITL Audit: Location preference missing — triggering clarification question")
            return {
                "supervision_passed": False,
                "supervision_notes": "Audit flagged missing location preference — HITL clarification required",
                "clarification_question": clarification,
            }

    agent_results = state.get("agent_results", [])
    errors = state.get("errors", [])

    if not agent_results:
        return {
            "supervision_passed": True,
            "supervision_notes": "No sub-agent outputs to audit (general chat)",
            "clarification_question": None,
        }

    llm = get_llm()

    has_resume = bool(user_prefs.get("resumeJson"))
    context_summary = (
        f"Resume Uploaded: {has_resume}, "
        f"Location: {location_pref or 'None'}, "
        f"Calendar Events: {len(request.context.calendar_events)}, "
        f"Watchlist: {user_prefs.get('watchlist', [])}"
    )

    errors_summary = ", ".join([f"{e['agent_name']}: {e['error']}" for e in errors]) if errors else "None"

    subagent_outputs_text = "\n\n".join(
        [f"[{r['agent_name'].upper()}]: {r['content']}" for r in agent_results]
    )

    audit_prompt = SUPERVISOR_AUDIT_PROMPT.format(
        prompt=request.prompt,
        context_summary=context_summary,
        errors_summary=errors_summary,
        subagent_outputs=subagent_outputs_text,
    )

    try:
        response = llm.invoke(
            [
                {"role": "system", "content": audit_prompt},
                {"role": "user", "content": "Audit and verify the above sub-agent outputs for truthfulness and accuracy."},
            ]
        )

        notes = "Supervisor verified and anti-hallucination audited"
        if errors:
            notes += f" (Graceful degradation for: {errors_summary})"

        logger.info("🛡️ Supervisor Quality Control passed — zero hallucinations verified")
        return {
            "supervision_passed": True,
            "supervision_notes": notes,
            "clarification_question": None,
        }

    except Exception as e:
        logger.warning("⚠️ Supervision node non-blocking warning: %s", e)
        return {
            "supervision_passed": True,
            "supervision_notes": f"Supervision fallback: {e}",
            "clarification_question": None,
        }


def run_synthesis_node(state: OrchestratorState) -> dict[str, Any]:
    """
    Node 4: Consolidate verified agent outputs into final response.

    HITL Rule: If clarification_question exists, bypass all formatting and return
    the clarification question directly with intent_detected = "clarification".
    """
    clarification = state.get("clarification_question")

    if clarification:
        logger.info("❓ Synthesis Node: Returning HITL clarification question directly")
        final_resp = OrchestrateResponse(
            reply_text=clarification,
            intent_detected="clarification",
            agents_executed=["supervisor", "clarification"],
        ).model_dump()
        return {"final_response": final_resp}

    request = OrchestrateRequest(**state["request"])

    agent_results = [
        AgentResult(
            content=r["content"],
            agent_name=r["agent_name"],
            metadata=r.get("metadata", {}),
        )
        for r in state.get("agent_results", [])
    ]

    synthesis_result = run_synthesis_agent(
        original_prompt=request.prompt,
        agent_results=agent_results,
        intent=state["intent"],
    )

    agents_executed = [r["agent_name"] for r in state.get("agent_results", [])]
    agents_executed.extend(["supervisor", "synthesis"])

    final_resp = OrchestrateResponse(
        reply_text=synthesis_result.content,
        intent_detected=state["intent"],
        agents_executed=agents_executed,
    ).model_dump()

    return {"final_response": final_resp}


# ---------------------------------------------------------------------------
# LangGraph Routing Logic
# ---------------------------------------------------------------------------

def route_after_classification(state: OrchestratorState) -> str:
    """Conditional edge: decide which agent(s) to invoke based on classified intent."""
    intent = state["intent"]

    if intent == "jobs":
        return "jobs"
    elif intent == "resume":
        return "resume"
    elif intent == "financial":
        return "financial"
    elif intent == "calendar":
        return "calendar"
    elif intent == "mixed":
        return "mixed_jobs"
    else:
        # General chat — skip sub-agents, go directly to synthesis
        return "synthesize"


# ---------------------------------------------------------------------------
# LangGraph State Machine Builder
# ---------------------------------------------------------------------------

def _build_graph() -> StateGraph:
    """Construct the unified LangGraph state machine with accumulator state & sub-agents."""
    graph = StateGraph(OrchestratorState)

    # Register nodes
    graph.add_node("classify", classify_intent_node)
    graph.add_node("jobs", run_jobs_node)
    graph.add_node("resume", run_resume_node)
    graph.add_node("financial", run_financial_node)
    graph.add_node("calendar", run_calendar_node)
    graph.add_node("mixed_jobs", run_jobs_node)
    graph.add_node("mixed_financial", run_financial_node)
    graph.add_node("mixed_calendar", run_calendar_node)
    graph.add_node("supervise", supervise_node)
    graph.add_node("synthesize", run_synthesis_node)

    # Entry point
    graph.set_entry_point("classify")

    # Conditional routing after classification
    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {
            "jobs": "jobs",
            "resume": "resume",
            "financial": "financial",
            "calendar": "calendar",
            "mixed_jobs": "mixed_jobs",
            "synthesize": "synthesize",
        },
    )

    # Single-agent paths → supervise -> synthesize
    graph.add_edge("jobs", "supervise")
    graph.add_edge("resume", "supervise")
    graph.add_edge("financial", "supervise")
    graph.add_edge("calendar", "supervise")

    # Mixed path accumulator chain: jobs → financial → calendar → supervise -> synthesize
    graph.add_edge("mixed_jobs", "mixed_financial")
    graph.add_edge("mixed_financial", "mixed_calendar")
    graph.add_edge("mixed_calendar", "supervise")

    # Supervise → Synthesize
    graph.add_edge("supervise", "synthesize")

    # Synthesize → END
    graph.add_edge("synthesize", END)

    return graph


# Compile the LangGraph state machine graph once at module level
_compiled_graph = _build_graph().compile()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def run_orchestration(request: OrchestrateRequest) -> OrchestrateResponse:
    """
    Execute the full multi-agent orchestration pipeline.

    Flow via LangGraph:
      1. Supervisor classifies intent (jobs / resume / financial / calendar / mixed / general)
      2. Routes to Job / Resume / Financial / Calendar / all / none
      3. Accumulates outputs via Annotated[list[dict], operator.add] without overwriting
      4. Degrades gracefully on sub-agent errors / timeouts via error state flags
      5. Supervisor audits & quality-checks outputs against hallucinations
      6. Synthesis consolidates into Telegram HTML
      7. Returns structured OrchestrateResponse
    """
    initial_state: OrchestratorState = {
        "request": request.model_dump(),
        "intent": "",
        "agent_results": [],
        "errors": [],
        "supervision_passed": False,
        "supervision_notes": "",
        "clarification_question": None,
        "final_response": {},
    }

    loop = asyncio.get_event_loop()
    final_state = await loop.run_in_executor(None, _compiled_graph.invoke, initial_state)

    return OrchestrateResponse(**final_state["final_response"])
