"""Create a developer-focused daily log with commits, PRs, and code reviews.

Usage:
    python -m scripts .opencode/skills/para-dev-log
"""

import os
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


def _get_recent_projects(days: int = 3) -> list[str]:
    projects_dir = VAULT_ROOT / "projects"
    if not projects_dir.exists():
        return []
    cutoff = date.today() - timedelta(days=days)
    recent = []
    for f in sorted(projects_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        if f.name == ".gitkeep":
            continue
        mtime = date.fromtimestamp(f.stat().st_mtime)
        if mtime >= cutoff:
            recent.append(f"[[../projects/{f.stem}]]")
        if len(recent) >= 5:
            break
    return recent


def _get_recent_adrs(days: int = 7) -> list[str]:
    adrs_dir = VAULT_ROOT / "adrs"
    if not adrs_dir.exists():
        return []
    cutoff = date.today() - timedelta(days=days)
    recent = []
    for f in sorted(adrs_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        if f.name == ".gitkeep":
            continue
        mtime = date.fromtimestamp(f.stat().st_mtime)
        if mtime >= cutoff:
            recent.append(f"[[../adrs/{f.stem}]]")
        if len(recent) >= 3:
            break
    return recent


def _get_yesterday_actions() -> list[str]:
    yesterday = date.today() - timedelta(days=1)
    path = VAULT_ROOT / "daily" / f"{yesterday.strftime('%Y-%m-%d')}.md"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").split("\n")
    actions = []
    in_next = False
    for line in lines:
        if "Next Actions" in line:
            in_next = True
            continue
        if in_next:
            if line.strip().startswith("## ") or line.strip().startswith("---"):
                break
            if line.strip().startswith("- [ ]"):
                actions.append(line.strip())
    return actions


DEV_LOG_TEMPLATE = """# {date} — Dev Log
tags: #daily/{tag_month}

## Commits
<!-- `hash` type: short description → [[project]] -->
- 

## PRs
<!-- #N status: description -->
- 

## Code Reviews
<!-- [x] PR #N — notes -->
- [ ] 

## Progress
<!-- What got built today -->
- 

## Decisions
<!-- Architecture decisions made → [[../adrs/...]] -->
- 

## Bugs
<!-- Bugs found or fixed → [[../errors/...]] -->
- 

## Blockers
<!-- Anything holding things up -->
- 

## Insights
<!-- Lessons, discoveries, patterns -->
- 

## References
<!-- Links to projects, ADRs, snippets, resources -->
{references}

## Next Actions
<!-- For tomorrow, prioritized -->
{yesterday_actions}
- [ ] 

---

## Daily Summary

### Completed
- [x] 
- [x] 

### In Progress / Pending
- [ ] 
- [ ] 

---

**Energy:** 🙂 / 😐 / 😫 &nbsp;&nbsp; **Focus:** 🎯 / 🌀 / 🌊
"""


def main():
    _find_vault_root()

    today = date.today()
    filename = f"{today.strftime('%Y-%m-%d')}.md"
    filepath = VAULT_ROOT / "daily" / filename

    if filepath.exists():
        print(f"Daily dev log already exists: daily/{filename}")
        return

    recent_projects = _get_recent_projects()
    recent_adrs = _get_recent_adrs()
    yesterday_actions = _get_yesterday_actions()

    refs = []
    for p in recent_projects:
        refs.append(f"- {p}")
    for a in recent_adrs:
        refs.append(f"- {a}")

    references = "\n".join(refs) if refs else "- "
    yesterday = "\n".join(yesterday_actions) + "\n" if yesterday_actions else ""

    content = DEV_LOG_TEMPLATE.format(
        date=today.strftime("%Y-%m-%d"),
        tag_month=today.strftime("%Y-%m"),
        references=references,
        yesterday_actions=yesterday,
    )

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: daily/{filename}")
    print(f"  Tags: #daily/{today.strftime('%Y-%m')}")
    if recent_projects:
        print(f"  Linked projects: {len(recent_projects)}")
    if recent_adrs:
        print(f"  Linked ADRs: {len(recent_adrs)}")
    print()
    print("Fill in: Commits, PRs, Code Reviews, Progress, Decisions, Bugs.")


if __name__ == "__main__":
    main()
