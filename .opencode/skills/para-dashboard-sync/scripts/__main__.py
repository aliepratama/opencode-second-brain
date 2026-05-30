"""Sync Dashboard.md counts and tables with actual vault contents.

Usage:
    python -m scripts .opencode/skills/para-dashboard-sync [--dry-run]
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

VAULT_ROOT = None


def _find_vault_root():
    global VAULT_ROOT
    current = Path(os.getcwd())
    for parent in [current, *current.parents]:
        if (parent / "AGENTS.md").exists():
            VAULT_ROOT = parent
            return
    raise SystemExit("ERROR: AGENTS.md not found. Run from inside a second brain vault.")


def _find_shared():
    skill_dir = Path(__file__).resolve().parent.parent
    shared = skill_dir.parent / "_shared"
    sys.path.insert(0, str(shared.parent))


def _count_files(folder: str) -> int:
    d = VAULT_ROOT / folder
    if not d.exists():
        return 0
    return len([f for f in d.glob("*.md") if f.name != ".gitkeep"])


def _count_projects_by_status() -> dict:
    counts = {"active": 0, "on-hold": 0, "done": 0}
    d = VAULT_ROOT / "projects"
    if not d.exists():
        return counts
    for f in d.glob("*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            m = re.search(r"^status:\s*(\S+)", text, re.MULTILINE)
            if m:
                status = m.group(1).strip()
                if status in counts:
                    counts[status] += 1
        except Exception:
            continue
    return counts


def _update_dashboard(counts: dict):
    path = VAULT_ROOT / "Dashboard.md"
    if not path.exists():
        print("WARNING: Dashboard.md not found.")
        return

    content = path.read_text(encoding="utf-8")
    today = date.today().strftime("%Y-%m-%d")

    # Update last updated
    content = re.sub(r"\*\*Last updated:\*\*.*", f"**Last updated:** {today}", content)

    # Update PARA Structure counts
    folder_counts = {
        "projects/": counts["active"],
        "areas/": _count_files("areas"),
        "resources/": _count_files("resources"),
        "archives/": _count_files("archives"),
        "daily/": _count_files("daily"),
        "weekly/": _count_files("weekly"),
    }

    # Simple placeholder count updates
    for folder, count in folder_counts.items():
        unit = "active" if folder == "projects/" else "areas" if folder == "areas/" else \
               "resources" if folder == "resources/" else "archived" if folder == "archives/" else \
               "entries" if folder == "daily/" else "entries"
        pattern = rf"(\[\[{re.escape(folder)}\]\].*\|)\s*\d+\s+{unit}"
        replacement = rf"\1 {count} {unit}"
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
        else:
            pattern2 = rf"(\[\[{re.escape(folder)}\]\].*\|)\s*\S+"
            replacement2 = rf"\1 {count} {unit}"
            content = re.sub(pattern2, replacement2, content)

    # Update templates count
    template_count = _count_files("templates")
    content = re.sub(
        r"(\[\[templates/\S*\|?.*\]\].*\|)\s*\S+",
        rf"\1 {template_count} templates",
        content
    )

    # Update recent activity
    daily_files = sorted(
        [f for f in (VAULT_ROOT / "daily").glob("*.md") if f.name != ".gitkeep"],
        key=lambda p: p.stat().st_mtime, reverse=True
    )
    recent_lines = []
    for f in daily_files[:5]:
        recent_lines.append(f"| {f.stem} | — |")
    if recent_lines:
        activity_section = "| Date | Highlights |\n|------|-----------|\n" + "\n".join(recent_lines)
        content = re.sub(
            r"\| Date \| Highlights \|\s*\n\|------\|-----------\|\s*\n(\| .*? \| .*? \|\s*\n)*",
            activity_section + "\n",
            content
        )

    path.write_text(content, encoding="utf-8")

    print(f"Dashboard.md updated ({today})")
    status_counts = _count_projects_by_status()
    total_projects = sum(status_counts.values())
    print(f"  Active projects: {status_counts['active']} (total: {total_projects})")
    print(f"  Areas: {_count_files('areas')}")
    print(f"  Resources: {_count_files('resources')}")
    print(f"  Archived: {_count_files('archives')}")
    print(f"  Daily logs: {_count_files('daily')}")
    print(f"  Weekly reviews: {_count_files('weekly')}")


def main():
    _find_vault_root()
    _find_shared()

    dry_run = "--dry-run" in sys.argv
    counts = _count_projects_by_status()

    if dry_run:
        print("[Dry run] Dashboard would be updated with:")
        print(f"  Active projects: {counts['active']}")
        print(f"  On-hold projects: {counts['on-hold']}")
        print(f"  Done projects: {counts['done']}")
        print("Run without --dry-run to execute.")
        return

    _update_dashboard(counts)


if __name__ == "__main__":
    main()
