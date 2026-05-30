"""Validate frontmatter compliance across all vault files.

Usage:
    python -m scripts .opencode/skills/para-frontmatter-check [--fix]
"""

import os
import re
import sys
from pathlib import Path

VAULT_ROOT = None

STATUS_VALUES = {"active", "on-hold", "done", "archived"}
YAML_BLOCK_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

REQUIRED_BY_FOLDER = {
    "projects": {"tags": "project", "status": STATUS_VALUES},
    "areas": {"tags": "area", "status": {"active", "on-hold"}},
    "resources": {"tags": "resource"},
    "archives": {"tags": "project", "status": {"archived"}},
}


def _find_vault_root():
    global VAULT_ROOT
    current = Path(os.getcwd())
    for parent in [current, *current.parents]:
        if (parent / "AGENTS.md").exists():
            VAULT_ROOT = parent
            return
    raise SystemExit("ERROR: AGENTS.md not found. Run from inside a second brain vault.")


def _parse_frontmatter(text: str) -> dict:
    match = YAML_BLOCK_RE.match(text)
    if not match:
        return {}
    result = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            result[key] = val
    return result


def main():
    global VAULT_ROOT
    _find_vault_root()

    fix = "--fix" in sys.argv
    issues = []

    folders = ["projects", "areas", "resources", "archives"]
    for folder in folders:
        d = VAULT_ROOT / folder
        if not d.exists():
            continue
        rules = REQUIRED_BY_FOLDER.get(folder, {})
        for f in d.glob("*.md"):
            if f.name == ".gitkeep":
                continue
            try:
                text = f.read_text(encoding="utf-8")
                fm = _parse_frontmatter(text)

                for key, expected in rules.items():
                    value = fm.get(key)
                    if value is None:
                        issues.append(f"[MISSING] {folder}/{f.name}: '{key}' not found")
                        if fix and key == "status":
                            new_text = text
                            if text.startswith("---"):
                                new_text = re.sub(
                                    r"(---\s*\n.*?\n)---",
                                    rf"\1status: active\n---",
                                    text, count=1, flags=re.DOTALL
                                )
                            f.write_text(new_text, encoding="utf-8")
                            print(f"  FIXED: Added status: active to {folder}/{f.name}")
                    elif isinstance(expected, set) and value not in expected:
                        issues.append(f"[INVALID] {folder}/{f.name}: '{key}' = '{value}' (expected: {expected})")
                        if fix and key == "status":
                            new_text = re.sub(rf"^status:\s*{re.escape(value)}", "status: active", text, flags=re.MULTILINE)
                            f.write_text(new_text, encoding="utf-8")
                            print(f"  FIXED: status: {value} -> active in {folder}/{f.name}")
                    elif isinstance(expected, str) and expected not in value:
                        issues.append(f"[INVALID] {folder}/{f.name}: '{key}' = '{value}' (expected to contain: {expected})")

            except Exception as e:
                issues.append(f"[ERROR] {folder}/{f.name}: {e}")

    print("=" * 60)
    print("  PARA Frontmatter Checker")
    print("=" * 60)
    print()

    if issues:
        for issue in issues:
            print(f"  {issue}")
        print()
        print("-" * 60)
        print(f"  Total: {len(issues)} issue(s) found")
    else:
        print("  All files pass validation.")
        print()

    total = sum(len([f for f in (VAULT_ROOT / folder).glob("*.md") if f.name != ".gitkeep"])
                 for folder in folders if (VAULT_ROOT / folder).exists())
    print(f"  Scanned: {total} files across {len(folders)} folders")


if __name__ == "__main__":
    main()
