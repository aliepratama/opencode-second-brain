"""Create an Architecture Decision Record from template.

Usage:
    python -m scripts .opencode/skills/para-adr "Decision Title" [--status proposed]
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


def _get_next_number() -> int:
    adrs_dir = VAULT_ROOT / "adrs"
    if not adrs_dir.exists():
        return 1
    existing = [f.stem for f in adrs_dir.glob("*.md") if f.name != ".gitkeep"]
    if not existing:
        return 1
    numbers = []
    for name in existing:
        match = re.match(r"^(\d+)", name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) + 1 if numbers else 1


def _sanitize_title(title: str) -> str:
    return title.lower().replace(" ", "-").replace("_", "-").strip("-")[:60]


def main():
    _find_vault_root()

    args = sys.argv[1:]
    if not args:
        raise SystemExit("Usage: python -m scripts <skill-dir> 'Title of decision' [--status proposed|accepted]")

    title = args[0]
    status = "proposed"
    if "--status" in args:
        idx = args.index("--status")
        if idx + 1 < len(args):
            status = args[idx + 1]

    num = _get_next_number()
    slug = _sanitize_title(title)
    filename = f"{num:04d}-{slug}.md"
    filepath = VAULT_ROOT / "adrs" / filename

    # Find template
    template_path = VAULT_ROOT / "templates" / "_adr.md"
    if not template_path.exists():
        # Try editions/dev/templates
        template_path = VAULT_ROOT / "editions" / "dev" / "templates" / "_adr.md"
    if not template_path.exists():
        raise SystemExit("ERROR: _adr.md template not found in templates/")

    content = template_path.read_text(encoding="utf-8")
    today = date.today().strftime("%Y-%m-%d")

    content = content.replace("{{date:YYYY-MM-DD}}", today)
    content = content.replace("{{number}}", str(num))
    content = content.replace("{{title}}", title)
    content = content.replace("status: proposed  # proposed | accepted | deprecated | superseded",
                              f"status: {status}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: adrs/{filename}")
    print(f"  Number: {num:04d}")
    print(f"  Status: {status}")
    print(f"  Date: {today}")
    print()
    print("Next: fill in Context & Options sections, then link from your project brief.")


if __name__ == "__main__":
    main()
