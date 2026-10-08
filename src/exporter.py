"""Export job listings to CSV or JSON."""
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Literal
from .models import JobListing

OUTPUT_DIR = Path("data")

def export(listings: list[JobListing], fmt: Literal["csv", "json"] = "csv") -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = OUTPUT_DIR / f"results_{timestamp}.{fmt}"
    if fmt == "csv":
        fields = ["title", "company", "location", "salary_display", "duration_months", "is_paid", "is_remote", "source", "url"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for l in listings:
                writer.writerow({"title": l.title, "company": l.company, "location": l.location,
                    "salary_display": l.salary_display, "duration_months": l.duration_months or "N/A",
                    "is_paid": "Yes" if l.is_paid else "No", "is_remote": "Yes" if l.is_remote else "No",
                    "source": l.source, "url": l.url})
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([l.model_dump(mode="json") for l in listings], f, indent=2, default=str)
    return path
