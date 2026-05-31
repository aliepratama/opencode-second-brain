"""Create bug reports from template.

Usage:
    python -m scripts .opencode/skills/para-bug-tracker new "Memory leak" \
        --severity high --lang go --project "compiler"
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


def _sanitize_name(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-").strip("-")[:60]


def _parse_args(argv):
    result = {"severity": "medium", "lang": "", "project": ""}
    i = 2  # skip "new" and title positional
    while i < len(argv):
        if argv[i] == "--severity" and i + 1 < len(argv):
            result["severity"] = argv[i + 1]; i += 2
        elif argv[i] == "--lang" and i + 1 < len(argv):
            result["lang"] = argv[i + 1]; i += 2
        elif argv[i] == "--project" and i + 1 < len(argv):
            result["project"] = argv[i + 1]; i += 2
        else:
            i += 1
    return result


def main():
    _find_vault_root()

    argv = sys.argv[1:]
    if len(argv) < 2 or argv[0] != "new":
        raise SystemExit("Usage: python -m scripts <skill-dir> new 'Bug title' [--severity high] [--lang go] [--project name]")

    title = argv[1]
    kwargs = _parse_args(argv)
    slug = _sanitize_name(title)
    filename = f"{slug}.md"
    filepath = VAULT_ROOT / "errors" / filename

    if filepath.exists():
        print(f"Bug report already exists: errors/{filename}")
        return

    template_path = VAULT_ROOT / "templates" / "_bug-tracker.md"
    if not template_path.exists():
        template_path = VAULT_ROOT / "editions" / "dev" / "templates" / "_bug-tracker.md"
    if not template_path.exists():
        raise SystemExit("ERROR: _bug-tracker.md template not found")

    content = template_path.read_text(encoding="utf-8")
    today = date.today().strftime("%Y-%m-%d")

    content = content.replace("{{title}}", title)
    content = content.replace("{{date:YYYY-MM-DD}}", today)
    content = content.replace("severity: medium  # low | medium | high | critical",
                              f"severity: {kwargs['severity']}")
    content = content.replace("language: ", f"language: {kwargs['lang']}")
    content = content.replace("project: ", f"project: {kwargs['project']}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: errors/{filename}")
    print(f"  Status: open")
    print(f"  Severity: {kwargs['severity']}")
    if kwargs['language']: print(f"  Language: {kwargs['lang']}")
    if kwargs['project']: print(f"  Project: {kwargs['project']}")
    print()
    print("Next: fill in Environment, Error/Symptom, and Reproduction Steps.")


if __name__ == "__main__":
    main()
