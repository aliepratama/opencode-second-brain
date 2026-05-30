"""Monthly review: archive done projects and generate monthly review.

Usage:
    python -m scripts .opencode/skills/para-monthly-review [--dry-run]
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


def _find_done_projects() -> list[Path]:
    projects = []
    for f in (VAULT_ROOT / "projects").glob("*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            if re.search(r"^status:\s*done\s*$", text, re.MULTILINE):
                projects.append(f)
        except Exception:
            continue
    return projects


def _update_references(old_name: str, new_name: str):
    old_link = f"[[projects/{old_name}]]"
    new_link = f"[[archives/{old_name}]]"
    old_link_alt = f"[[../projects/{old_name}]]"
    new_link_alt = f"[[../archives/{old_name}]]"
    old_link_display = f"[[projects/{old_name}|"
    new_link_display = f"[[archives/{old_name}|"
    old_link_display2 = f"[[../projects/{old_name}|"
    new_link_display2 = f"[[../archives/{old_name}|"

    for md_file in VAULT_ROOT.rglob("*.md"):
        if ".obsidian" in str(md_file) or ".opencode" in str(md_file):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            updated = text
            updated = updated.replace(old_link_display, new_link_display)
            updated = updated.replace(old_link_display2, new_link_display2)
            updated = updated.replace(old_link, new_link)
            updated = updated.replace(old_link_alt, new_link_alt)
            if updated != text:
                md_file.write_text(updated, encoding="utf-8")
                print(f"  Updated references in: {md_file.relative_to(VAULT_ROOT)}")
        except Exception as e:
            print(f"  WARNING: Could not update {md_file.relative_to(VAULT_ROOT)}: {e}")


def main():
    _find_vault_root()
    _find_shared()

    dry_run = "--dry-run" in sys.argv
    today = date.today()
    month_str = today.strftime("%Y-%m")

    done = _find_done_projects()

    if not done:
        print("No projects with status 'done' found.")
        return

    print(f"Found {len(done)} project(s) ready to archive:")
    for p in done:
        print(f"  - projects/{p.name}")

    if dry_run:
        print("\n[Dry run] No files were changed.")
        print("Run without --dry-run to execute.")
        return

    print("\nArchiving...")
    for p in done:
        dest = VAULT_ROOT / "archives" / p.name
        content = p.read_text(encoding="utf-8")
        content = re.sub(r"^status:\s*done\s*$", "status: archived", content, flags=re.MULTILINE)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        p.unlink()
        print(f"  Moved: projects/{p.name} -> archives/{p.name}")

        _update_references(p.stem, p.stem)

    # Generate monthly review
    review_path = VAULT_ROOT / "weekly" / f"{month_str}-review.md"
    template_path = VAULT_ROOT / "templates" / "_monthly-review.md"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{{date:YYYY-MM}}", month_str)
        for p in done:
            content = content.replace(
                "- [ ] Move [[../projects/xxx.md]]",
                f"- [x] Moved [[../projects/{p.stem}.md]] -> [[../archives/{p.stem}.md]]\n- [ ] Move [[../projects/xxx.md]]"
            )
        review_path.write_text(content, encoding="utf-8")
        print(f"\nCreated monthly review: weekly/{month_str}-review.md")

    print("\nDone. Run 'para-dashboard-sync' to update Dashboard counts.")


if __name__ == "__main__":
    main()
