"""Create today's daily log from template with auto-linking.

Usage:
    python -m scripts .opencode/skills/para-daily-log
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


def _find_shared():
    skill_dir = Path(__file__).resolve().parent.parent
    shared = skill_dir.parent / "_shared"
    sys.path.insert(0, str(shared.parent))


def _load_template() -> str:
    path = VAULT_ROOT / "templates" / "_daily-log.md"
    if not path.exists():
        raise SystemExit(f"ERROR: Template not found: {path}")
    return path.read_text(encoding="utf-8")


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


def _get_yesterday_next_actions() -> list[str]:
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


def main():
    _find_vault_root()
    _find_shared()

    today = date.today()
    filename = f"{today.strftime('%Y-%m-%d')}.md"
    filepath = VAULT_ROOT / "daily" / filename

    if filepath.exists():
        print(f"Daily log already exists: daily/{filename}")
        print("Open it in Obsidian or edit directly.")
        return

    template = _load_template()
    content = template.replace("{{date:YYYY-MM-DD}}", today.strftime("%Y-%m-%d"))
    content = content.replace("{{date:YYYY-MM}}", today.strftime("%Y-%m"))

    # Auto-link recent projects
    recent = _get_recent_projects()
    if recent:
        ref_line = "\n".join(f"- {r}" for r in recent)
        content = content.replace(
            "## References\n<!-- Link to project briefs, external resources -->\n\n- ",
            f"## References\n<!-- Link to project briefs, external resources -->\n\n{ref_line}\n- "
        )

    # Carry over yesterday's next actions
    yesterday_actions = _get_yesterday_next_actions()
    if yesterday_actions:
        na = "\n".join(yesterday_actions)
        content = content.replace(
            "## Next Actions\n<!-- For tomorrow / prioritized -->\n\n- [ ] ",
            f"## Next Actions\n<!-- For tomorrow / prioritized -->\n\n{na}\n- [ ] "
        )

    # Verify Daily Summary section exists
    if "## Daily Summary" not in content:
        content += "\n\n## Daily Summary\n\n### Completed\n- [x] \n\n### In Progress / Pending\n- [ ] \n"

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: daily/{filename}")
    print(f"  Tags: #daily/{today.strftime('%Y-%m')}")
    if recent:
        print(f"  Linked projects: {len(recent)}")


if __name__ == "__main__":
    main()
