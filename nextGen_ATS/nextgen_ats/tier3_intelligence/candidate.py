"""
Tier 3: Candidate Coaching & Optimization Module.

Generates actionable career intelligence for candidates:
- Missing critical skills roadmap
- Google-XYZ formula bullet rewrites ("Accomplished [X] as measured by [Y], by doing [Z]")
- Pre-submission ATS readiness checklist
"""

from __future__ import annotations

import re
from typing import List, Optional

from ..schemas import (
    CandidateCoachingReport,
    CandidateProfile,
    GoogleXYZRewrite,
    JobPosting,
    LayaDecisionMetrics,
    QualificationTier,
)


def _generate_google_xyz_rewrites(
    bullets: List[str],
    target_skills: List[str],
) -> List[GoogleXYZRewrite]:
    """
    Transform raw resume bullets into quantifiable Google-XYZ accomplishments:
    'Accomplished [X] as measured by [Y], by doing [Z]'.
    Employs domain-aware contextual analysis to avoid repetitive template appending.
    """
    rewrites: List[GoogleXYZRewrite] = []
    skill_hint = target_skills[0] if target_skills else "production systems"

    for bullet in bullets[:3]:
        cleaned = bullet.strip().rstrip(".")
        if not cleaned or len(cleaned) < 15:
            continue

        b_lower = cleaned.lower()
        has_metrics = bool(re.search(r"\b\d+%\b|\b\d+k\b|\b\d+x\b|\b\d+\.\d+\b", b_lower))
        passive_starts = ["worked on", "responsible for", "helped with", "assisted in", "participated in", "involved in"]
        is_passive = any(b_lower.startswith(p) for p in passive_starts)

        # 1. If candidate already quantified impact with active verbs, elevate the technical architecture
        if has_metrics and not is_passive:
            if any(kw in b_lower for kw in ("database", "sql", "query", "postgres", "supabase", "api", "load")):
                rewritten = (
                    f"{cleaned}, establishing sub-100ms response SLAs and hardening data tier resilience."
                )
                explanation = (
                    "Elevated an already quantified bullet by linking technical optimization directly to an enterprise SLA."
                )
            elif any(kw in b_lower for kw in ("ocr", "rag", "ai", "model", "llm", "chatbot")):
                rewritten = (
                    f"{cleaned}, while maintaining strict evaluation guardrails and reducing token consumption."
                )
                explanation = (
                    "Strengthened AI/ML accomplishment by detailing operational cost-efficiency and production safety guardrails."
                )
            else:
                rewritten = (
                    f"{cleaned}, streamlining workflow execution across cross-functional engineering teams."
                )
                explanation = (
                    "Enhanced metric-driven bullet with organizational impact and cross-functional leadership."
                )

        # 2. If passive, replace opening with strong technical ownership verb
        elif is_passive:
            active_verb = "Architected and delivered" if "architect" not in b_lower else "Spearheaded"
            stripped_passive = re.sub(r"^(?:worked on|responsible for|helped with|assisted in|participated in|involved in)\s*", "", cleaned, flags=re.IGNORECASE)
            rewritten = (
                f"{active_verb} {stripped_passive} using {skill_hint}, "
                f"improving delivery throughput by [25-30%] and eliminating critical process bottlenecks."
            )
            explanation = (
                "Replaced passive participation phrasing with assertive engineering ownership and a measurable throughput target."
            )

        # 3. If missing metrics, synthesize domain-calibrated Google-XYZ metric recommendations
        else:
            if any(kw in b_lower for kw in ("database", "postgres", "sql", "backend", "api", "query")):
                rewritten = (
                    f"{cleaned}, reducing p99 API latency by [20-35%] and sustaining [10k+] daily transactions using {skill_hint}."
                )
                explanation = (
                    "Applied Google-XYZ formula: quantified backend execution with p99 latency reduction and transaction volume."
                )
            elif any(kw in b_lower for kw in ("data", "etl", "pipeline", "ingestion", "bi", "reporting", "tableau", "powerbi")):
                rewritten = (
                    f"{cleaned}, cutting data ingestion turnaround from [hours to minutes] and powering automated business intelligence reports."
                )
                explanation = (
                    "Applied Google-XYZ formula: framed data engineering with turnaround time reduction and downstream BI enablement."
                )
            elif any(kw in b_lower for kw in ("ai", "llm", "rag", "ocr", "search", "tesseract")):
                rewritten = (
                    f"{cleaned}, achieving [95%+ accuracy] and reducing manual operational review by [40%] through automated inference."
                )
                explanation = (
                    "Applied Google-XYZ formula: added model evaluation benchmarks (accuracy) and human-in-the-loop labor reduction."
                )
            else:
                rewritten = (
                    f"{cleaned}, improving operational turnaround by [25%] while ensuring 99.9% pipeline reliability."
                )
                explanation = (
                    "Applied Google-XYZ formula: converted general engineering output into quantifiable business impact."
                )

        rewrites.append(
            GoogleXYZRewrite(
                original_bullet=cleaned,
                rewritten_bullet=rewritten,
                impact_explanation=explanation,
            )
        )

    # Fallback starter rewrite if no bullets were supplied
    if not rewrites:
        rewrites.append(
            GoogleXYZRewrite(
                original_bullet="Developed backend APIs and handled database management.",
                rewritten_bullet=(
                    f"Engineered high-concurrency RESTful APIs and optimized SQL query pipelines using {skill_hint}, "
                    f"reducing p99 response times by 40% under peak load."
                ),
                impact_explanation="Demonstrates how to frame basic development into quantifiable architectural achievement.",
            )
        )

    return rewrites


