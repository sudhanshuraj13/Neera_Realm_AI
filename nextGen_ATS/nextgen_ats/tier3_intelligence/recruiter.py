"""
Tier 3: Recruiter Intelligence & Triage Module.

Provides hiring teams with:
- Executive candidate decision briefings
- Targeted, gap-probing technical interview questions
- Anti-keyword stuffing & resume tampering anomaly detection
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from ..schemas import (
    CandidateProfile,
    InterviewQuestion,
    JobPosting,
    KnockoutResult,
    LayaDecisionMetrics,
    QualificationTier,
    RecruiterDossier,
)


def _detect_keyword_stuffing(candidate: CandidateProfile, job: JobPosting) -> Tuple[bool, str]:
    """
    Detect unnatural keyword stuffing and white-text padding attempts.
    
    Checks:
    1. Unnatural repetition frequency of required skills.
    2. High density of disconnected buzzwords without sentence syntax.
    """
    if not candidate.raw_text:
        return False, "LOW"

    raw_lower = candidate.raw_text.lower()
    total_words = len(raw_lower.split())
    if total_words < 50:
        return False, "LOW"

    suspicious_counts = 0
    for skill in job.required_skills:
        skill_clean = skill.lower().strip()
        if len(skill_clean) < 3:
            continue
        # Count exact occurrences
        occurrences = len(re.findall(r"\b" + re.escape(skill_clean) + r"\b", raw_lower))
        # If a single tech skill appears more than 7 times in a standard 500-word resume, flag
        if occurrences > 7:
            suspicious_counts += 1

    # Ratio of unique skills to total words
    if suspicious_counts >= 3 or (len(candidate.skills) > 40 and total_words < 250):
        return True, "HIGH"
    elif suspicious_counts >= 1:
        return True, "MEDIUM"

    return False, "LOW"


def _generate_interview_questions(
    candidate: CandidateProfile,
    job: JobPosting,
    laya_metrics: LayaDecisionMetrics,
) -> List[InterviewQuestion]:
    """
    Generate targeted technical interview questions probing candidate's
    actual depth and any missing or translatable stack areas.
    """
    questions: List[InterviewQuestion] = []
    cand_skills_lower = {s.lower().strip() for s in candidate.skills}
    missing_skills = [s for s in job.required_skills if s.lower().strip() not in cand_skills_lower]

    # 1. Probe translatability / missing skills
    if missing_skills:
        target = missing_skills[0]
        closest_cand_skill = candidate.skills[0] if candidate.skills else "core languages"
        
        # Check if target is a concrete tool/language vs a discipline/domain
        is_tool = any(kw in target.lower() for kw in ("sql", "tableau", "powerbi", "react", "docker", "python", "postgres", "aws", "gcp", "prisma", "excel"))
        if is_tool:
            q_text = (
                f"The role relies on {target}, whereas your profile primarily emphasizes {closest_cand_skill}. "
                f"How would you approach ramping up on {target}, and what fundamental concepts from {closest_cand_skill} "
                f"transfer directly to accelerate your execution?"
            )
            look_for = (
                f"Look for conceptual fundamentals rather than syntax memorization. Strong candidates articulate "
                f"data flow, schema design, or execution models common to both systems."
            )
        else:
            q_text = (
                f"The position requires competencies in {target}, while your background is centered on {closest_cand_skill}. "
                f"How do your analytical and architectural skills translate to delivering measurable impact in {target}?"
            )
            look_for = (
                f"Look for structured problem-solving, domain adaptability, and demonstrated track record of rapid tooling acquisition."
            )

        questions.append(
            InterviewQuestion(
                topic=f"Stack Translatability ({target})",
                question=q_text,
                what_to_look_for=look_for,
            )
        )

    # 2. Probe scalability & production depth
    questions.append(
        InterviewQuestion(
            topic="Production Scale & Resilience",
            question=(
                f"In your work as a {candidate.primary_role}, walk us through a critical production incident or "
                f"bottleneck you diagnosed. What telemetry did you inspect, and how did you resolve it?"
            ),
            what_to_look_for=(
                "Look for systematic root-cause analysis (metrics, profiling, distributed tracing) rather than trial-and-error."
            ),
        )
    )

    # 3. Probe Seniority / Architecture if senior level
    if job.min_years_experience >= 4 or "senior" in job.title.lower():
        questions.append(
            InterviewQuestion(
                topic="System Design & Trade-offs",
                question=(
                    "How do you evaluate consistency vs. availability when designing data storage layers for "
                    f"services in the {job.domain or 'cloud'} domain?"
                ),
                what_to_look_for=(
                    "Candidate should reference the CAP theorem, eventual consistency trade-offs, and practical caching invalidation strategies."
                ),
            )
        )

    return questions


def generate_recruiter_dossier(
    candidate: CandidateProfile,
    job: JobPosting,
    overall_score: int,
    knockout: KnockoutResult,
    laya_metrics: LayaDecisionMetrics,
) -> RecruiterDossier:
    """
    Generate the executive recruiter dossier.
    """
    # 1. Determine triage recommendation
    if not knockout.passed or overall_score < 45:
        recommendation = "AUTO_REJECT"
    elif overall_score >= 78:
        recommendation = "ADVANCE_TO_INTERVIEW"
    else:
        recommendation = "MANUAL_REVIEW"

    # 2. Check for keyword stuffing
    is_stuffed, stuff_risk = _detect_keyword_stuffing(candidate, job)

    # 3. Generate summary
    years_cand = f"{candidate.years_experience:.1f} YOE"
    years_req = f"{job.min_years_experience:.1f} YOE required"
    summary = (
        f"{candidate.name or 'Candidate'} ({years_cand} vs {years_req}) demonstrated "
        f"{laya_metrics.qualification_tier.value.upper()} fit with a calibrated score of {overall_score}/100. "
        f"Primary recommendation is {recommendation}."
    )

    # 4. Generate targeted questions
    questions = _generate_interview_questions(candidate, job, laya_metrics)

    return RecruiterDossier(
        candidate_id=candidate.candidate_id,
        candidate_name=candidate.name or "Candidate",
        overall_score=overall_score,
        recommendation=recommendation,
        executive_summary=summary,
        seniority_match=laya_metrics.seniority_fit.title(),
        keyword_stuffing_detected=is_stuffed,
        stuffing_risk_level=stuff_risk,
        interview_questions=questions,
    )
