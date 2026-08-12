"""
Startup Funding Radar Ingestion Service.

Parses TechCrunch Startups RSS feed (articles from the last 48 hours),
uses Gemini / LLM to structure funding events into FundedStartup objects,
and returns candidate-relevant funding alerts for the Job Agent.
"""

from __future__ import annotations

import datetime
import logging
import re
import time
from typing import Any

import feedparser
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger("neera_ai_service.funding_service")

TECHCRUNCH_STARTUPS_RSS = "https://techcrunch.com/category/startups/feed/"
RSS_TIMEOUT = 10.0


class FundedStartupItem(BaseModel):
    id: str = Field(default="", description="Unique identifier or hash of source URL")
    company_name: str = Field(..., description="Name of the funded startup")
    amount_raised: str = Field(default="Undisclosed", description="Funding amount e.g. $20M")
    funding_stage: str = Field(default="Venture", description="Stage e.g. Seed, Series A, Series B")
    domain: str = Field(default="Tech", description="Industry domain e.g. AI/ML, FinTech, HealthTech, Robotics")
    summary: str = Field(..., description="1-sentence summary of the funding and hiring focus")
    careers_url: str | None = Field(default=None, description="Direct or inferred careers page link")
    source_url: str = Field(..., description="Original news article link")
    published_at: str = Field(default="", description="ISO timestamp")


def _is_within_hours(published_struct: time.struct_time | None, hours: int = 48) -> bool:
    """Check if an RSS item published struct_time is within the last N hours."""
    if not published_struct:
        return True  # Fallback to keep item if timestamp is missing
    try:
        pub_dt = datetime.datetime(*published_struct[:6], tzinfo=datetime.timezone.utc)
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        return (now_dt - pub_dt).total_seconds() <= (hours * 3600)
    except Exception:
        return True


def _extract_funding_from_title(title: str, summary_text: str, link: str) -> FundedStartupItem | None:
    """
    Deterministic rule-based extraction fallback for startup funding announcements.
    Matches patterns like 'Company raises $20M Series A' or 'Company closes $50M'.
    """
    text = f"{title} {summary_text}"

    # Search for dollar amounts e.g. $10M, $1.5M, $100 million
    amount_match = re.search(r"\$\d+(?:\.\d+)?\s*(?:M|million|B|billion|k|K)?", text, re.IGNORECASE)
    amount = amount_match.group(0) if amount_match else "Undisclosed"

    # Search for stage e.g. Seed, Series A, Series B, Series C
    stage_match = re.search(r"\b(Seed|Series\s+[A-E]|Series\s+Seed|Pre-seed|Venture|Growth)\b", text, re.IGNORECASE)
    stage = stage_match.group(0).title() if stage_match else "Funding Round"

    # Extract company name from title e.g. 'Cognition raises $175M' -> Cognition
    company = title.split(" raises ")[0].split(" secures ")[0].split(" nabs ")[0].split(" closes ")[0].strip()
    # Clean company name
    company = re.sub(r"^(TechCrunch|Exclusive:|\b[A-Z]{2,}\b:)\s*", "", company, flags=re.IGNORECASE).strip()
    if not company or len(company) > 40:
        company = title.split(":")[0].strip()

    # Determine domain from text
    domain = "Tech & Software"
    text_lower = text.lower()
    if any(k in text_lower for k in ["ai", "llm", "genai", "artificial intelligence", "machine learning"]):
        domain = "AI / Machine Learning"
    elif any(k in text_lower for k in ["fintech", "banking", "payments", "crypto"]):
        domain = "FinTech"
    elif any(k in text_lower for k in ["health", "biotech", "medical"]):
        domain = "HealthTech & Bio"
    elif any(k in text_lower for k in ["dev", "cloud", "infrastructure", "security"]):
        domain = "DevTools & Infrastructure"
    elif any(k in text_lower for k in ["design", "ui", "ux", "media"]):
        domain = "Design & Creative Tools"
    elif any(k in text_lower for k in ["robot", "auto", "vehicle", "hardware", "spatial"]):
        domain = "Robotics & Hardware"

    clean_summary = re.sub(r"<[^>]+>", "", summary_text).strip()
    if len(clean_summary) > 200:
        clean_summary = clean_summary[:197] + "..."

    item_id = f"fs_{hash(link) & 0xFFFFFFFF:08x}"

    return FundedStartupItem(
        id=item_id,
        company_name=company or "Stealth Startup",
        amount_raised=amount,
        funding_stage=stage,
        domain=domain,
        summary=clean_summary or title,
        careers_url=link,
        source_url=link,
    )


async def fetch_recent_funded_startups(hours: int = 48) -> list[FundedStartupItem]:
    """
    Fetch and parse TechCrunch Startups RSS feed.
    Filters stories published in the last N hours and extracts structured funding alerts.
    Gracefully degrades to an empty list on failure.
    """
    logger.info("📡 Scanning TechCrunch Startups RSS feed for recent funding alerts (last %dh)...", hours)
    startups: list[FundedStartupItem] = []

    try:
        async with httpx.AsyncClient(timeout=RSS_TIMEOUT, follow_redirects=True) as client:
            resp = await client.get(TECHCRUNCH_STARTUPS_RSS)
            if resp.status_code != 200:
                logger.warning("⚠️ RSS feed fetch returned HTTP %d", resp.status_code)
                return []

            feed = feedparser.parse(resp.content)
            entries = feed.get("entries", [])

            for entry in entries:
                published_struct = entry.get("published_parsed")
                if not _is_within_hours(published_struct, hours=hours):
                    continue

                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")

                # Only process articles mentioning funding/raising
                combined_lower = f"{title} {summary}".lower()
                if any(word in combined_lower for word in ["raise", "raises", "raised", "raising", "funding", "seed", "series", "secures", "nabs", "closes", "valuation", "million", "billion"]):
                    parsed_item = _extract_funding_from_title(title, summary, link)
                    if parsed_item:
                        startups.append(parsed_item)

            logger.info("✅ TechCrunch Ingestion: extracted %d recent funding radar items", len(startups))
            return startups

    except Exception as e:
        logger.warning("⚠️ Startup funding RSS ingestion failed gracefully: %s", e)
        return []
