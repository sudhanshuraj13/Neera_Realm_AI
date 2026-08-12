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


NON_IT_ENGINEERING_PHRASES: list[str] = [
    "mechanical engineer",
    "civil engineer",
    "chemical engineer",
    "aerospace engineer",
    "structural engineer",
    "industrial engineer",
    "biomedical engineer",
    "environmental engineer",
    "petroleum engineer",
    "materials engineer",
    "mining engineer",
    "marine engineer",
    "nuclear engineer",
    "audio engineer",
    "sound engineer",
]

IT_ROLE_KEYWORDS: list[str] = [
    "software",
    "developer",
    "fullstack",
    "full stack",
    "backend",
    "frontend",
    "web",
    "programmer",
    "coder",
    "devops",
    "cloud",
    "data scientist",
    "data engineer",
    "ai",
    "ml",
    "machine learning",
    "sre",
    "site reliability",
    "engineer",
]


def is_it_role(role: str) -> bool:
    """
    Check if a given role string explicitly contains IT-related keywords,
    excluding non-IT engineering roles like 'mechanical engineer' or 'civil engineer'.
    """
    if not role:
        return False
    role_lower = role.strip().lower()

    sanitized = role_lower
    for non_it in NON_IT_ENGINEERING_PHRASES:
        sanitized = sanitized.replace(non_it, "")

    return any(kw in sanitized for kw in IT_ROLE_KEYWORDS)


def is_job_title_matching(title: str, keywords: set[str]) -> bool:
    """
    Strictly filter job titles against user role keywords.

    1. Negative Filtering:
       If keywords do NOT contain IT/software terms, any job title containing
       'software', 'backend', 'frontend', 'fullstack', 'devops', etc. MUST BE DROPPED.
       If keywords do NOT contain 'sales', any job title containing 'sales' MUST BE DROPPED.

    2. Positive Filtering:
       The job title must contain at least one of the candidate's keywords.
    """
    if not title:
        return False
    if not keywords:
        return True

    title_lower = title.strip().lower()

    # 1. Negative Filtering (Domain exclusions)
    has_software_keywords = any(
        kw in " ".join(keywords)
        for kw in ["software", "developer", "backend", "frontend", "fullstack", "devops", "sre", "programmer", "coder", "systems engineer"]
    )
    if not has_software_keywords:
        software_terms = ["software", "backend", "frontend", "fullstack", "full-stack", "devops", "sre", "firmware"]
        if any(term in title_lower for term in software_terms):
            return False

    has_sales_keywords = any("sales" in kw for kw in keywords)
    if not has_sales_keywords:
        if "sales" in title_lower:
            return False

    # 2. Positive Keyword Matching
    return any(kw in title_lower for kw in keywords)


def build_role_keywords(
    primary_role: str = "",
    target_roles: list[str] | None = None,
    skills: list[str] | None = None,
) -> set[str]:
    """
    Build candidate-specific role search keywords without hardcoded software bias.
    Initializes an empty set and populates primary_role & target_roles.
    Derived software roles (Backend, AI, Frontend, etc.) are ONLY appended if the candidate's
    primary_role or target_roles explicitly contain IT-related keywords (excluding mechanical/civil engineers).
    """
    keywords: set[str] = set()
    all_candidate_roles: list[str] = []

    if primary_role:
        clean = primary_role.strip().lower()
        if clean:
            keywords.add(clean)
            all_candidate_roles.append(clean)
            for word in clean.split():
                if len(word) > 2 and word not in {"fresher", "junior", "senior", "lead", "principal", "staff"}:
                    keywords.add(word)

    if target_roles:
        for r in target_roles:
            clean = r.strip().lower()
            if clean:
                keywords.add(clean)
                all_candidate_roles.append(clean)
                for word in clean.split():
                    if len(word) > 2 and word not in {"fresher", "junior", "senior", "lead", "principal", "staff"}:
                        keywords.add(word)

    # ONLY append derived software roles IF candidate roles explicitly contain IT-related keywords
    is_it_candidate = any(is_it_role(r) for r in all_candidate_roles)

    if is_it_candidate:
        # Common baseline roles for IT candidates
        keywords.update({
            "software engineer",
            "software developer",
            "fullstack",
            "full stack",
            "developer",
            "engineer",
        })

        if skills:
            for skill in skills:
                sk_lower = skill.strip().lower()
                if any(term in sk_lower for term in ["ai", "ml", "artificial intelligence", "machine learning", "genai", "llm"]):
                    keywords.update({"ai", "ml", "ai engineer", "ai developer", "machine learning", "data scientist", "llm"})
                if any(term in sk_lower for term in ["backend", "api", "node", "python", "java", "golang", "postgres"]):
                    keywords.update({"backend", "backend engineer", "backend developer", "systems engineer"})
                if any(term in sk_lower for term in ["frontend", "react", "vue", "angular"]):
                    keywords.update({"frontend", "frontend engineer", "frontend developer", "web developer"})
                if any(term in sk_lower for term in ["cloud", "devops", "aws", "docker", "kubernetes"]):
                    keywords.update({"devops", "cloud engineer", "infrastructure", "site reliability"})
                if any(term in sk_lower for term in ["mobile", "flutter", "android", "ios", "react native"]):
                    keywords.update({"mobile", "android", "ios", "flutter", "react native"})

    return keywords


