"""
nextGen_ATS Main Orchestration Engine.

Orchestrates the complete 4-Tier decision pipeline:
  Tier 0: Hard Knockout Gate (<5ms)
  Tier 1: Dense Semantic Vector Alignment (~25ms)
  Tier 2: Laya ModernBERT System-1 Decision Head (~35ms)
  Tier 3: Dual Intelligence Layer (Recruiter Triage & Candidate Coaching)
"""

from __future__ import annotations

import logging
import time
from typing import List, Optional

from .distillation import (
    build_laya_state,
    distill_candidate_profile,
    distill_job_posting,
)
from .schemas import (
    ATSNextGenReport,
    CandidateProfile,
    JobPosting,
    KnockoutResult,
)
from .tier0_knockout import evaluate_knockouts
from .tier1_vector import compute_vector_alignment
from .tier2_laya import evaluate_laya_decision
from .tier3_intelligence import (
    generate_candidate_coaching,
    generate_recruiter_dossier,
)

logger = logging.getLogger("nextgen_ats.engine")


class NextGenATSEngine:
    """
    High-performance 4-Tier ATS decision and intelligence engine.
    """

    def __init__(self, vector_weight: float = 0.35, laya_weight: float = 0.65):
        """
        Initialize the NextGenATSEngine.

        Args:
            vector_weight: Weight allocated to Tier 1 vector similarity (default: 0.35).
            laya_weight: Weight allocated to Tier 2 Laya decision score (default: 0.65).
        """
        self.vector_weight = vector_weight
        self.laya_weight = laya_weight
        logger.info(
            "Initialized NextGenATSEngine (vector_weight=%.2f, laya_weight=%.2f)",
            vector_weight,
            laya_weight,
        )

    def evaluate(
        self,
        candidate: CandidateProfile,
        job: JobPosting,
    ) -> ATSNextGenReport:
        """
        Execute full 4-tier ATS evaluation for a single candidate against a job posting.

        Args:
            candidate: CandidateProfile instance.
            job: JobPosting instance.

        Returns:
            ATSNextGenReport containing multi-tier scores, recruiter dossier, and candidate coaching.
        """
        start_time = time.perf_counter()

        # Step 0: Distillation
        distilled_resume = distill_candidate_profile(candidate)
        distilled_jd = distill_job_posting(job)
        laya_state = build_laya_state(candidate, job)

        # Tier 0: Hard Knockout Evaluation
        knockout_res = evaluate_knockouts(candidate, job)

        # Tier 1: Dense Vector Similarity
        vector_res = compute_vector_alignment(distilled_resume, distilled_jd)

        # Tier 2: Laya ModernBERT System-1 Decision Engine
        laya_res = evaluate_laya_decision(laya_state, candidate, job)

        # Calculate Calibrated Composite Score
        if not knockout_res.passed:
            # Heavily penalize knockout failures while retaining baseline vector signal
            overall_score = min(25, int(vector_res.calibrated_score * 0.3))
        else:
            raw_composite = (
                vector_res.calibrated_score * self.vector_weight
                + laya_res.calibrated_laya_score * self.laya_weight
            )
            overall_score = int(round(raw_composite))

        # Tier 3: Dual Intelligence Layer
        coaching_report = generate_candidate_coaching(
            candidate=candidate,
            job=job,
            overall_score=overall_score,
            laya_metrics=laya_res,
        )

        recruiter_dossier = generate_recruiter_dossier(
            candidate=candidate,
            job=job,
            overall_score=overall_score,
            knockout=knockout_res,
            laya_metrics=laya_res,
        )

        total_elapsed_ms = (time.perf_counter() - start_time) * 1000

        return ATSNextGenReport(
            candidate_name=candidate.name or "Candidate",
            job_title=job.title,
            overall_ats_score=overall_score,
            knockout=knockout_res,
            vector_score=vector_res.calibrated_score,
            laya_metrics=laya_res,
            candidate_coaching=coaching_report,
            recruiter_dossier=recruiter_dossier,
            execution_time_ms=round(total_elapsed_ms, 2),
        )

    def rank_candidates(
        self,
        candidates: List[CandidateProfile],
        job: JobPosting,
    ) -> List[ATSNextGenReport]:
        """
        Rank multiple candidates concurrently against a single job posting.
        Returns reports sorted descending by overall_ats_score.
        """
        reports = [self.evaluate(cand, job) for cand in candidates]
        reports.sort(key=lambda r: r.overall_ats_score, reverse=True)
        return reports

    def quick_scan(
        self,
        resume_text: str,
        jd_text: str,
        candidate_name: str = "Candidate",
        primary_role: str = "Software Engineer",
        target_title: str = "Software Engineer",
        min_yoe: float = 3.0,
        cand_yoe: float = 3.0,
    ) -> ATSNextGenReport:
        """
        Convenience method to scan raw resume and JD texts directly.
        """
        candidate = CandidateProfile(
            name=candidate_name,
            primary_role=primary_role,
            years_experience=cand_yoe,
            raw_text=resume_text,
            skills=[w.strip() for w in resume_text[:300].split(",") if len(w.strip()) > 2],
        )
        job = JobPosting(
            title=target_title,
            min_years_experience=min_yoe,
            raw_text=jd_text,
            required_skills=[w.strip() for w in jd_text[:300].split(",") if len(w.strip()) > 2],
        )
        return self.evaluate(candidate, job)
