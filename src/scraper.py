"""Async HTTP scraping logic."""
import asyncio
import hashlib
import re
from typing import Optional
import httpx
from .models import JobListing, SearchConfig

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = httpx.Timeout(10.0, connect=5.0)

def _make_id(title: str, company: str, source: str) -> str:
    raw = f"{title}{company}{source}".lower()
    return hashlib.md5(raw.encode()).hexdigest()[:16]

async def _fetch(client: httpx.AsyncClient, url: str) -> Optional[str]:
    try:
        response = await client.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except (httpx.HTTPError, httpx.TimeoutException):
        return None

async def scrape_mock(config: SearchConfig) -> list[JobListing]:
    """Mock scraper returning realistic sample data.
    Replace _fetch() calls here with real scraping logic for production."""
    await asyncio.sleep(0.3)
    mock_data = [
        {"title": "Frontend Developer Intern", "company": "TechStartup GmbH",
         "location": "Berlin, Germany", "salary_min": 800, "salary_max": 1200,
         "duration_months": 6, "is_paid": True, "is_remote": False,
         "tags": ["react", "typescript", "frontend"], "url": "https://example.com/1", "source": "mock"},
        {"title": "Python Data Engineer Intern", "company": "EnergyTech",
         "location": "Munich, Germany", "salary_min": 900, "salary_max": 1100,
         "duration_months": 3, "is_paid": True, "is_remote": True,
         "tags": ["python", "data", "etl", "devops"], "url": "https://example.com/2", "source": "mock"},
        {"title": "Full Stack Developer Traineeship", "company": "Apollo Green",
         "location": "Athens, Greece", "salary_min": None, "salary_max": None,
         "duration_months": 4, "is_paid": False, "is_remote": True,
         "tags": ["nextjs", "typescript", "tailwind"], "url": "https://example.com/3", "source": "mock"},
    ]
    listings = []
    for item in mock_data:
        listing = JobListing(id=_make_id(item["title"], item["company"], item["source"]), **item)
        if listing.matches_keywords(config.keywords):
            if config.location is None or config.location.lower() in listing.location.lower():
                if not config.paid_only or listing.is_paid:
                    listings.append(listing)
    return listings

async def run_search(config: SearchConfig) -> list[JobListing]:
    async with httpx.AsyncClient() as client:
        return await scrape_mock(config)
