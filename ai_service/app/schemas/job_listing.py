"""
Pydantic v2 schema for standardized ATS job listings.

Used by the ATS service to normalize responses from Greenhouse, Lever, and Ashby
into a single unified format.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class JobListing(BaseModel):
    """A single job listing normalized from any ATS provider."""

    company: str = Field(..., description="Company name")
    title: str = Field(..., description="Job title")
    location: str = Field(..., description="Job location or 'Remote'")
    apply_url: str = Field(..., description="Direct application URL")
