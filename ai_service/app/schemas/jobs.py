"""
Unified Job Pydantic Model.

Standardizes job postings across all multi-source adapters (ATS, JobSpy, Adzuna).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class UnifiedJob(BaseModel):
    """Unified job posting model returned by all job search adapters."""

    id: str = Field(..., description="Unique hash or string identifier for deduplication")
    company: str = Field(..., description="Company name")
    title: str = Field(..., description="Job position title")
    location: str = Field(default="Remote / Flexible", description="Job location")
    apply_url: str = Field(..., description="Direct link or application URL")
    source: str = Field(..., description="Source adapter tag (e.g. ATS, JobSpy, Adzuna)")
    posted_at: str | None = Field(default=None, description="Optional ISO timestamp or posting date")
