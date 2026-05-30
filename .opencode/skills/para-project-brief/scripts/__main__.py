"""Create a new project brief from template.

Usage:
    python -m scripts .opencode/skills/para-project-brief "project-name" [--status active] [--priority medium]
"""

import os
import shutil
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


def _sanitize_name(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-").strip("-")


def _parse_args():
    args = sys.argv[1:]
    if not args:
        raise SystemExit("Usage: python -m scripts <skill-dir> <project-name> [--status active] [--priority medium]")

    project_name = args[0]
    status = "active"
    priority = "Medium"

    i = 1
    while i < len(args):
        if args[i] == "--status" and i + 1 < len(args):
            status = args[i + 1]
            i += 2
        elif args[i] == "--priority" and i + 1 < len(args):
            priority = args[i + 1]
            i += 2
        else:
            i += 1

    return project_name, status.capitalize(), priority


def _priority_emoji(priority: str) -> str:
    p = priority.lower()
    if p in ("high", "critical", "p0", "p1"):
        return "🔴 High"
    elif p in ("medium", "normal", "p2"):
        return "🟡 Medium"
    else:
        return "🟢 Low"


def main():
    _find_vault_root()
    _find_shared()

    project_name, status, priority = _parse_args()
    slug = _sanitize_name(project_name)
    filepath = VAULT_ROOT / "projects" / f"{slug}.md"

    if filepath.exists():
        print(f"Project already exists: projects/{slug}.md")
        return

    template_path = VAULT_ROOT / "templates" / "_project-brief.md"
    if not template_path.exists():
        raise SystemExit(f"ERROR: Template not found: {template_path}")

    content = template_path.read_text(encoding="utf-8")
    today = date.today().strftime("%Y-%m-%d")

    content = content.replace("{{title}}", project_name)
    content = content.replace("{{date:YYYY-MM-DD}}", today)
    content = content.replace("status: active", f"status: {status.lower()}")
    content = content.replace("**Priority:** 🔴 High / 🟡 Medium / 🟢 Low", f"**Priority:** {_priority_emoji(priority)}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: projects/{slug}.md")
    print(f"  Status: {status.lower()}")
    print(f"  Priority: {priority}")
    print(f"  Started: {today}")
    print()
    print("Next steps:")
    print("  1. Fill in the Brief section")
    print("  2. Update Dashboard's Active Projects table")
    print("  3. Add a reference in today's daily log")
    print("  4. Run: python -m scripts .opencode/skills/para-dashboard-sync")


if __name__ == "__main__":
    main()
