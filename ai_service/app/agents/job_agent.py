"""
Job Matching Agent.

Fetches live job listings from public ATS APIs (Greenhouse, Lever, Ashby) via ats_service,
scores and ranks them against the user's extracted ResumeProfile, and formats a clean
Telegram HTML response.

Supports strict experience-level filtering (Fresher / Junior / Senior) to ensure freshers
never receive irrelevant senior job postings.
"""

from __future__ import annotations

import logging
from typing import Any

from app.schemas.job_listing import JobListing
from app.services.ats_service import fetch_all_jobs

logger = logging.getLogger("neera_ai_service.job_agent")

DEFAULT_COMPANIES = [
    "stripe",
    "openai",
    "vercel",
    "notion",
    "figma",
    "linear",
    "github",
    "cloudflare",
    "discord",
    "postman",
    "freshworks",
    "browserstack",
    "hasura",
    "harness",
    "datadog",
]

SENIOR_TERMS = {
    "senior",
    "sr",
    "lead",
    "staff",
    "principal",
    "head",
    "director",
    "vp",
    "manager",
    "architect",
}

ENTRY_TERMS = {
    "junior",
    "jr",
    "entry",
    "associate",
    "graduate",
    "fresher",
    "intern",
    "trainee",
    "apprentice",
    "new grad",
}


def score_job_match(
    job: JobListing,
    primary_role: str,
    target_roles: list[str],
    skills: list[str],
    years_experience: int = 0,
    experience_level: str = "auto",  # "fresher" | "junior" | "senior" | "auto"
) -> tuple[int, str]:
    """
    Score a job listing against candidate profile (0–100%).
    Strictly filters out senior roles if the candidate is a fresher.

    Returns:
        (score, reason_text)
    """
    title_lower = job.title.lower()
    role_lower = primary_role.lower()

    # Determine if candidate is a fresher
    is_fresher = (
        experience_level == "fresher"
        or (
            experience_level == "auto"
            and (
                years_experience == 0
                or "fresher" in role_lower
                or "junior" in role_lower
                or "entry" in role_lower
                or any("fresher" in r.lower() for r in target_roles)
            )
        )
    )

    is_senior_target = (
        experience_level == "senior"
        or (
            experience_level == "auto"
            and (
                years_experience >= 3
                or any(s in role_lower for s in ["senior", "lead", "staff", "principal"])
            )
        )
    )

    # 1. Seniority Filtering & Exclusion
    has_senior_title = any(term in title_lower for term in SENIOR_TERMS)
    has_entry_title = any(term in title_lower for term in ENTRY_TERMS)

    if is_fresher:
        if has_senior_title:
            # Strictly exclude senior positions for freshers
            return 0, "Requires Senior Experience (Excluded)"
        elif has_entry_title:
            base_score = 75
            reason = "Entry-Level / Fresher position"
        else:
            base_score = 55
            reason = "General Developer role"
    elif is_senior_target:
        if has_senior_title:
            base_score = 75
            reason = "Senior level role"
        elif has_entry_title:
            return 25, "Entry level position (Below experience target)"
        else:
            base_score = 50
            reason = "Standard position"
    else:
        base_score = 55
        reason = "Matching role"

    score = base_score
    reasons = [reason]

    # 2. Title & Target Role Matching
    all_target_roles = [role_lower] + [r.lower() for r in target_roles]
    matched_role = None
    for tr in all_target_roles:
        words = [
            w
            for w in tr.split()
            if len(w) > 2
            and w not in {"fresher", "junior", "senior", "developer", "engineer", "software"}
        ]
        if words and any(w in title_lower for w in words):
            matched_role = tr
            break

    if matched_role:
        score += 20
        reasons.append(f"Matches target role '{matched_role.title()}'")
    elif any(
        term in title_lower
        for term in ["software", "engineer", "developer", "backend", "frontend", "fullstack", "data", "ai", "cloud"]
    ):
        score += 10

    # 3. Skill matching
    matched_skills = []
    for skill in skills:
        sk_lower = skill.lower()
        if len(sk_lower) > 2 and sk_lower in title_lower:
            matched_skills.append(skill)

    if matched_skills:
        score += min(15, len(matched_skills) * 5)
        reasons.append(f"Skills: {', '.join(matched_skills)}")

    final_score = max(10, min(98, score))
    reason_text = " • ".join(reasons)

    return final_score, reason_text


