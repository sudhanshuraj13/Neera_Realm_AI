"""
Tier 0: Hard Knockout & Entity Validation Gate.

Executes deterministic sub-5ms checks on non-negotiable job requirements
(work authorization, minimum years of experience, geographic restrictions).
Prevents compute spend on disqualified applicants.
"""

from __future__ import annotations

from typing import List
from .schemas import CandidateProfile, JobPosting, KnockoutResult, KnockoutStatus


def evaluate_knockouts(candidate: CandidateProfile, job: JobPosting) -> KnockoutResult:
    """
    Run deterministic knockout evaluation.
    
    Args:
        candidate: Candidate profile details.
        job: Job posting criteria.
        
    Returns:
        KnockoutResult with status, pass/fail flag, and specific failure reasons.
    """
    failed_criteria: List[str] = []

    # 1. Work Authorization Check
    if candidate.work_authorization is False:
        failed_criteria.append("Candidate lacks required work authorization.")

    # 2. Strict Minimum Experience Gate
    # Allow a grace delta of 1.0 year for high-potential candidates
    if job.min_years_experience > 0:
        required_floor = max(0.0, job.min_years_experience - 1.0)
        if candidate.years_experience < required_floor:
            failed_criteria.append(
                f"Experience deficiency: {candidate.years_experience:.1f} YOE provided, "
                f"minimum {job.min_years_experience:.1f} YOE required."
            )

    # 3. Location / Geographic Restriction (if not remote)
    if not job.is_remote and job.location and candidate.location:
        job_loc = job.location.lower().strip()
        cand_loc = candidate.location.lower().strip()
        
        # Check for non-overlapping geographic regions
        if job_loc not in cand_loc and cand_loc not in job_loc:
            # If completely disjoint, flag warning rather than hard reject unless strictly required
            if "us only" in job_loc and "us" not in cand_loc and "united states" not in cand_loc:
                failed_criteria.append(f"Geographic mismatch: role requires '{job.location}', candidate is in '{candidate.location}'.")

    if failed_criteria:
        return KnockoutResult(
            status=KnockoutStatus.FAILED,
            passed=False,
            reason="; ".join(failed_criteria),
            failed_criteria=failed_criteria,
        )

    return KnockoutResult(
        status=KnockoutStatus.PASSED,
        passed=True,
        reason="All non-negotiable knockout criteria satisfied.",
        failed_criteria=[],
    )