def generate_candidate_coaching(
    candidate: CandidateProfile,
    job: JobPosting,
    overall_score: int,
    laya_metrics: LayaDecisionMetrics,
) -> CandidateCoachingReport:
    """
    Synthesize complete candidate coaching report.
    """
    cand_skills_lower = {s.lower().strip() for s in candidate.skills}
    req_skills = job.required_skills or []

    matched: List[str] = []
    missing: List[str] = []

    for req in req_skills:
        req_clean = req.strip()
        if req_clean.lower() in cand_skills_lower:
            matched.append(req_clean)
        else:
            missing.append(req_clean)

    # Categorize Fit Tier
    if overall_score >= 85:
        fit_tier = "Exceptional Candidate (Direct Interview Recommendation)"
    elif overall_score >= 70:
        fit_tier = "Strong Candidate (High Match with Minor Polish Needed)"
    elif overall_score >= 50:
        fit_tier = "Borderline Candidate (Bridge Gaps Before Applying)"
    else:
        fit_tier = "Needs Significant Alignment (Major Skill / Seniority Gaps)"

    # Actionable prioritized recommendations
    recommendations: List[str] = []
    if missing:
        top_missing = missing[:3]
        recommendations.append(
            f"Address High-Priority Skill Gaps: Feature projects demonstrating '{', '.join(top_missing)}'."
        )

    if laya_metrics.seniority_fit == "underqualified":
        recommendations.append(
            f"Seniority Deficit: Role requires ~{job.min_years_experience:.0f} YOE. Highlight high-impact, independent architectural leadership to compensate."
        )
    elif laya_metrics.seniority_fit == "overqualified":
        recommendations.append(
            "Overqualification Alert: Emphasize hands-on technical execution rather than pure managerial delegation."
        )

    recommendations.append(
        "Quantify Business Metrics: Incorporate percentage improvements (e.g. latency, cost reduction, throughput) in at least 3 bullet points."
    )

    # Generate Google-XYZ rewrites
    rewrites = _generate_google_xyz_rewrites(candidate.bullet_points, missing or req_skills or candidate.skills)

    # Standard ATS submission checklist
    checklist = [
        "Single-column plain text format (tables and multi-column layouts break legacy parsers).",
        "Target keywords embedded directly in context within project experience bullets.",
        "Clear date formatting (Month Year – Month Year) for automated seniority parsing.",
        "PDF exported directly from digital document (avoid scanned images or non-selectable text).",
    ]

    return CandidateCoachingReport(
        match_score=overall_score,
        fit_tier=fit_tier,
        matched_skills=matched,
        missing_critical_skills=missing,
        prioritized_recommendations=recommendations,
        google_xyz_rewrites=rewrites,
        ats_readiness_checklist=checklist,
    )