async def fetch_global_startup_jobs(
    client: httpx.AsyncClient,
    primary_role: str = "",
    target_roles: list[str] | None = None,
    skills: list[str] | None = None,
) -> list[JobListing]:
    """
    Fetch open job listings from global job aggregators (Remotive & Arbeitnow).
    Filters listings to match candidate's target roles and keywords.
    """
    jobs: list[JobListing] = []
    keywords = build_role_keywords(primary_role, target_roles, skills)

    # 1. Remotive Public Remote Jobs API
    remotive_url = "https://remotive.com/api/remote-jobs?limit=50"
    try:
        resp = await client.get(remotive_url)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("jobs", []):
                company = item.get("company_name", "Company")
                title = item.get("title", "Position")
                location = item.get("candidate_required_location", "Remote")
                apply_url = item.get("url", "")

                if is_job_title_matching(title, keywords):
                    jobs.append(
                        JobListing(
                            company=company,
                            title=title,
                            location=location or "Remote",
                            apply_url=apply_url or "https://remotive.com",
                        )
                    )
            logger.info("🚀 Remotive Global Jobs: fetched %d matched jobs", len(jobs))
    except Exception as e:
        logger.warning("⚠️ Remotive fetch error: %s", e)

    # 2. Arbeitnow Public Job Board API
    arbeitnow_url = "https://www.arbeitnow.com/api/job-board-api"
    try:
        resp = await client.get(arbeitnow_url)
        if resp.status_code == 200:
            data = resp.json()
            count = 0
            for item in data.get("data", []):
                company = item.get("company_name", "Company")
                title = item.get("title", "Position")
                location = item.get("location", "Remote / Flexible")
                apply_url = item.get("url", "")

                if is_job_title_matching(title, keywords):
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
            logger.info("🌐 Arbeitnow Jobs: fetched %d matched jobs", count)
    except Exception as e:
        logger.warning("⚠️ Arbeitnow fetch error: %s", e)

    return jobs


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------


async def fetch_all_jobs(
    company_slugs: list[str] | None = None,
    include_global_startups: bool = True,
    primary_role: str = "",
    target_roles: list[str] | None = None,
    skills: list[str] | None = None,
) -> list[JobListing]:
    """
    Fetch jobs from target dream companies (Greenhouse, Lever, Ashby)
    plus global job boards (Remotive, Arbeitnow).

    Args:
        company_slugs: Custom target/dream companies specified by the user
        include_global_startups: Whether to scan global startup job boards
        primary_role: Candidate primary role title
        target_roles: Candidate target roles
        skills: Candidate extracted skills

    Returns:
        Combined, deduplicated list of JobListing objects.
    """
    slugs = company_slugs or []
    logger.info(
        "🔍 Fetching jobs — target_companies=%s, primary_role='%s', skills=%s",
        slugs,
        primary_role,
        skills[:4] if skills else [],
    )

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

        # Global startup job boards with role & skill filtering
        if include_global_startups:
            tasks.append(
                fetch_global_startup_jobs(
                    client,
                    primary_role=primary_role,
                    target_roles=target_roles,
                    skills=skills,
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.warning("⚠️ ATS fetch task failed: %s", result)
                continue
            if isinstance(result, list):
                all_jobs.extend(result)

    keywords = build_role_keywords(primary_role, target_roles, skills)
    if keywords:
        filtered_jobs = [j for j in all_jobs if is_job_title_matching(j.title, keywords)]
        logger.info("🎯 Strict ATS job filtering: %d -> %d jobs matching keywords: %s", len(all_jobs), len(filtered_jobs), list(keywords)[:5])
        all_jobs = filtered_jobs

    logger.info("✅ Total jobs fetched: %d across target companies & global job boards", len(all_jobs))
    return all_jobs

