"""Generate a weekly review by aggregating daily logs.

Usage:
    python -m scripts .opencode/skills/para-weekly-review
"""

import os
import re
import sys
from datetime import date, timedelta
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


def _get_week_range():
    import datetime
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def _iso_week(d: date) -> str:
    iso = d.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def _find_dailies(monday: date, sunday: date) -> list[Path]:
    daily_dir = VAULT_ROOT / "daily"
    files = []
    current = monday
    while current <= sunday:
        f = daily_dir / f"{current.strftime('%Y-%m-%d')}.md"
        if f.exists():
            files.append(f)
        current += timedelta(days=1)
    return files


def _extract_section(content: str, heading: str) -> list[str]:
    pattern = rf"##\s+{heading}\s*\n(.*?)(?=\n## |\n---|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    lines = match.group(1).strip().split("\n")
    return [l.strip("- ").strip() for l in lines if l.strip().startswith("-") and l.strip("- ").strip()]


def _extract_checklist_items(content: str, heading: str, checked: bool = False) -> list[str]:
    prefix = "- [x]" if checked else "- [ ]"
    pattern = rf"##\s+{heading}\s*\n(.*?)(?=\n## |\n---|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    lines = match.group(1).split("\n")
    items = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            items.append(stripped[5:].strip())
    return items


def _load_template() -> str:
    path = VAULT_ROOT / "templates" / "_weekly-review.md"
    if not path.exists():
        raise SystemExit(f"ERROR: Template not found: {path}")
    return path.read_text(encoding="utf-8")


def main():
    _find_vault_root()
    _find_shared()

    monday, sunday = _get_week_range()
    week_str = _iso_week(monday)
    filepath = VAULT_ROOT / "weekly" / f"{week_str}.md"

    if filepath.exists():
        print(f"Weekly review already exists: weekly/{week_str}.md")
        return

    dailies = _find_dailies(monday, sunday)
    if not dailies:
        print(f"No daily logs found for {monday} to {sunday}")
        return

    # Aggregate all sections
    all_progress = []
    all_blockers = []
    all_insights = []
    all_completed = []
    all_pending = []
    blocker_counts = {}

    for f in dailies:
        content = f.read_text(encoding="utf-8")
        day_label = f.stem
        for item in _extract_section(content, "Progress"):
            if item:
                all_progress.append(f"- {item} ({day_label})")
        for item in _extract_section(content, "Blockers"):
            if item:
                all_blockers.append(f"- {item} ({day_label})")
                blocker_counts[item] = blocker_counts.get(item, 0) + 1
        for item in _extract_section(content, "Insights"):
            if item:
                all_insights.append(f"- {item} ({day_label})")
        for item in _extract_checklist_items(content, "Daily Summary|Completed", checked=True):
            if item:
                all_completed.append(f"- [x] {item}")
        for item in _extract_checklist_items(content, "Daily Summary|In Progress", checked=False):
            if item:
                all_pending.append(f"- [ ] {item}")

    # Detect recurring blockers (3+ days)
    recurring = [f"- ⚠️ RECURRING: {k} ({v} days)" for k, v in blocker_counts.items() if v >= 3]

    # Load and populate template
    template = _load_template()
    content = template.replace(
        "{{date:YYYY-MM-DD}} to {{monday:YYYY-MM-DD}}",
        f"{sunday.strftime('%Y-%m-%d')} to {monday.strftime('%Y-%m-%d')}"
    )

    content = content.replace("## Accomplished\n\n<!-- What got done this week -->\n\n- ",
                              f"## Accomplished\n\n<!-- What got done this week -->\n\n{chr(10).join(all_progress[:15])}\n- ")
    content = content.replace("## On Hold / Blocked\n\n<!-- Stalled and why -->\n\n- ",
                              f"## On Hold / Blocked\n\n<!-- Stalled and why -->\n\n{chr(10).join(all_blockers[:10])}\n{chr(10).join(recurring)}\n- ")
    content = content.replace("## Insights & Patterns\n\n<!-- Recurring patterns, efficiencies, problems that came up again -->\n\n- ",
                              f"## Insights & Patterns\n\n<!-- Recurring patterns, efficiencies, problems that came up again -->\n\n{chr(10).join(all_insights[:10])}\n- ")

    # Add aggregated summary
    summary = f"\n\n## Aggregated Summary\n\n### Completed This Week\n{chr(10).join(all_completed[:20])}\n\n### Still Pending\n{chr(10).join(all_pending[:20])}\n"
    content += summary

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: weekly/{week_str}.md")
    print(f"  Week: {monday} to {sunday}")
    print(f"  Daily logs processed: {len(dailies)}")
    print(f"  Progress items: {len(all_progress)}")
    print(f"  Blockers: {len(all_blockers)}")
    if recurring:
        print(f"  ⚠️ Recurring blockers: {len(recurring)}")


if __name__ == "__main__":
    main()
