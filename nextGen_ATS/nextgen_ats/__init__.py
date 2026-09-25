"""
nextGen_ATS: High-Performance 4-Tier Semantic Decision ATS Engine.

Combines Laya's non-autoregressive ModernBERT System-1 models with
dense semantic embeddings and dual-persona intelligence (Recruiter Triage & Candidate Coaching).
"""

__version__ = "0.1.0"
__author__ = "Atlas AI / Neera Realm AI Team"
__license__ = "Apache-2.0"

from .engine import NextGenATSEngine
from .schemas import (
    ATSNextGenReport,
    CandidateCoachingReport,
    CandidateProfile,
    GoogleXYZRewrite,
    InterviewQuestion,
    JobPosting,
    KnockoutResult,
    KnockoutStatus,
    LayaDecisionMetrics,
    QualificationTier,
    RecruiterDossier,
    VectorSimilarityResult,
)
from .distillation import (
    distill_candidate_profile,
    distill_job_posting,
    strip_boilerplate,
)

__all__ = [
    "NextGenATSEngine",
    "CandidateProfile",
    "JobPosting",
    "ATSNextGenReport",
    "KnockoutStatus",
    "KnockoutResult",
    "QualificationTier",
    "LayaDecisionMetrics",
    "VectorSimilarityResult",
    "GoogleXYZRewrite",
    "CandidateCoachingReport",
    "RecruiterDossier",
    "InterviewQuestion",
    "distill_candidate_profile",
    "distill_job_posting",
    "strip_boilerplate",
]
