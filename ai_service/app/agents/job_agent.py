"""
Job Matching Agent.

Fetches live job listings from public ATS APIs (Greenhouse, Lever, Ashby) via ats_service,
scores and ranks them against the user's extracted ResumeProfile, and formats a clean
Telegram HTML response.
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
]


def score_job_match(
    job: JobListing,
    primary_role: str,
    target_roles: list[str],
    skills: list[str],
) -> tuple[int, str]:
    """
    Score a job listing against candidate profile (0–100%).
    Returns (score, reason).
    """
    title_lower = job.title.lower()
    role_lower = primary_role.lower()

    score = 50  # Base match score for active engineering listing
    reasons = []

    # Title matching
    all_target_roles = [role_lower] + [r.lower() for r in target_roles]

    matched_role = None
    for tr in all_target_roles:
        # Check key terms
        words = [w for w in tr.split() if len(w) > 2]
        if any(w in title_lower for w in words):
            matched_role = tr
            break

    if matched_role:
        score += 30
        reasons.append(f"Matches target role '{matched_role.title()}'")
    elif "engineer" in title_lower or "developer" in title_lower or "software" in title_lower:
        score += 15
        reasons.append("Software engineering role")

    # Skill keyword matching in title or location
    matched_skills = []
    for skill in skills:
        sk_lower = skill.lower()
        if len(sk_lower) > 2 and sk_lower in title_lower:
            matched_skills.append(skill)

    if matched_skills:
        score += min(20, len(matched_skills) * 10)
        reasons.append(f"Skills: {', '.join(matched_skills)}")

    # Check for Fresher / Entry-Level targeting
    is_fresher_candidate = (
        "fresher" in role_lower
        or "junior" in role_lower
        or "entry" in role_lower
        or any("fresher" in r for r in all_target_roles)
    )

    if is_fresher_candidate:
        if any(term in title_lower for term in ["junior", "entry", "associate", "graduate", "intern"]):
            score += 20
            reasons.append("Entry-level / Fresher friendly position")
        elif any(term in title_lower for term in ["senior", "lead", "staff", "principal"]):
            score -= 30

    final_score = max(30, min(98, score))
    reason_text = " • ".join(reasons) if reasons else "Compatible role"

    return final_score, reason_text


async def match_jobs_for_resume(
    resume_profile: dict[str, Any],
    company_slugs: list[str] | None = None,
) -> dict[str, Any]:
    """
    Fetch live ATS jobs and match them against candidate's resume profile.

    Args:
        resume_profile: Dictionary representation of ResumeProfile
        company_slugs: Optional list of ATS company slugs to query

    Returns:
        Dict with total_found, matched_count, and formatted_html
    """
    slugs = company_slugs or DEFAULT_COMPANIES

    primary_role = str(resume_profile.get("primary_role", "Software Engineer"))
    target_roles = [str(r) for r in resume_profile.get("target_roles", [])]
    skills = [str(s) for s in resume_profile.get("skills", [])]

    logger.info(
        "🔍 Job matching initiated — role='%s', target_roles=%s, companies=%s",
        primary_role,
        target_roles,
        slugs,
    )

    # 1. Fetch live jobs from ATS endpoints
    all_jobs = await fetch_all_jobs(slugs)

    if not all_jobs:
        # Fallback response if external ATS endpoints are unreachable
        html = [
            "<b>💼 Live Tech Job Board Matches</b>",
            "",
            f"<b>Profile:</b> <code>{primary_role}</code>",
            f"<b>Skills:</b> {', '.join(skills[:5]) if skills else 'Software Engineering'}",
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
            "formatted_html": "\n".join(html),
            "jobs": [],
        }

    # 2. Score and rank jobs
    scored_jobs = []
    for job in all_jobs:
        score, reason = score_job_match(job, primary_role, target_roles, skills)
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
        f"<b>🎯 Candidate Profile:</b> <code>{primary_role}</code>",
        f"<b>🛠️ Top Skills:</b> {', '.join(skills[:6]) if skills else 'General Engineering'}",
        f"<b>⚡ Live ATS Scanned:</b> {len(all_jobs)} openings across tech companies",
        "",
    ]

    for idx, item in enumerate(top_matches, start=1):
        html_lines.extend([
            f"{idx}. <b>{item['title']}</b>",
            f"   🏢 <b>Company:</b> {item['company']}",
            f"   📍 <b>Location:</b> {item['location']}",
            f"   🔥 <b>Match:</b> {item['score']}% ({item['reason']})",
            f"   👉 <a href='{item['apply_url']}'><b>Apply Now Directly</b></a>",
            "",
        ])

    html_lines.append("<i>💡 Type <code>/jobs</code> anytime to refresh your job feed.</i>")

    return {
        "total_found": len(all_jobs),
        "matched_count": len(top_matches),
        "formatted_html": "\n".join(html_lines),
        "jobs": top_matches,
    }
