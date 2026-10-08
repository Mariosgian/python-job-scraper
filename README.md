# 🔍 Job Scraper & Tracker

A Python CLI tool that scrapes internship and job listings from multiple sources, filters them by keywords, and exports structured results to CSV or JSON. Built with async HTTP requests and BeautifulSoup.

## Features

- 🚀 Async scraping with `httpx` — fast parallel requests
- 🔎 Keyword filtering (role, location, salary, duration)
- 📊 Export to CSV or JSON
- 💾 Local SQLite cache — don't re-scrape what you already have
- 🎨 Rich CLI output with progress bars and color
- ✅ Fully typed with Python type hints

## Demo

```bash
$ python -m src.main search --keywords "python developer" --location "Berlin" --export csv

  Searching for: python developer in Berlin
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:03

  Found 24 listings
  ✓ Exported to data/results_2027-01-15.csv
```

## Tech Stack

- Python 3.11+
- `httpx` — async HTTP client
- `BeautifulSoup4` — HTML parsing
- `rich` — CLI output
- `sqlite3` — built-in caching layer
- `typer` — CLI framework
- `pydantic` — data validation

## Installation

```bash
git clone https://github.com/Mariosgian/python-job-scraper
cd python-job-scraper
pip install -r requirements.txt
python -m src.main --help
```

## Usage

```bash
# Search listings
python -m src.main search --keywords "web developer" --location "remote"

# Search with salary filter
python -m src.main search --keywords "python" --min-salary 800

# Export to JSON
python -m src.main search --keywords "frontend" --export json

# Clear cache
python -m src.main cache clear

# View cached results
python -m src.main cache list
```

## Project Structure

```
python-job-scraper/
├── src/
│   ├── __init__.py
│   ├── main.py          # CLI entry point (typer)
│   ├── scraper.py       # Async scraping logic
│   ├── parser.py        # HTML parsing with BS4
│   ├── models.py        # Pydantic data models
│   ├── database.py      # SQLite cache layer
│   └── exporter.py      # CSV/JSON export
├── tests/
│   ├── test_parser.py
│   ├── test_models.py
│   └── test_exporter.py
├── data/                # Output files (gitignored)
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Author

**Marios Giannoulis** — [mariosgian.com](https://mariosgian.com)
