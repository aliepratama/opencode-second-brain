"""Vault path utilities and file discovery."""

import os
from datetime import date, datetime, timedelta
from pathlib import Path


def get_vault_root(start: str | None = None) -> Path:
    """Find vault root by walking up until AGENTS.md is found."""
    current = Path(start or os.getcwd()).resolve()
    for parent in [current, *current.parents]:
        if (parent / "AGENTS.md").exists():
            return parent
    raise FileNotFoundError("AGENTS.md not found — not in a second brain vault")


def list_files(folder: str, pattern: str = "*.md", vault_root: str | None = None) -> list[Path]:
    """List all markdown files in a folder, sorted by modification time (newest first)."""
    root = Path(vault_root) if vault_root else get_vault_root()
    target = root / folder
    if not target.exists():
        return []
    files = sorted(target.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return [f for f in files if f.name != ".gitkeep"]


def get_recent_files(n: int = 5, folder: str = "projects", vault_root: str | None = None) -> list[Path]:
    """Get the n most recently modified files in a folder."""
    files = list_files(folder, vault_root=vault_root)
    return files[:n]


def today_daily_path(vault_root: str | None = None) -> Path:
    """Return the path to today's daily log."""
    root = Path(vault_root) if vault_root else get_vault_root()
    today = date.today().strftime("%Y-%m-%d")
    return root / "daily" / f"{today}.md"


def this_week_range() -> tuple[date, date]:
    """Return (monday, sunday) of the current ISO week."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def iso_week_string(d: date | None = None) -> str:
    """Return ISO week string like '2026-W22'."""
    d = d or date.today()
    iso = d.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def daily_files_in_range(start_date: date, end_date: date, vault_root: str | None = None) -> list[Path]:
    """Return daily log files within a date range (inclusive)."""
    root = Path(vault_root) if vault_root else get_vault_root()
    daily_dir = root / "daily"
    if not daily_dir.exists():
        return []

    files = []
    current = start_date
    while current <= end_date:
        f = daily_dir / f"{current.strftime('%Y-%m-%d')}.md"
        if f.exists():
            files.append(f)
        current += timedelta(days=1)
    return files
