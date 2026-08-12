"""
ATS Job Board Adapter.

Fetches job listings from target dream companies (Greenhouse, Lever, Ashby)
and global public job aggregators (Remotive, Arbeitnow).
"""

from __future__ import annotations

import logging

from app.schemas.jobs import UnifiedJob
from app.services.ats_service import fetch_all_jobs
from app.services.job_adapters.base_adapter import BaseJobAdapter

logger = logging.getLogger("neera_ai_service.job_adapters.ats")


class ATSJobAdapter(BaseJobAdapter):
    """Adapter for Greenhouse, Lever, Ashby, Remotive, and Arbeitnow feeds."""

    @property
    def source_name(self) -> str:
        return "ATS"

    async def fetch_jobs(self, user_context: dict) -> list[UnifiedJob]:
        """Fetch jobs from ATS services and map to UnifiedJob format."""
        company_slugs = user_context.get("target_companies") or []
        primary_role = user_context.get("primary_role", "")
        target_roles = user_context.get("target_roles") or []
        skills = user_context.get("skills") or []

        try:
            raw_jobs = await fetch_all_jobs(
                company_slugs=company_slugs,
                include_global_startups=True,
                primary_role=primary_role,
                target_roles=target_roles,
                skills=skills,
            )

            unified_jobs: list[UnifiedJob] = []
            for j in raw_jobs:
                job_id = f"ats_{hash((j.company, j.title, j.apply_url)) & 0xFFFFFFFF:08x}"
                unified_jobs.append(
                    UnifiedJob(
                        id=job_id,
                        company=j.company,
                        title=j.title,
                        location=j.location or "Remote",
                        apply_url=j.apply_url,
                        source=self.source_name,
                        posted_at=None,
                    )
                )

            logger.info("✅ [ATS Adapter] Fetched %d jobs", len(unified_jobs))
            return unified_jobs
        except Exception as e:
            logger.warning("⚠️ [ATS Adapter] Fetch failed gracefully: %s", e)
            return []
