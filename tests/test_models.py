"""Tests for data models."""
import pytest
from src.models import JobListing

def make_listing(**kwargs) -> JobListing:
    return JobListing(**{"id": "abc123", "title": "Python Intern", "company": "TechCo",
        "location": "Berlin", "url": "https://example.com", "source": "test", "is_paid": True, **kwargs})

def test_creation():
    l = make_listing()
    assert l.title == "Python Intern"

def test_salary_display_range():
    l = make_listing(salary_min=800, salary_max=1200)
    assert "800" in l.salary_display and "1200" in l.salary_display

def test_salary_display_unpaid():
    assert make_listing(is_paid=False).salary_display == "Unpaid"

def test_matches_keywords():
    l = make_listing(title="React Frontend Developer", tags=["typescript"])
    assert l.matches_keywords(["react"])
    assert l.matches_keywords(["typescript"])
    assert not l.matches_keywords(["java"])

def test_strip_whitespace():
    l = make_listing(title="  Dev  ", company="  Co  ", location="  Berlin  ")
    assert l.title == "Dev" and l.company == "Co" and l.location == "Berlin"

def test_negative_salary_rejected():
    with pytest.raises(Exception):
        make_listing(salary_min=-100)
