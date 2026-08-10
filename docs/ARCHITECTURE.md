# System Architecture Document — Neera Realm AI

## High-Level Architecture Diagram

```
                 ┌───────────────────────────────────────┐
                 │          Telegram Bot API             │
                 └──────────────────┬────────────────────┘
                                    │
                                    ▼
                 ┌───────────────────────────────────────┐
                 │       Node.js Express Gateway         │
                 │   (grammY, Prisma, PDF Parse, OAuth)  │
                 └──────────┬─────────────────┬──────────┘
                            │                 │
                            ▼                 ▼
          ┌───────────────────┐     ┌─────────────────────┐
          │  Neon PostgreSQL  │     │ Python FastAPI Engine│
          │   (Prisma ORM)    │     │  (LangGraph, Gemini)│
          └───────────────────┘     └──────────┬──────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ LangGraph Supervisor   │
                                  │   State Machine        │
                                  └────────────┬───────────┘
                                               │
               ┌────────────────┬──────────────┼──────────────┬────────────────┐
               ▼                ▼              ▼              ▼                ▼
         [Job Agent]     [Resume Agent] [Financial Agt] [Calendar Agt]  [Clarification]
               │                │              │              │                │
               ▼                ▼              ▼              ▼                │
       (ATS / Remotive /  (Gemini Parse) (Market Data) (Google Cal)            │
        Arbeitnow APIs)                                                        │
               │                │              │              │                │
               └────────────────┴──────┬───────┴──────────────┘                │
                                       ▼                                       │
                              ┌────────────────┐                               │
                              │ Supervise Node │ <─────────────────────────────┘
                              └───────┬────────┘
                                      ▼
                              ┌────────────────┐
                              │ Synthesis Node │
                              └───────┬────────┘
                                      ▼
                             Telegram HTML Output
```

## Microservice Decoupling
1. **Node.js Gateway (`src/`)**:
   - Manages Telegram Bot polling/webhooks via grammY.
   - Handles user database persistence using Prisma & Neon PostgreSQL.
   - Downloads PDF resumes and extracts raw text via `pdf-parse`.
   - Sends structured HTTP JSON requests to the Python microservice.

2. **Python FastAPI AI Microservice (`ai_service/`)**:
   - Houses the LangGraph Supervisor state machine (`StateGraph`).
   - Executes specialized agents (`job_agent.py`, `resume_agent.py`, `financial.py`, `calendar_agent.py`).
   - Connects directly to external ATS APIs (Greenhouse, Lever, Ashby) and global startup boards (Remotive, Arbeitnow).
   - Generates anti-hallucinated Telegram HTML output.

## LangGraph State Machine Architecture
- **Typed State**: `OrchestratorState` contains `request`, `intent`, `agent_results`, `errors`, `supervision_passed`, `supervision_notes`, `clarification_question`, `final_response`.
- **State Reducers**: `agent_results` and `errors` use `Annotated[list[dict], operator.add]` so nodes in sequential chains append output without overwriting previous node data.
- **Human-In-The-Loop (HITL) Clarification**: `supervise_node` audits search parameters. If `location_preference` is missing during a job search, it sets `clarification_question` and `synthesize_node` returns `intent_detected = "clarification"`.
