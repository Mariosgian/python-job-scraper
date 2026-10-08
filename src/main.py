"""CLI entry point."""
import asyncio
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from .models import SearchConfig
from .scraper import run_search
from .database import save_listings, get_cached_listings, clear_cache
from .exporter import export

app = typer.Typer(name="job-scraper", help="Async job & internship scraper.", add_completion=False)
console = Console()

@app.command()
def search(
    keywords: list[str] = typer.Option(..., "--keywords", "-k"),
    location: Optional[str] = typer.Option(None, "--location", "-l"),
    min_salary: Optional[int] = typer.Option(None, "--min-salary"),
    paid_only: bool = typer.Option(False, "--paid-only"),
    export_fmt: Optional[str] = typer.Option(None, "--export"),
    use_cache: bool = typer.Option(True, "--cache/--no-cache"),
) -> None:
    """Search for internships and jobs."""
    config = SearchConfig(keywords=keywords, location=location, min_salary=min_salary, paid_only=paid_only)
    console.print(f"\n[bold blue]Searching:[/] {', '.join(keywords)}")
    listings = asyncio.run(run_search(config))
    save_listings(listings)
    if not listings:
        console.print("[yellow]No listings found.[/yellow]")
        raise typer.Exit()
    table = Table(show_header=True, header_style="bold blue", box=None)
    for col in ["Title", "Company", "Location", "Salary", "Duration", "Remote"]:
        table.add_column(col)
    for l in listings:
        table.add_row(l.title, l.company, l.location, l.salary_display,
            f"{l.duration_months}mo" if l.duration_months else "–", "✓" if l.is_remote else "–")
    console.print(f"\n[bold green]Found {len(listings)} listings[/bold green]\n")
    console.print(table)
    if export_fmt in ("csv", "json"):
        path = export(listings, fmt=export_fmt)
        console.print(f"\n[green]✓ Exported to {path}[/green]")

@app.command()
def cache(action: str = typer.Argument("list")) -> None:
    """Manage the local cache (list or clear)."""
    if action == "clear":
        console.print(f"[red]Cleared {clear_cache()} listings.[/red]")
    else:
        console.print(f"[blue]{len(get_cached_listings())} listings in cache.[/blue]")

if __name__ == "__main__":
    app()
