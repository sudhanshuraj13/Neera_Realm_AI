"""
Pydantic v2 schemas for resume parsing.

Defines the nested extraction schema used by the LLM resume parser,
plus the FastAPI request/response contract for POST /api/v1/resume/parse.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Experience(BaseModel):
    """A single work experience entry extracted from a resume."""

    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    duration: str = Field(..., description="Duration, e.g. 'Jan 2022 – Present'")
    highlights: list[str] = Field(
        default_factory=list,
        description="Key accomplishments or responsibilities",
    )


class Project(BaseModel):
    """A single project entry extracted from a resume."""

    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Brief project description")
    technologies: list[str] = Field(
        default_factory=list,
        description="Technologies, frameworks, or tools used",
    )


class ResumeProfile(BaseModel):
    """
    High-fidelity career profile extracted from a resume.

    This is the canonical schema that the LLM must output.
    Stored as JSONB in the User.resumeJson column.
    """

    primary_role: str = Field(..., description="Candidate's primary role, e.g. 'Backend Engineer'")
    years_experience: int = Field(..., description="Total years of professional experience")
    skills: list[str] = Field(
        default_factory=list,
        description="Technical and soft skills extracted from the resume",
    )
    target_roles: list[str] = Field(
        default_factory=list,
        description="Roles the candidate is targeting or qualified for",
    )
    preferred_domains: list[str] = Field(
        default_factory=list,
        description="Industries or domains the candidate prefers (e.g. 'FinTech', 'AI/ML')",
    )
    target_companies: list[str] = Field(
        default_factory=list,
        description="Target or dream companies candidate wants to watch or apply for",
    )
    experience: list[Experience] = Field(
        default_factory=list,
        description="Work experience entries",
    )
    projects: list[Project] = Field(
        default_factory=list,
        description="Notable projects",
    )


class ResumeParseRequest(BaseModel):
    """Inbound payload from the Node.js gateway for resume parsing."""

    user_id: str = Field(..., description="Internal user ID from Neon PostgreSQL")
    raw_text: str = Field(..., description="Raw text extracted from the PDF resume")


class ResumeParseResponse(BaseModel):
    """Outbound payload returned to the Node.js gateway after resume parsing."""

    profile: ResumeProfile = Field(..., description="Structured resume profile")
