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
from app.schemas.jobs import UnifiedJob
from app.services.ats_service import fetch_all_jobs
from app.services.funding_service import fetch_recent_funded_startups
from app.services.job_orchestrator import fetch_all_jobs_concurrently

logger = logging.getLogger("neera_ai_service.job_agent")


def score_job_match(
    job: JobListing | UnifiedJob,
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
            return -1, "Exceeds experience requirement (Senior title)"
        score = 85 if has_entry_title else 70
        reason = "Fresher friendly role"
    elif is_senior:
        if has_entry_title:
            return -1, "Below experience target (Junior title)"
        score = 85 if has_senior_title else 70
        reason = "Senior level role"
    else:
        score = 75
        reason = "Mid-level role"

    # 2. Primary Role & Target Roles Match
    role_matched = False
    all_roles = [role_lower] + [r.lower() for r in target_roles]
    for r in all_roles:
        words = [w for w in r.split() if len(w) > 2 and w not in {"engineer", "developer", "software", "fresher", "junior", "senior"}]
        if words and any(w in title_lower for w in words):
            score += 15
            role_matched = True
            reason += f" • Role match ({r.title()})"
            break

    if not role_matched and not any(term in title_lower for term in role_lower.split() if len(term) > 2):
        score -= 10

    # 3. Target Companies Boost
    if target_companies:
        for c in target_companies:
            if c.lower() in company_lower:
                score += 20
                reason += f" • Dream Company ({c.title()})"
                break

    # 4. Location Boost
    if location_preference:
        loc_pref = location_preference.lower()
        if loc_pref in location_lower or (loc_pref == "remote" and "remote" in location_lower):
            score += 10
            reason += " • Location preference match"

    final_score = min(99, max(10, score))
    return final_score, reason


async def match_jobs_for_resume(
    resume_profile: dict[str, Any],
    company_slugs: list[str] | None = None,
    experience_level: str | None = None,
    target_roles: list[str] | None = None,
    location_preference: str | None = None,
    primary_role: str | None = None,
    exclude_startup_ids: list[str] | None = None,
) -> dict[str, Any]:
    """
    Fetch live jobs concurrently across multi-source job search adapters (ATS, JobSpy, Adzuna).
    Includes Startup Funding Radar integration for high-growth funding alerts.
    """
    target_companies = company_slugs or resume_profile.get("target_companies", [])
    if isinstance(target_companies, str):
        target_companies = [c.strip() for c in target_companies.split(",") if c.strip()]

    p_role = primary_role or str(resume_profile.get("primary_role") or "General Candidate")
    roles = target_roles or [str(r) for r in resume_profile.get("target_roles", [])]
    skills = [str(s) for s in resume_profile.get("skills", [])]

    exp_label = experience_level or "Not specified"
    loc_label = location_preference or "Any Location"

    user_context = {
        "primary_role": p_role,
        "target_roles": roles,
        "skills": skills,
        "experience_level": exp_label,
        "location_preference": loc_label,
        "target_companies": target_companies,
    }

    logger.info(
        "🔍 Multi-adapter job search — role='%s', exp_level='%s', location='%s', target_roles=%s",
        p_role,
        exp_label,
        loc_label,
        roles,
    )

    # 1. Fetch live jobs concurrently across all registered adapters
    all_jobs = await fetch_all_jobs_concurrently(user_context)

    if not all_jobs:
        html = [
            "<b>💼 Multi-Source Job Search Engine</b>",
            "",
            f"<b>🎯 Role:</b> <code>{p_role}</code>",
            f"<b>📊 Experience:</b> <code>{exp_label}</code>",
            f"<b>📍 Location:</b> <code>{loc_label}</code>",
            f"<b>🏢 Target Companies:</b> {', '.join(target_companies) if target_companies else 'All Global Companies & Job Boards'}",
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
            "sent_startup_ids": [],
        }

    # 2. Score and rank jobs using deterministic filters
    scored_jobs = []
    for job in all_jobs:
        score, reason = score_job_match(
            job,
            primary_role=p_role,
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
                "source": job.source,
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
        "<b>💼 Live Matched Job Openings (Multi-Source Engine)</b>",
        "",
        f"<b>🎯 Primary Role:</b> <code>{p_role}</code>",
        f"<b>📊 Experience Level:</b> <code>{exp_label}</code>",
        f"<b>📍 Location Preference:</b> <code>{loc_label}</code>",
        f"<b>🏢 Target Companies:</b> {target_comp_str}",
        f"<b>🛠️ Top Skills:</b> {', '.join(skills[:5]) if skills else 'Professional Skills'}",
        f"<b>⚡ Live Discovered:</b> {len(all_jobs)} open postings across ATS, LinkedIn & Job Boards",
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
            source_badge = f" [<code>{item['source']}</code>]" if item.get("source") else ""
            html_lines.extend([
                f"{idx}. <b>{item['title']}</b>{source_badge}",
                f"   🏢 <b>Company:</b> {item['company']}",
                f"   📍 <b>Location:</b> {item['location']}",
                f"   🔥 <b>Match:</b> {item['score']}% ({item['reason']})",
                f"   👉 <a href='{item['apply_url']}'><b>Apply Now Directly</b></a>",
                "",
            ])

    # 4. Startup Funding Radar Section (Deduplicated)
    exclude_ids = set(exclude_startup_ids or [])
    funding_items = await fetch_recent_funded_startups(hours=48)
    unseen_funding = [item for item in funding_items if item.id not in exclude_ids and item.source_url not in exclude_ids]

    sent_startup_ids: list[str] = []
    if unseen_funding:
        candidate_terms = [p_role.lower()] + [r.lower() for r in roles] + [s.lower() for s in skills[:6]]
        matched_funding = []
        for item in unseen_funding:
            item_text = f"{item.company_name} {item.domain} {item.summary}".lower()
            if any(term in item_text for term in candidate_terms if len(term) > 2):
                matched_funding.append(item)

        top_funding = matched_funding[:2] if matched_funding else unseen_funding[:2]
        sent_startup_ids = [f.id for f in top_funding]

        if top_funding:
            html_lines.append("<b>💰 High-Growth Funding Radar Alert</b>")
            html_lines.append("<i>Recent startup funding events matching your domain:</i>")
            html_lines.append("")
            for f_item in top_funding:
                html_lines.extend([
                    f"🚀 <b>{f_item.company_name}</b> ({f_item.funding_stage} — <b>{f_item.amount_raised}</b>)",
                    f"   • <b>Domain:</b> {f_item.domain}",
                    f"   • <b>Radar:</b> {f_item.summary}",
                    f"   • 🌐 <a href='{f_item.source_url}'><b>Founder News & Careers</b></a>",
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
        "sent_startup_ids": sent_startup_ids,
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
            "<b>💼 Jobs & Careers Matcher</b>\n\n"
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
