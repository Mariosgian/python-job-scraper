"""SQLite cache layer for job listings."""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from .models import JobListing

DB_PATH = Path("data/cache.db")

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                currency TEXT DEFAULT 'EUR',
                duration_months INTEGER,
                is_paid INTEGER DEFAULT 1,
                is_remote INTEGER DEFAULT 0,
                source TEXT NOT NULL,
                scraped_at TEXT NOT NULL,
                tags TEXT DEFAULT '[]'
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_scraped_at ON listings(scraped_at)")
        conn.commit()

def save_listings(listings: list[JobListing]) -> int:
    init_db()
    inserted = 0
    with get_connection() as conn:
        for listing in listings:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO listings
                    (id, title, company, location, url, description,
                     salary_min, salary_max, currency, duration_months,
                     is_paid, is_remote, source, scraped_at, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    listing.id, listing.title, listing.company,
                    listing.location, listing.url, listing.description,
                    listing.salary_min, listing.salary_max, listing.currency,
                    listing.duration_months, int(listing.is_paid),
                    int(listing.is_remote), listing.source,
                    listing.scraped_at.isoformat(), json.dumps(listing.tags),
                ))
                inserted += conn.execute("SELECT changes()").fetchone()[0]
            except sqlite3.Error:
                continue
        conn.commit()
    return inserted

def get_cached_listings(max_age_hours: int = 24) -> list[JobListing]:
    init_db()
    cutoff = (datetime.now() - timedelta(hours=max_age_hours)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM listings WHERE scraped_at > ? ORDER BY scraped_at DESC",
            (cutoff,)
        ).fetchall()
    listings = []
    for row in rows:
        try:
            listings.append(JobListing(
                id=row["id"], title=row["title"], company=row["company"],
                location=row["location"], url=row["url"],
                description=row["description"], salary_min=row["salary_min"],
                salary_max=row["salary_max"], currency=row["currency"],
                duration_months=row["duration_months"],
                is_paid=bool(row["is_paid"]), is_remote=bool(row["is_remote"]),
                source=row["source"],
                scraped_at=datetime.fromisoformat(row["scraped_at"]),
                tags=json.loads(row["tags"]),
            ))
        except Exception:
            continue
    return listings

def clear_cache() -> int:
    init_db()
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
        conn.execute("DELETE FROM listings")
        conn.commit()
    return count