async def match_jobs_for_resume(
    resume_profile: dict[str, Any],
    company_slugs: list[str] | None = None,
    experience_level_override: str | None = None,
) -> dict[str, Any]:
    """
    Fetch live ATS jobs and match them against candidate's resume profile.

    Args:
        resume_profile: Dictionary representation of ResumeProfile
        company_slugs: Optional list of ATS company slugs to query
        experience_level_override: Optional experience filter ("fresher" | "junior" | "senior")

    Returns:
        Dict with total_found, matched_count, experience_level, and formatted_html
    """
    slugs = company_slugs or DEFAULT_COMPANIES

    primary_role = str(resume_profile.get("primary_role", "Software Engineer"))
    target_roles = [str(r) for r in resume_profile.get("target_roles", [])]
    skills = [str(s) for s in resume_profile.get("skills", [])]
    years_exp = int(resume_profile.get("years_experience", 0))

    exp_level = experience_level_override or "auto"

    is_fresher = (
        exp_level == "fresher"
        or (
            exp_level == "auto"
            and (
                years_exp == 0
                or "fresher" in primary_role.lower()
                or "junior" in primary_role.lower()
                or "entry" in primary_role.lower()
                or any("fresher" in r.lower() for r in target_roles)
            )
        )
    )

    exp_label = "🎓 Fresher / Entry-Level (0–1 yrs)" if is_fresher else (
        f"💼 Experienced ({years_exp}+ yrs)" if years_exp > 0 else "💻 Junior / Mid-Level (1–3 yrs)"
    )

    logger.info(
        "🔍 Job matching initiated — role='%s', exp_level=%s (years=%d), target_roles=%s",
        primary_role,
        exp_label,
        years_exp,
        target_roles,
    )

    # 1. Fetch live jobs from ATS endpoints
    all_jobs = await fetch_all_jobs(slugs)

    if not all_jobs:
        # Fallback response if external ATS endpoints are unreachable
        html = [
            "<b>💼 Live Tech Job Board Matches</b>",
            "",
            f"<b>🎯 Role:</b> <code>{primary_role}</code>",
            f"<b>{exp_label}</b>",
            f"<b>🛠️ Skills:</b> {', '.join(skills[:5]) if skills else 'Software Engineering'}",
            "",
            "⚠️ Live ATS sync is updating. Here are top tech career portals matching your role:",
            "• 🌐 <a href='https://openai.com/careers'>OpenAI Careers</a>",
            "• 🌐 <a href='https://stripe.com/jobs'>Stripe Careers</a>",
            "• 🌐 <a href='https://vercel.com/careers'>Vercel Careers</a>",
            "• 🌐 <a href='https://notion.so/careers'>Notion Careers</a>",
            "",
            "<i>Type <code>/jobs</code> to refresh live ATS openings anytime!</i>",
        ]
        return {
            "total_found": 0,
            "matched_count": 0,
            "experience_level": exp_label,
            "formatted_html": "\n".join(html),
            "jobs": [],
        }

    # 2. Score and rank jobs
    scored_jobs = []
    for job in all_jobs:
        score, reason = score_job_match(
            job,
            primary_role,
            target_roles,
            skills,
            years_experience=years_exp,
            experience_level=exp_level,
        )

        # Skip zero-score excluded jobs (e.g. senior jobs for freshers)
        if score <= 0:
            continue

        scored_jobs.append(
            {
                "company": job.company.capitalize(),
                "title": job.title,
                "location": job.location,
                "apply_url": job.apply_url,
                "score": score,
                "reason": reason,
            }
        )

    # Sort descending by match score
    scored_jobs.sort(key=lambda x: x["score"], reverse=True)

    # Take top 6 matched jobs
    top_matches = scored_jobs[:6]

    # 3. Format Telegram HTML message
    html_lines = [
        "<b>💼 Live Matched Job Openings</b>",
        "",
        f"<b>🎯 Role:</b> <code>{primary_role}</code>",
        f"<b>{exp_label}</b>",
        f"<b>🛠️ Top Skills:</b> {', '.join(skills[:6]) if skills else 'General Engineering'}",
        f"<b>⚡ Live ATS Scanned:</b> {len(all_jobs)} openings across tech leaders & startups",
        "",
    ]

    if not top_matches:
        html_lines.extend([
            "ℹ️ No active entry-level openings matched right now across scanned company boards.",
            "👉 Try switching experience filter using the buttons below or check back soon!",
            "",
        ])
    else:
        for idx, item in enumerate(top_matches, start=1):
            html_lines.extend([
                f"{idx}. <b>{item['title']}</b>",
                f"   🏢 <b>Company:</b> {item['company']}",
                f"   📍 <b>Location:</b> {item['location']}",
                f"   🔥 <b>Match:</b> {item['score']}% ({item['reason']})",
                f"   👉 <a href='{item['apply_url']}'><b>Apply Now Directly</b></a>",
                "",
            ])

    html_lines.append("<i>💡 Tap a button below to filter jobs by your experience level!</i>")

    return {
        "total_found": len(all_jobs),
        "matched_count": len(top_matches),
        "experience_level": exp_label,
        "is_fresher": is_fresher,
        "formatted_html": "\n".join(html_lines),
        "jobs": top_matches,
    }


async def run_job_agent(prompt: str, context: Any) -> Any:
    """
    Standard Sub-Agent function for Job / Career Agent.

    Args:
        prompt: Raw user message text
        context: UserContext model or dictionary

    Returns:
        AgentResult with formatted Telegram HTML job response
    """
    from app.agents.base import AgentResult

    user_prefs = {}
    if hasattr(context, "user_preferences"):
        user_prefs = context.user_preferences
    elif isinstance(context, dict):
        user_prefs = context.get("user_preferences", {})

    resume_profile = user_prefs.get("resumeJson") or user_prefs.get("resume_profile") or {}
    exp_override = user_prefs.get("experience_level")

    if not resume_profile:
        content = (
            "<b>💼 Tech & Career Job Matcher</b>\n\n"
            "You haven't uploaded a resume yet!\n\n"
            "To get personalized live job postings matched to your target role & skills:\n"
            "👉 Send your resume PDF using <code>/resume</code> or tap <b>📄 Upload Resume</b>!"
        )
        return AgentResult(
            content=content,
            agent_name="job",
            metadata={"status": "no_resume"},
        )

    match_res = await match_jobs_for_resume(
        resume_profile,
        experience_level_override=exp_override,
    )
    return AgentResult(
        content=match_res.get("formatted_html", ""),
        agent_name="job",
        metadata={
            "total_found": match_res.get("total_found", 0),
            "matched_count": match_res.get("matched_count", 0),
            "is_fresher": match_res.get("is_fresher", False),
        },
    )
