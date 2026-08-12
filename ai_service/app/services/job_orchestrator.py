"""
Unified Job Orchestrator.

Concurrently executes multi-source job search adapters (ATS, JobSpy, Adzuna)
using asyncio.gather, flattens results, and deduplicates postings.
"""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Any

from app.schemas.jobs import UnifiedJob
from app.services.job_adapters import (
    AdzunaJobAdapter,
    ATSJobAdapter,
    JobSpyAdapter,
)

logger = logging.getLogger("neera_ai_service.job_orchestrator")


def _normalize_key(company: str, title: str) -> str:
    """Normalize company name and job title to create deduplication key."""
    clean_company = re.sub(r"[^\w\s]", "", company.lower()).strip()
    clean_title = re.sub(r"[^\w\s]", "", title.lower()).strip()
    return f"{clean_company}||{clean_title}"


async def fetch_all_jobs_concurrently(user_context: dict[str, Any]) -> list[UnifiedJob]:
    """
    Fetch job listings concurrently across all registered adapters.

    Args:
        user_context: Dictionary containing user preferences:
                      primary_role, target_roles, skills, location_preference, target_companies

    Returns:
        Flattened, deduplicated list of UnifiedJob instances.
    """
    primary_role = user_context.get("primary_role", "General")
    target_companies = user_context.get("target_companies") or []

    logger.info(
        "🚀 [Job Orchestrator] Starting concurrent job search — role='%s', target_companies=%s",
        primary_role,
        target_companies,
    )

    # Initialize adapters
    ats_adapter = ATSJobAdapter()
    jobspy_adapter = JobSpyAdapter()
    adzuna_adapter = AdzunaJobAdapter()

    # Build tasks list
    tasks = []

    # ATS adapter runs for target companies + global startup feeds
    tasks.append(ats_adapter.fetch_jobs(user_context))

    # JobSpy adapter runs LinkedIn/Indeed scraping
    tasks.append(jobspy_adapter.fetch_jobs(user_context))

    # Adzuna adapter runs free API/fallback
    tasks.append(adzuna_adapter.fetch_jobs(user_context))

    # Execute all adapters concurrently with defensive exception swallowing
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_jobs: list[UnifiedJob] = []

    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning("⚠️ [Job Orchestrator] Adapter task #%d failed: %s", idx, result)
            continue
        if isinstance(result, list):
            all_jobs.extend(result)

    # Deduplicate postings by normalized (company, title) key
    seen_keys: set[str] = set()
    deduped_jobs: list[UnifiedJob] = []

    for job in all_jobs:
        dedup_key = _normalize_key(job.company, job.title)
        if dedup_key not in seen_keys:
            seen_keys.add(dedup_key)
            deduped_jobs.append(job)

    logger.info(
        "✅ [Job Orchestrator] Completed multi-adapter fetch: %d raw -> %d deduplicated UnifiedJobs",
        len(all_jobs),
        len(deduped_jobs),
    )

    return deduped_jobs
