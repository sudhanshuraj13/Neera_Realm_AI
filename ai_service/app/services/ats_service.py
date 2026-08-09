"""
ATS Job Fetcher Service.

Fetches jobs from public ATS JSON endpoints (no scraping) and normalizes them
into a unified JobListing schema. Supports Greenhouse, Lever, and Ashby.

Usage:
    from app.services.ats_service import fetch_all_jobs
    jobs = await fetch_all_jobs(["stripe", "openai", "vercel", "notion"])
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from app.schemas.job_listing import JobListing

logger = logging.getLogger("neera_ai_service.ats_service")

# Shared timeout for all ATS API calls
ATS_TIMEOUT = 15.0


# ---------------------------------------------------------------------------
# Provider-specific fetchers
# ---------------------------------------------------------------------------


async def fetch_greenhouse_jobs(
    client: httpx.AsyncClient, company_slug: str
) -> list[JobListing]:
    """
    Fetch jobs from the Greenhouse boards API.

    Endpoint: GET https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    try:
        resp = await client.get(url, params={"content": "true"})
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()

        jobs: list[JobListing] = []
        for job in data.get("jobs", []):
            location_name = ""
            if job.get("location"):
                location_name = job["location"].get("name", "")

            absolute_url = job.get("absolute_url", "")

            jobs.append(
                JobListing(
                    company=company_slug,
                    title=job.get("title", "Unknown"),
                    location=location_name or "Not specified",
                    apply_url=absolute_url or f"https://boards.greenhouse.io/{company_slug}",
                )
            )

        logger.info("🌿 Greenhouse [%s]: fetched %d jobs", company_slug, len(jobs))
        return jobs

    except httpx.HTTPStatusError as e:
        logger.warning("⚠️ Greenhouse [%s]: HTTP %d", company_slug, e.response.status_code)
        return []
    except Exception as e:
        logger.warning("⚠️ Greenhouse [%s]: %s", company_slug, e)
        return []


async def fetch_lever_jobs(
    client: httpx.AsyncClient, company_slug: str
) -> list[JobListing]:
    """
    Fetch jobs from the Lever postings API.

    Endpoint: GET https://api.lever.co/v0/postings/{slug}?mode=json
    """
    url = f"https://api.lever.co/v0/postings/{company_slug}"
    try:
        resp = await client.get(url, params={"mode": "json"})
        resp.raise_for_status()
        postings: list[dict[str, Any]] = resp.json()

        jobs: list[JobListing] = []
        for posting in postings:
            categories = posting.get("categories", {})
            location = categories.get("location", "") or posting.get("workplaceType", "")

            jobs.append(
                JobListing(
                    company=company_slug,
                    title=posting.get("text", "Unknown"),
                    location=location or "Not specified",
                    apply_url=posting.get("hostedUrl", "") or posting.get("applyUrl", ""),
                )
            )

        logger.info("🔵 Lever [%s]: fetched %d jobs", company_slug, len(jobs))
        return jobs

    except httpx.HTTPStatusError as e:
        logger.warning("⚠️ Lever [%s]: HTTP %d", company_slug, e.response.status_code)
        return []
    except Exception as e:
        logger.warning("⚠️ Lever [%s]: %s", company_slug, e)
        return []


async def fetch_ashby_jobs(
    client: httpx.AsyncClient, company_slug: str
) -> list[JobListing]:
    """
    Fetch jobs from the Ashby posting API.

    Endpoint: GET https://api.ashbyhq.com/posting-api/job-board/{slug}
    """
    url = f"https://api.ashbyhq.com/posting-api/job-board/{company_slug}"
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()

        jobs: list[JobListing] = []
        for job in data.get("jobs", []):
            location = job.get("location", "")
            if isinstance(location, dict):
                location = location.get("name", "Not specified")

            apply_url = job.get("applyUrl", "") or job.get("jobUrl", "")
            if not apply_url:
                apply_url = f"https://jobs.ashbyhq.com/{company_slug}"

            jobs.append(
                JobListing(
                    company=company_slug,
                    title=job.get("title", "Unknown"),
                    location=location or "Not specified",
                    apply_url=apply_url,
                )
            )

        logger.info("🟣 Ashby [%s]: fetched %d jobs", company_slug, len(jobs))
        return jobs

    except httpx.HTTPStatusError as e:
        logger.warning("⚠️ Ashby [%s]: HTTP %d", company_slug, e.response.status_code)
        return []
    except Exception as e:
        logger.warning("⚠️ Ashby [%s]: %s", company_slug, e)
        return []


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------


async def fetch_all_jobs(company_slugs: list[str]) -> list[JobListing]:
    """
    Fetch jobs from all ATS providers for the given company slugs.

    Hits Greenhouse, Lever, and Ashby in parallel for each company.
    Failed requests are logged and silently skipped — partial results
    are always returned.

    Args:
        company_slugs: List of company slugs (e.g. ['stripe', 'openai', 'vercel', 'notion']).

    Returns:
        Combined, deduplicated list of JobListing objects.
    """
    logger.info("🔍 Fetching jobs for %d companies: %s", len(company_slugs), company_slugs)

    all_jobs: list[JobListing] = []

    async with httpx.AsyncClient(timeout=ATS_TIMEOUT) as client:
        tasks = []
        for slug in company_slugs:
            tasks.append(fetch_greenhouse_jobs(client, slug))
            tasks.append(fetch_lever_jobs(client, slug))
            tasks.append(fetch_ashby_jobs(client, slug))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.warning("⚠️ ATS fetch task failed: %s", result)
                continue
            if isinstance(result, list):
                all_jobs.extend(result)

    logger.info("✅ Total jobs fetched: %d across %d companies", len(all_jobs), len(company_slugs))
    return all_jobs
