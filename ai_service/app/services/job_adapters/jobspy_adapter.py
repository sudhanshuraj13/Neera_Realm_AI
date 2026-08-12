"""
JobSpy Adapter for LinkedIn, Indeed, ZipRecruiter & Glassdoor.

Wraps python-jobspy `scrape_jobs` function inside asyncio.to_thread with a strict
timeout and graceful degradation so scraper slowdowns never block the application.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from app.schemas.jobs import UnifiedJob
from app.services.job_adapters.base_adapter import BaseJobAdapter

logger = logging.getLogger("neera_ai_service.job_adapters.jobspy")

JOBSPY_TIMEOUT = 8.0  # Max 8 seconds timeout for JobSpy scraping


def _run_jobspy_sync(search_term: str, location: str, results_wanted: int = 5) -> list[dict[str, Any]]:
    """Synchronous JobSpy scraping function to run inside thread pool."""
    try:
        # pyrefly: ignore [missing-import]
        from jobspy import scrape_jobs

        site_names = ["linkedin", "indeed"]
        logger.info("🔎 [JobSpy Sync] Scraping sites=%s for term='%s' in '%s'", site_names, search_term, location)

        jobs_df = scrape_jobs(
            site_name=site_names,
            search_term=search_term,
            location=location or "Remote",
            results_wanted=results_wanted,
            hours_old=72,
            country_indeed="USA",  # Default fallback country
        )

        if jobs_df is None or jobs_df.empty:
            return []

        results = []
        for _, row in jobs_df.iterrows():
            company = str(row.get("company", "Company")).strip()
            if not company or company.lower() in {"nan", "none", "null"}:
                company = "Company"
            title = str(row.get("title", "Position")).strip()
            job_url = str(row.get("job_url", "") or row.get("job_url_direct", "")).strip()
            loc = str(row.get("location", "Remote")).strip()
            site = str(row.get("site", "JobSpy")).capitalize()

            if title and job_url:
                results.append(
                    {
                        "company": company,
                        "title": title,
                        "apply_url": job_url,
                        "location": loc,
                        "site": site,
                        "date_posted": str(row.get("date_posted", "") or ""),
                    }
                )

        return results

    except ImportError:
        logger.warning("⚠️ python-jobspy is not installed in the environment.")
        return []
    except Exception as e:
        logger.warning("⚠️ [JobSpy Sync] Error during scraping: %s", e)
        return []


class JobSpyAdapter(BaseJobAdapter):
    """Adapter for scraping LinkedIn/Indeed/Glassdoor via python-jobspy."""

    @property
    def source_name(self) -> str:
        return "JobSpy"

    async def fetch_jobs(self, user_context: dict) -> list[UnifiedJob]:
        """Fetch jobs concurrently with strict timeout."""
        primary_role = user_context.get("primary_role") or "Software Engineer"
        location = user_context.get("location_preference") or "Remote"

        try:
            # Run in thread pool with strict timeout
            raw_results = await asyncio.wait_for(
                asyncio.to_thread(_run_jobspy_sync, primary_role, location, 15),
                timeout=JOBSPY_TIMEOUT,
            )

            unified_jobs: list[UnifiedJob] = []
            for item in raw_results:
                job_id = f"jobspy_{hash((item['company'], item['title'], item['apply_url'])) & 0xFFFFFFFF:08x}"
                unified_jobs.append(
                    UnifiedJob(
                        id=job_id,
                        company=item["company"],
                        title=item["title"],
                        location=item["location"],
                        apply_url=item["apply_url"],
                        source=f"JobSpy ({item.get('site', 'LinkedIn/Indeed')})",
                        posted_at=item.get("date_posted") or None,
                    )
                )

            logger.info("✅ [JobSpy Adapter] Fetched %d jobs", len(unified_jobs))
            return unified_jobs

        except asyncio.TimeoutError:
            logger.warning("⏳ [JobSpy Adapter] Timed out after %.1fs — degrading gracefully", JOBSPY_TIMEOUT)
            return []
        except Exception as e:
            logger.warning("⚠️ [JobSpy Adapter] Fetch error: %s", e)
            return []
