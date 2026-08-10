"""
Job Matching Agent.

Fetches live job listings dynamically across global startup boards (Remotive, Arbeitnow)
and user-configured target dream companies (Greenhouse, Lever, Ashby via ats_service).

Scores and ranks job postings against candidate profile using explicit deterministic filters
(experience_level, target_roles, location_preference) passed directly from Node.js user DB model.
Eliminates brittle text-guessing logic.
"""

from __future__ import annotations

import logging
from typing import Any

from app.schemas.job_listing import JobListing
from app.services.ats_service import fetch_all_jobs

logger = logging.getLogger("neera_ai_service.job_agent")


def score_job_match(
    job: JobListing,
    primary_role: str,
    target_roles: list[str],
    skills: list[str],
    experience_level: str | None = None,
    location_preference: str | None = None,
    target_companies: list[str] | None = None,
) -> tuple[int, str]:
    """
    Score a job listing against candidate profile (0–100%) using explicit deterministic filters.

    Returns:
        (score, reason_text)
    """
    title_lower = job.title.lower()
    location_lower = job.location.lower()
    company_lower = job.company.lower()
    role_lower = primary_role.lower()

    # 1. Deterministic Experience Level Filtering
    exp_norm = (experience_level or "").strip().lower()
    is_fresher = "fresher" in exp_norm or "0-1" in exp_norm
    is_senior = "senior" in exp_norm or "3+" in exp_norm or "lead" in exp_norm

    has_senior_title = any(term in title_lower for term in ["senior", "sr", "lead", "staff", "principal", "head", "director", "vp", "manager", "architect"])
    has_entry_title = any(term in title_lower for term in ["junior", "jr", "entry", "associate", "intern", "trainee", "fresher", "apprentice"])

    if is_fresher:
        if has_senior_title:
            return 0, "Requires Senior Experience (Excluded)"
        elif has_entry_title:
            score = 75
            reason = "Entry-Level / Fresher position"
        else:
            score = 55
            reason = "General Developer role"
    elif is_senior:
        if has_senior_title:
            score = 75
            reason = "Senior level role"
        elif has_entry_title:
            return 25, "Entry level position (Below experience target)"
        else:
            score = 50
            reason = "Standard position"
    else:
        score = 55
        reason = "Matching role"

    reasons = [reason]

    # 2. Deterministic Location Matching
    if location_preference:
        loc_pref = location_preference.strip().lower()
        if loc_pref in location_lower or (loc_pref == "remote" and "remote" in location_lower):
            score += 15
            reasons.append(f"📍 Location Match ({job.location})")
        elif "remote" in location_lower:
            score += 10
            reasons.append(f"📍 Remote Position")

    # 3. Target Dream Companies Boost
    if target_companies:
        for tc in target_companies:
            tc_clean = tc.strip().lower()
            if tc_clean and tc_clean in company_lower:
                score += 20
                reasons.append(f"🎯 Dream Company ({tc.title()})")
                break

    # 4. Target Roles & Skills Matching
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
        reasons.append(f"Role: {matched_role.title()}")
    elif any(
        term in title_lower
        for term in ["software", "engineer", "developer", "backend", "frontend", "fullstack", "data", "ai", "cloud"]
    ):
        score += 10

    # 5. Skill keyword matching
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
    experience_level: str | None = None,
    target_roles: list[str] | None = None,
    location_preference: str | None = None,
) -> dict[str, Any]:
    """
    Fetch live jobs from target dream companies and global startup boards using deterministic DB preferences.

    Args:
        resume_profile: Dictionary representation of ResumeProfile
        company_slugs: Custom target company slugs specified by user
        experience_level: Explicit experience level ("Fresher", "1-3 Years", "Senior")
        target_roles: Explicit target roles (e.g., ["Backend", "AI"])
        location_preference: Explicit location preference (e.g., "Remote", "India")

    Returns:
        Dict with total_found, matched_count, experience_level, location_preference, and formatted_html
    """
    target_companies = company_slugs or resume_profile.get("target_companies", [])
    if isinstance(target_companies, str):
        target_companies = [c.strip() for c in target_companies.split(",") if c.strip()]

    primary_role = str(resume_profile.get("primary_role", "Software Engineer"))
    roles = target_roles or [str(r) for r in resume_profile.get("target_roles", [])]
    skills = [str(s) for s in resume_profile.get("skills", [])]

    exp_label = experience_level or "Not specified"
    loc_label = location_preference or "Any Location"

    logger.info(
        "🔍 Deterministic job matching — role='%s', exp_level='%s', location='%s', target_roles=%s",
        primary_role,
        exp_label,
        loc_label,
        roles,
    )

    # 1. Fetch live jobs dynamically (target companies + global startup job aggregators)
    all_jobs = await fetch_all_jobs(
        company_slugs=target_companies,
        include_global_startups=True,
        primary_role=primary_role,
        target_roles=roles,
        skills=skills,
    )

    if not all_jobs:
        html = [
            "<b>💼 Dynamic Job Board Matcher</b>",
            "",
            f"<b>🎯 Role:</b> <code>{primary_role}</code>",
            f"<b>📊 Experience:</b> <code>{exp_label}</code>",
            f"<b>📍 Location:</b> <code>{loc_label}</code>",
            f"<b>🏢 Target Companies:</b> {', '.join(target_companies) if target_companies else 'All Global Startups & Tech'}",
            "",
            "⚠️ Job search engine is currently updating. Try <code>/jobs</code> again in a moment!",
        ]
        return {
            "total_found": 0,
            "matched_count": 0,
            "experience_level": exp_label,
            "location_preference": loc_label,
            "target_companies": target_companies,
            "formatted_html": "\n".join(html),
            "jobs": [],
        }

    # 2. Score and rank jobs using deterministic filters
    scored_jobs = []
    for job in all_jobs:
        score, reason = score_job_match(
            job,
            primary_role=primary_role,
            target_roles=roles,
            skills=skills,
            experience_level=experience_level,
            location_preference=location_preference,
            target_companies=target_companies,
        )

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

    top_matches = scored_jobs[:6]

    # 3. Format Telegram HTML response
    target_comp_str = ", ".join([c.title() for c in target_companies]) if target_companies else "Open (Tell bot e.g. 'Add Google to target companies')"

    html_lines = [
        "<b>💼 Live Matched Job Openings</b>",
        "",
        f"<b>🎯 Primary Role:</b> <code>{primary_role}</code>",
        f"<b>📊 Experience Level:</b> <code>{exp_label}</code>",
        f"<b>📍 Location Preference:</b> <code>{loc_label}</code>",
        f"<b>🏢 Target Companies:</b> {target_comp_str}",
        f"<b>🛠️ Top Skills:</b> {', '.join(skills[:5]) if skills else 'Software Engineering'}",
        f"<b>⚡ Live Discovered:</b> {len(all_jobs)} open postings across global startups & tech",
        "",
    ]

    if not top_matches:
        html_lines.extend([
            "ℹ️ No active openings matched your criteria right now.",
            "👉 Tell the bot your dream companies (e.g. <i>'Add Razorpay, Stripe to my target companies'</i>) to watch for new alerts!",
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

    html_lines.append("<i>💡 Tap a button below to update your experience filter anytime!</i>")

    return {
        "total_found": len(all_jobs),
        "matched_count": len(top_matches),
        "experience_level": exp_label,
        "location_preference": loc_label,
        "target_companies": target_companies,
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
    exp_level = user_prefs.get("experienceLevel") or user_prefs.get("experience_level")
    target_roles = user_prefs.get("targetRoles") or user_prefs.get("target_roles")
    loc_pref = user_prefs.get("locationPreference") or user_prefs.get("location_preference")
    target_comps = user_prefs.get("target_companies") or resume_profile.get("target_companies")

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
        company_slugs=target_comps,
        experience_level=exp_level,
        target_roles=target_roles,
        location_preference=loc_pref,
    )
    return AgentResult(
        content=match_res.get("formatted_html", ""),
        agent_name="job",
        metadata={
            "total_found": match_res.get("total_found", 0),
            "matched_count": match_res.get("matched_count", 0),
        },
    )
