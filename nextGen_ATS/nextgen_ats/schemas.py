"""
nextGen_ATS Data Schemas.

Type-safe Pydantic v2 models representing candidates, job postings,
intermediate scoring tiers, and dual-persona intelligence outputs.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class KnockoutStatus(str, Enum):
    """Knockout gate evaluation status."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"


class QualificationTier(str, Enum):
    """Candidate qualification category."""
    UNQUALIFIED = "unqualified"
    BORDERLINE = "borderline"
    STRONG = "strong"
    INTERVIEW_READY = "interview_ready"


class CandidateProfile(BaseModel):
    """Structured candidate profile for ATS evaluation."""
    candidate_id: Optional[str] = Field(default=None, description="Unique candidate ID")
    name: Optional[str] = Field(default="Candidate", description="Candidate name")
    primary_role: str = Field(..., description="Candidate's current or target job title")
    years_experience: float = Field(default=0.0, description="Total professional years of experience")
    skills: List[str] = Field(default_factory=list, description="List of technical and domain skills")
    location: Optional[str] = Field(default=None, description="Candidate location / country")
    work_authorization: Optional[bool] = Field(default=True, description="Legal work authorization flag")
    bullet_points: List[str] = Field(default_factory=list, description="Key accomplishment bullets from resume")
    raw_text: Optional[str] = Field(default=None, description="Raw unparsed resume text")


class JobPosting(BaseModel):
    """Structured job posting requirements."""
    job_id: Optional[str] = Field(default=None, description="Unique Job ID")
    title: str = Field(..., description="Target job title")
    company: Optional[str] = Field(default="Company", description="Hiring company")
    location: Optional[str] = Field(default=None, description="Job location")
    is_remote: bool = Field(default=False, description="Remote friendly role")
    min_years_experience: float = Field(default=0.0, description="Minimum mandatory years of experience")
    required_skills: List[str] = Field(default_factory=list, description="Mandatory required skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Nice-to-have skills")
    domain: Optional[str] = Field(default=None, description="Industry or technical domain (e.g. Fintech, Cloud)")
    raw_text: Optional[str] = Field(default=None, description="Raw job description text")


class KnockoutResult(BaseModel):
    """Tier 0 hard knockout validation outcome."""
    status: KnockoutStatus = Field(..., description="Knockout gate result")
    passed: bool = Field(..., description="Whether candidate passed all non-negotiable filters")
    reason: str = Field(default="All knockout criteria satisfied", description="Explanation")
    failed_criteria: List[str] = Field(default_factory=list, description="List of failed knockout rules")


class VectorSimilarityResult(BaseModel):
    """Tier 1 dense vector semantic alignment outcome."""
    raw_cosine: float = Field(..., description="Raw cosine similarity (-1.0 to 1.0)")
    calibrated_score: int = Field(..., ge=0, le=100, description="Calibrated vector score (0-100)")
    latency_ms: float = Field(default=0.0, description="Vector computation latency in ms")


class LayaDecisionMetrics(BaseModel):
    """Tier 2 System-1 ModernBERT decision model metrics."""
    seniority_fit: str = Field(..., description="Seniority alignment judgment (e.g. 'appropriate', 'overqualified')")
    tech_translatability_score: int = Field(..., ge=0, le=2, description="Stack translatability (0: Low, 1: Moderate, 2: High)")
    domain_relevance_score: int = Field(..., ge=0, le=2, description="Domain/industry alignment (0: Low, 1: Moderate, 2: High)")
    qualification_tier: QualificationTier = Field(..., description="Overall qualification category")
    decision_confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated RLCD confidence score")
    calibrated_laya_score: int = Field(..., ge=0, le=100, description="Decision model score (0-100)")
    latency_ms: float = Field(default=0.0, description="Laya inference latency in ms")


class GoogleXYZRewrite(BaseModel):
    """Candidate resume bullet rewritten according to Google's XYZ formula."""
    original_bullet: str = Field(..., description="Original raw resume bullet point")
    rewritten_bullet: str = Field(..., description="Rewritten bullet: 'Accomplished [X] as measured by [Y], by doing [Z]'")
    impact_explanation: str = Field(..., description="Why this rewrite increases ATS ranking & recruiter interest")


class CandidateCoachingReport(BaseModel):
    """Actionable candidate guidance and ATS optimization roadmap."""
    match_score: int = Field(..., ge=0, le=100, description="Final candidate match score")
    fit_tier: str = Field(..., description="Descriptive fit tier (e.g. 'Strong Candidate', 'Borderline')")
    matched_skills: List[str] = Field(default_factory=list, description="Skills verified in candidate resume")
    missing_critical_skills: List[str] = Field(default_factory=list, description="Essential skills missing from resume")
    prioritized_recommendations: List[str] = Field(default_factory=list, description="Top actionable recommendations")
    google_xyz_rewrites: List[GoogleXYZRewrite] = Field(default_factory=list, description="Tailored bullet rewrites")
    ats_readiness_checklist: List[str] = Field(default_factory=list, description="Pre-flight submission checklist")


class InterviewQuestion(BaseModel):
    """Targeted technical question for recruiters/interviewers."""
    topic: str = Field(..., description="Skill or gap area being probed")
    question: str = Field(..., description="Specific technical or architectural question")
    what_to_look_for: str = Field(..., description="Expected strong signal vs red flag in candidate answer")


class RecruiterDossier(BaseModel):
    """Executive recruiter briefing and interview preparation."""
    candidate_id: Optional[str] = None
    candidate_name: str
    overall_score: int = Field(..., ge=0, le=100)
    recommendation: str = Field(..., description="'ADVANCE_TO_INTERVIEW', 'MANUAL_REVIEW', or 'AUTO_REJECT'")
    executive_summary: str = Field(..., description="Concise 2-sentence recruiter summary")
    seniority_match: str = Field(..., description="Assessment of candidate level vs role level")
    keyword_stuffing_detected: bool = Field(default=False, description="Anomaly flag for stuffed/hidden text")
    stuffing_risk_level: str = Field(default="LOW", description="'LOW', 'MEDIUM', 'HIGH'")
    interview_questions: List[InterviewQuestion] = Field(default_factory=list, description="Questions targeted at gaps")


class ATSNextGenReport(BaseModel):
    """Comprehensive, unified output of the 4-Tier nextGen_ATS engine."""
    candidate_name: str
    job_title: str
    overall_ats_score: int = Field(..., ge=0, le=100, description="Weighted composite ATS score")
    knockout: KnockoutResult
    vector_score: int
    laya_metrics: LayaDecisionMetrics
    candidate_coaching: CandidateCoachingReport
    recruiter_dossier: RecruiterDossier
    execution_time_ms: float = Field(..., description="Total pipeline processing time in milliseconds")
