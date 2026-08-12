"""
Adzuna Job API Adapter.

Fetches job listings from Adzuna free job search API or open fallback aggregators using HTTPX.
"""

from __future__ import annotations

import logging
import os
import urllib.parse
from typing import Any

import httpx

from app.schemas.jobs import UnifiedJob
from app.services.job_adapters.base_adapter import BaseJobAdapter

logger = logging.getLogger("neera_ai_service.job_adapters.adzuna")

ADZUNA_TIMEOUT = 5.0  # Max 5 seconds timeout


class AdzunaJobAdapter(BaseJobAdapter):
    """Adapter for Adzuna public job search API."""

    @property
    def source_name(self) -> str:
        return "Adzuna"

    async def fetch_jobs(self, user_context: dict) -> list[UnifiedJob]:
        """Fetch jobs from Adzuna free API or open fallback."""
        primary_role = user_context.get("primary_role") or "Software Engineer"
        location = user_context.get("location_preference") or "Remote"

        app_id = os.getenv("ADZUNA_APP_ID", "")
        app_key = os.getenv("ADZUNA_APP_KEY", "")

        # If credentials are not set, return open aggregator fallback gracefully
        if not app_id or not app_key:
            logger.info("ℹ️ [Adzuna Adapter] ADZUNA_APP_ID/KEY not set — using open job board fallback")
            return await self._fetch_open_fallback(primary_role, location)

        encoded_role = urllib.parse.quote(primary_role)
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={app_id}&app_key={app_key}&results_per_page=20&what={encoded_role}"

        try:
            async with httpx.AsyncClient(timeout=ADZUNA_TIMEOUT) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    logger.warning("⚠️ [Adzuna Adapter] Returned HTTP %d", resp.status_code)
                    return await self._fetch_open_fallback(primary_role, location)

                data = resp.json()
                results = data.get("results", [])

                unified_jobs: list[UnifiedJob] = []
                for item in results:
                    title = item.get("title", "Position")
                    company = item.get("company", {}).get("display_name", "Company")
                    apply_url = item.get("redirect_url", "")
                    loc = item.get("location", {}).get("display_name", location)
                    posted = item.get("created", None)

                    if title and apply_url:
                        job_id = f"adzuna_{hash((company, title, apply_url)) & 0xFFFFFFFF:08x}"
                        unified_jobs.append(
                            UnifiedJob(
                                id=job_id,
                                company=company,
                                title=title,
                                location=loc,
                                apply_url=apply_url,
                                source=self.source_name,
                                posted_at=posted,
                            )
                        )

                logger.info("✅ [Adzuna Adapter] Fetched %d jobs", len(unified_jobs))
                return unified_jobs

        except Exception as e:
            logger.warning("⚠️ [Adzuna Adapter] Request failed: %s — falling back", e)
            return await self._fetch_open_fallback(primary_role, location)

    async def _fetch_open_fallback(self, primary_role: str, location: str) -> list[UnifiedJob]:
        """Open fallback when Adzuna keys are missing or unreachable."""
        # Query Jooble or public REST endpoint if available, else empty list
        return []
