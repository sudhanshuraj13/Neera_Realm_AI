"""
Pydantic v2 schemas for the NextGen 4-Tier Semantic Decision ATS Engine.

Defines the request and response models for scoring a candidate's resume
directly against a target Job Description (JD) using:
  Tier 0: Hard Knockout Gate (<5ms)
  Tier 1: Dense Semantic Vector Embeddings (all-MiniLM-L6-v2)
  Tier 2: Laya ModernBERT System-1 Non-Autoregressive Decision Head (~35ms)
  Tier 3: Dual-Persona Intelligence (Recruiter Triage & Candidate Coaching)
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field, model_validator


class ATSScoreRequest(BaseModel):
    """Request payload for evaluating a Resume against a Job Description."""

    resume_text: str = Field(..., min_length=20, description="Full extracted text of candidate's resume")
    jd_text: Optional[str] = Field(default=None, description="Full text of the target job description")
    job_description: Optional[str] = Field(default=None, description="Alias for target job description")
    experience_tier: Optional[str] = Field(
        default="Fresher",
        description="Target experience level: 'Fresher' (0-1 YOE), '1 YOE', '2+ YOE', or '3+ YOE'"
    )
    target_role: Optional[str] = Field(
        default=None,
        description="Target job title (e.g. 'Frontend Engineer', 'Full-Stack Developer')"
    )

    @model_validator(mode="after")
    def validate_jd_text(self) -> ATSScoreRequest:
        """Ensure either jd_text or job_description is provided."""
        if not self.jd_text and self.job_description:
            self.jd_text = self.job_description
        elif not self.jd_text and not self.job_description:
            raise ValueError("Either 'jd_text' or 'job_description' must be provided (min length 20 chars).")
        if len(self.jd_text or "") < 20:
            raise ValueError("Job description text must be at least 20 characters.")
        return self


class GoogleXYZRewrite(BaseModel):
    """A bullet point rewritten using Google's XYZ formula: Accomplished [X] as measured by [Y], by doing [Z]."""

    original_bullet: str = Field(..., description="Weak or unquantified bullet from the candidate's resume")
    rewritten_bullet: str = Field(..., description="Strong, recruiter-optimized bullet using Google XYZ formula")
    impact_metric: str = Field(..., description="The quantifiable measurement (e.g., 'reduced latency by 35%')")
    reasoning: str = Field(..., description="Why this rewrite will pass enterprise ATS filters")


class ATSScoreResponse(BaseModel):
    """Structured response from the NextGen 4-Tier Semantic Decision ATS Scorer."""

    composite_score: int = Field(..., ge=0, le=100, description="Final calibrated ATS score (0-100)")
    tier0_knockout_passed: bool = Field(default=True, description="Whether candidate passed all non-negotiable knockout gates")
    tier0_knockout_reason: str = Field(default="All non-negotiable criteria satisfied.", description="Detailed knockout rationale")
    tier1_vector_score: int = Field(..., ge=0, le=100, description="30ms Vector Cosine Similarity score (0-100)")
    tier2_laya_score: int = Field(default=80, ge=0, le=100, description="Laya ModernBERT System-1 non-autoregressive decision score (0-100)")
    tier2_rubric_score: int = Field(..., ge=0, le=100, description="Backward compatible alias to Tier 2 decision score (0-100)")
    laya_qualification_tier: str = Field(default="strong", description="Laya qualification tier: 'unqualified', 'borderline', 'strong', 'interview_ready'")
    laya_confidence: float = Field(default=0.85, description="Laya calibrated decision confidence")
    laya_seniority_fit: str = Field(default="appropriate", description="Laya seniority judgment: 'underqualified', 'appropriate', 'overqualified'")
    match_tier: str = Field(..., description="'Strong Match', 'Competitive Fit', or 'Needs Optimization'")
    matched_skills: list[str] = Field(default_factory=list, description="Skills present in both resume and JD")
    missing_critical_skills: list[str] = Field(default_factory=list, description="Must-have JD skills missing from resume")
    experience_alignment: str = Field(..., description="Evaluation of seniority, project scale, and stack translatability")
    google_xyz_rewrites: list[GoogleXYZRewrite] = Field(
        default_factory=list,
        description="Google-XYZ formula rewrites of candidate's experience bullets"
    )
    recruiter_recommendation: str = Field(
        default="ADVANCE_TO_INTERVIEW",
        description="Primary recruiter action: 'ADVANCE_TO_INTERVIEW', 'MANUAL_REVIEW', or 'AUTO_REJECT'"
    )
    targeted_interview_questions: list[str] = Field(
        default_factory=list,
        description="Targeted technical interview questions probing gap areas"
    )
    keyword_stuffing_risk: str = Field(
        default="LOW",
        description="Anti-stuffing and white text anomaly risk: 'LOW' or 'SUSPECTED_ANOMALY'"
    )
    actionable_recommendations: list[str] = Field(
        default_factory=list,
        description="Immediate tactical steps to increase match score"
    )
    computation_time_ms: float = Field(..., description="Total execution time in milliseconds")

