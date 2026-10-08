"""Pydantic data models for job listings."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class JobListing(BaseModel):
    id: str
    title: str
    company: str
    location: str
    url: str
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: str = "EUR"
    duration_months: Optional[int] = None
    is_paid: bool = True
    is_remote: bool = False
    source: str
    scraped_at: datetime = datetime.now()
    tags: list[str] = []

    @field_validator("title", "company", "location")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("salary_min", "salary_max")
    @classmethod
    def validate_salary(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("Salary cannot be negative")
        return v

    @property
    def salary_display(self) -> str:
        if self.salary_min and self.salary_max:
            return f"{self.salary_min}–{self.salary_max} {self.currency}/month"
        if self.salary_min:
            return f"From {self.salary_min} {self.currency}/month"
        return "Unpaid" if not self.is_paid else "Not specified"

    def matches_keywords(self, keywords: list[str]) -> bool:
        text = f"{self.title} {self.description or ''} {' '.join(self.tags)}".lower()
        return any(kw.lower() in text for kw in keywords)


class SearchConfig(BaseModel):
    keywords: list[str]
    location: Optional[str] = None
    min_salary: Optional[int] = None
    paid_only: bool = False
    remote_only: bool = False
