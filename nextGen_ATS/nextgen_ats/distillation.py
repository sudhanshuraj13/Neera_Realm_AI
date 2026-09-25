"""
High-Speed Text Distillation Engine.

Removes EEO boilerplate, legal disclaimers, company perks, and formatting noise
from 1,500+ word JDs and Resumes. Compresses inputs down to ~350 high-signal tokens
to fit ModernBERT context windows and maximize classification throughput.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Union

from .schemas import CandidateProfile, JobPosting

# Common boilerplate and legal headers in ATS postings
EEO_PATTERNS = [
    r"(?i)equal\s+opportunity\s+employer.*?(?=\n\n|\Z)",
    r"(?i)we\s+are\s+committed\s+to\s+diversity.*?(?=\n\n|\Z)",
    r"(?i)affirmative\s+action.*?(?=\n\n|\Z)",
    r"(?i)eeo\s+statement.*?(?=\n\n|\Z)",
    r"(?i)reasonable\s+accommodations?.*?(?=\n\n|\Z)",
    r"(?i)veteran\s+status.*?(?=\n\n|\Z)",
]

BENEFITS_PATTERNS = [
    r"(?i)(?:benefits|what\s+we\s+offer|perks|compensation|why\s+join\s+us):?.*?(?=\n\n|\Z)",
    r"(?i)(?:health,\s*dental,\s*and\s*vision|401\(k\)|unlimited\s+pto|wellness\s+stipend).*?(?=\n\n|\Z)",
]


def strip_html(text: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def strip_boilerplate(text: str) -> str:
    """Remove EEO and benefits boilerplate sections from job descriptions."""
    if not text:
        return ""
    
    cleaned = text
    for pattern in EEO_PATTERNS + BENEFITS_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.DOTALL)
    
    # Normalize multiple newlines and spaces
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def extract_core_requirements(raw_jd: str) -> str:
    """
    Extract the core 'Requirements' or 'Qualifications' section from a JD.
    Falls back to cleaned text if no explicit section headers are found.
    """
    cleaned = strip_html(raw_jd)
    cleaned = strip_boilerplate(cleaned)

    # Search for requirement section headers
    pattern = (
        r"(?i)(?:requirements|qualifications|what\s+you'?ll\s+need|what\s+we'?re\s+looking\s+for|minimum\s+qualifications|must\s+haves?):?\s*"
        r"(.*?)(?=(?:\n\s*(?:about\s+the\s+team|our\s+culture|benefits|perks|how\s+to\s+apply)\b|\Z))"
    )
    match = re.search(pattern, cleaned, flags=re.DOTALL)
    if match and len(match.group(1).strip()) > 60:
        return match.group(1).strip()[:1200]

    # Fallback to the first 1,000 characters of cleaned text
    return cleaned[:1000]


def distill_candidate_profile(candidate: CandidateProfile) -> str:
    """
    Distill a candidate profile into a compact, high-density text summary.
    Size: ~100 - 200 tokens.
    """
    parts = [
        f"Role: {candidate.primary_role}",
        f"Experience: {candidate.years_experience} years",
        f"Skills: {', '.join(candidate.skills[:20])}",
    ]
    if candidate.location:
        parts.append(f"Location: {candidate.location}")
    if candidate.bullet_points:
        bullets = " | ".join(candidate.bullet_points[:4])
        parts.append(f"Accomplishments: {bullets[:500]}")
    elif candidate.raw_text:
        clean_raw = strip_html(candidate.raw_text)[:400]
        parts.append(f"Summary: {clean_raw}")

    return "\n".join(parts)


def distill_job_posting(job: JobPosting) -> str:
    """
    Distill a job posting into a compact, high-density requirements summary.
    Size: ~100 - 200 tokens.
    """
    parts = [
        f"Target Role: {job.title}",
        f"Minimum Experience: {job.min_years_experience} years",
    ]
    if job.required_skills:
        parts.append(f"Required Skills: {', '.join(job.required_skills[:15])}")
    if job.preferred_skills:
        parts.append(f"Preferred Skills: {', '.join(job.preferred_skills[:10])}")
    if job.domain:
        parts.append(f"Domain: {job.domain}")

    if job.raw_text:
        core_reqs = extract_core_requirements(job.raw_text)
        parts.append(f"Core Requirements: {core_reqs[:500]}")

    return "\n".join(parts)


def build_laya_state(candidate: CandidateProfile, job: JobPosting) -> Dict[str, Any]:
    """
    Construct the final structured state dictionary passed into Laya's
    non-autoregressive ModernBERT decision engine.
    """
    return {
        "candidate": {
            "role": candidate.primary_role,
            "years_experience": candidate.years_experience,
            "skills": candidate.skills[:20],
            "key_highlights": candidate.bullet_points[:3] if candidate.bullet_points else candidate.primary_role,
        },
        "job": {
            "title": job.title,
            "min_years_experience": job.min_years_experience,
            "required_skills": job.required_skills[:15],
            "preferred_skills": job.preferred_skills[:10],
            "domain": job.domain or "Technology",
        },
    }
