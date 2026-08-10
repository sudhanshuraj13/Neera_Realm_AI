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


async def fetch_global_startup_jobs(
    client: httpx.AsyncClient, query_role: str = ""
) -> list[JobListing]:
    """
    Fetch open job listings from global startup & tech job aggregators (Remotive & Arbeitnow).
    Requires no API keys; searches live startup opportunities worldwide.
    """
    jobs: list[JobListing] = []

    # 1. Remotive Public Startup & Remote Jobs API
    remotive_url = "https://remotive.com/api/remote-jobs?limit=40"
    try:
        resp = await client.get(remotive_url)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("jobs", []):
                company = item.get("company_name", "Startup")
                title = item.get("title", "Software Engineer")
                location = item.get("candidate_required_location", "Remote")
                apply_url = item.get("url", "")

                jobs.append(
                    JobListing(
                        company=company,
                        title=title,
                        location=location or "Remote",
                        apply_url=apply_url or "https://remotive.com",
                    )
                )
            logger.info("🚀 Remotive Global Startups: fetched %d jobs", len(jobs))
    except Exception as e:
        logger.warning("⚠️ Remotive fetch error: %s", e)

    # 2. Arbeitnow Public Tech Job Board API
    arbeitnow_url = "https://www.arbeitnow.com/api/job-board-api"
    try:
        resp = await client.get(arbeitnow_url)
        if resp.status_code == 200:
            data = resp.json()
            count = 0
            for item in data.get("data", []):
                company = item.get("company_name", "Tech Startup")
                title = item.get("title", "Developer")
                location = item.get("location", "Remote / Flexible")
                apply_url = item.get("url", "")

                jobs.append(
                    JobListing(
                        company=company,
                        title=title,
                        location=location or "Remote",
                        apply_url=apply_url or "https://www.arbeitnow.com",
                    )
                )
                count += 1
                if count >= 30:
                    break
            logger.info("🌐 Arbeitnow Tech Jobs: fetched %d jobs", count)
    except Exception as e:
        logger.warning("⚠️ Arbeitnow fetch error: %s", e)

    return jobs


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------


async def fetch_all_jobs(
    company_slugs: list[str] | None = None,
    include_global_startups: bool = True,
) -> list[JobListing]:
    """
    Fetch jobs from target dream companies (Greenhouse, Lever, Ashby)
    plus global startup job boards (Remotive, Arbeitnow).

    Args:
        company_slugs: Custom target/dream companies specified by the user
        include_global_startups: Whether to scan global startup job boards

    Returns:
        Combined, deduplicated list of JobListing objects.
    """
    slugs = company_slugs or []
    logger.info("🔍 Fetching jobs — target_companies=%s, global_startups=%s", slugs, include_global_startups)

    all_jobs: list[JobListing] = []

    async with httpx.AsyncClient(timeout=ATS_TIMEOUT) as client:
        tasks = []

        # Target dream companies specified by user
        for slug in slugs:
            clean_slug = slug.strip().lower().replace(" ", "")
            if clean_slug:
                tasks.append(fetch_greenhouse_jobs(client, clean_slug))
                tasks.append(fetch_lever_jobs(client, clean_slug))
                tasks.append(fetch_ashby_jobs(client, clean_slug))

        # Global startup job boards
        if include_global_startups:
            tasks.append(fetch_global_startup_jobs(client))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.warning("⚠️ ATS fetch task failed: %s", result)
                continue
            if isinstance(result, list):
                all_jobs.extend(result)

    logger.info("✅ Total jobs fetched: %d across target companies & global startup boards", len(all_jobs))
    return all_jobs
