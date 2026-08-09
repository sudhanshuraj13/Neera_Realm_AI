"""
Resume parsing agent using LangChain structured output.

Uses the shared LLM chain (get_llm) with Pydantic-based structured output
to extract a high-fidelity career profile from raw resume text.
"""

from __future__ import annotations

import logging

from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.base import get_llm
from app.schemas.resume import ResumeProfile

logger = logging.getLogger("neera_ai_service.resume_agent")

SYSTEM_PROMPT = """\
You are an expert resume parser for a career intelligence platform.

Given the raw text of a resume, extract a structured career profile.
Be thorough and precise:

- **primary_role**: Identify the candidate's primary professional role (e.g. "Senior Backend Engineer", "Product Manager", or "Software Engineer (Fresher)").
- **years_experience**: Calculate total years of professional experience from the dates provided. If unclear, estimate conservatively (0 for freshers).
- **skills**: Extract ALL technical skills, programming languages, frameworks, tools, and soft skills mentioned.
- **target_roles**: Infer 2–4 roles the candidate is targeting or well-qualified for based on their experience, projects, and skills. For freshers/entry-level candidates, focus on junior, entry-level, or associate roles.
- **preferred_domains**: Infer 1–3 industry domains the candidate has worked in or is drawn to (e.g. "FinTech", "HealthTech", "AI/ML", "E-commerce").
- **experience**: Extract each work experience entry with title, company, duration (e.g. "Jan 2022 – Present"), and key highlights/accomplishments. If the candidate is a fresher with NO prior work experience or internships, add a default entry: `title`: "Fresher", `company`: "N/A", `duration`: "N/A", `highlights`: ["Fresh graduate / Entry-level candidate seeking new opportunities."].
- **projects**: Extract notable projects with name, description, and technologies used.

If a field cannot be determined from the resume text, use sensible defaults:
- Empty lists for list fields
- "Unknown" for string fields
- 0 for years_experience

Do NOT hallucinate information that is not present in the resume.
"""


async def parse_resume(raw_text: str) -> ResumeProfile:
    """
    Parse raw resume text into a structured ResumeProfile using LLM extraction.

    Args:
        raw_text: The raw text content extracted from a PDF resume.

    Returns:
        A validated ResumeProfile with structured career data.
    """
    logger.info("📄 Parsing resume (%d chars)", len(raw_text))

    llm = get_llm()

    # Use structured output for type-safe Pydantic extraction
    structured_llm = llm.with_structured_output(ResumeProfile)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Parse the following resume:\n\n{raw_text}"),
    ]

    result: ResumeProfile = await structured_llm.ainvoke(messages)

    # Post-processing: If candidate has no experience entries (Fresher fallback)
    if not result.experience:
        from app.schemas.resume import Experience
        result.experience.append(
            Experience(
                title="Fresher",
                company="N/A",
                duration="N/A",
                highlights=["Fresh graduate / Entry-level candidate seeking new opportunities."],
            )
        )
        if not result.primary_role or result.primary_role.lower() == "unknown":
            result.primary_role = "Junior Developer / Fresher"

    logger.info(
        "✅ Resume parsed — role=%s, skills=%d, experience=%d, projects=%d",
        result.primary_role,
        len(result.skills),
        len(result.experience),
        len(result.projects),
    )

    return result


async def run_resume_agent(prompt: str, context: Any) -> Any:
    """
    Sub-Agent interface function for Resume Intelligence & Critique Agent.

    Args:
        prompt: Raw user message text
        context: UserContext model or dictionary

    Returns:
        AgentResult with formatted Telegram HTML resume feedback/critique
    """
    from app.agents.base import AgentResult

    user_prefs = {}
    if hasattr(context, "user_preferences"):
        user_prefs = context.user_preferences
    elif isinstance(context, dict):
        user_prefs = context.get("user_preferences", {})

    resume_profile = user_prefs.get("resumeJson") or user_prefs.get("resume_profile") or {}

    if not resume_profile:
        content = (
            "<b>📄 Resume Intelligence</b>\n\n"
            "You haven't uploaded a resume yet!\n\n"
            "👉 Please upload your resume PDF using <code>/resume</code> or tap <b>📄 Upload Resume</b> so I can analyze your career profile and provide feedback!"
        )
        return AgentResult(
            content=content,
            agent_name="resume",
            metadata={"status": "no_resume"},
        )

    # Candidate has an uploaded profile — generate resume intelligence & feedback using LLM
    primary_role = resume_profile.get("primary_role", "Software Engineer")
    skills = resume_profile.get("skills", [])
    target_roles = resume_profile.get("target_roles", [])
    experience = resume_profile.get("experience", [])
    projects = resume_profile.get("projects", [])

    llm = get_llm()

    critique_prompt = f"""You are the Resume Intelligence Specialist for Neera AI.

Analyze the candidate's stored resume profile and answer their query: "{prompt}"

Candidate Profile Summary:
- Primary Role: {primary_role}
- Skills: {', '.join(skills)}
- Target Roles: {', '.join(target_roles)}
- Total Experience Entries: {len(experience)}
- Projects Extracted: {len(projects)}

Provide clear, actionable, professional career intelligence and resume advice.
Format using ONLY Telegram HTML tags (<b>, <i>, <code>). Keep it concise (4-8 lines).
"""

    response = llm.invoke([
        {"role": "system", "content": critique_prompt},
        {"role": "user", "content": prompt},
    ])

    raw_text = response.content if hasattr(response, "content") else str(response)

    return AgentResult(
        content=raw_text,
        agent_name="resume",
        metadata={"role": primary_role, "skills_count": len(skills)},
    )

