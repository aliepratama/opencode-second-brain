#!/usr/bin/env python3
"""Developer Edition Setup Script

Creates a developer-focused PARA second brain vault from the dev edition templates.

Usage:
    python editions/dev/setup.py /path/to/target --init    # Fresh dev vault
    python editions/dev/setup.py /path/to/existing --merge  # Add dev extras to existing

What it creates:
    adrs/           Architecture Decision Records
    snippets/       Code snippets by language
    learnings/      Tech learning journal
    errors/         Bug/error tracking

Options:
    --init      Create fresh dev vault (copies all core files)
    --merge     Add dev extras to existing general vault
    --dry-run   Preview without writing files
"""

import argparse
import os
import shutil
import sys
from datetime import date
from pathlib import Path


REPO_ROOT = None


def find_repo_root():
    global REPO_ROOT
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists() and (parent / ".opencode").exists():
            REPO_ROOT = parent
            return
    raise SystemExit("ERROR: Cannot find repo root. Run from within opencode-second-brain.")


def copy_template(src_name: str, dest_dir: Path, dry_run: bool = False):
    """Copy a template file."""
    src = Path(__file__).parent / "templates" / src_name
    dest = dest_dir / "templates" / src_name

    if dest.exists():
        print(f"  SKIP: {dest.relative_to(dest_dir)} already exists")
        return

    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    print(f"  COPY: templates/{src_name}")


def create_folder(name: str, dest_dir: Path, dry_run: bool = False):
    """Create a folder with .gitkeep."""
    folder = dest_dir / name
    if folder.exists():
        print(f"  SKIP: {name}/ already exists")
        return

    if not dry_run:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / ".gitkeep").write_text("")
    print(f"  CREATE: {name}/")


def copy_core_files(dest_dir: Path, dry_run: bool = False):
    """Copy AGENTS.md, Dashboard.md, and .obsidian config."""
    files_to_copy = ["AGENTS.md", "Dashboard.md"]
    dev_dir = Path(__file__).parent

    for fname in files_to_copy:
        src = dev_dir / fname
        dest = dest_dir / fname
        if dest.exists():
            print(f"  SKIP: {fname} already exists")
            continue
        if not dry_run:
            shutil.copy2(src, dest)
        print(f"  COPY: {fname}")

    # Copy .obsidian from root if available
    obsidian_src = REPO_ROOT / ".obsidian"
    obsidian_dest = dest_dir / ".obsidian"
    if obsidian_src.exists() and not obsidian_dest.exists():
        if not dry_run:
            shutil.copytree(obsidian_src, obsidian_dest)
        print(f"  COPY: .obsidian/")


def copy_skills(dest_dir: Path, dry_run: bool = False):
    """Copy the entire .opencode/skills/ directory."""
    skills_src = REPO_ROOT / ".opencode" / "skills"
    skills_dest = dest_dir / ".opencode" / "skills"

    if skills_dest.exists():
        print(f"  SKIP: .opencode/skills/ already exists")
        return

    if not dry_run:
        shutil.copytree(skills_src, skills_dest)
    print(f"  COPY: .opencode/skills/ (16 skills)")


def copy_opencode_config(dest_dir: Path, dry_run: bool = False):
    """Copy opencode.jsonc."""
    src = REPO_ROOT / ".opencode" / "opencode.jsonc"
    dest = dest_dir / ".opencode" / "opencode.jsonc"

    if dest.exists():
        print(f"  SKIP: .opencode/opencode.jsonc already exists")
        return

    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    print(f"  COPY: .opencode/opencode.jsonc")


def copy_general_templates(dest_dir: Path, dry_run: bool = False):
    """Copy general edition templates (daily, project, weekly, monthly)."""
    general_tmpl = ["_daily-log.md", "_project-brief.md", "_weekly-review.md", "_monthly-review.md"]
    src_dir = REPO_ROOT / "templates"

    for tmpl in general_tmpl:
        src = src_dir / tmpl
        dest = dest_dir / "templates" / tmpl
        if dest.exists():
            continue
        if src.exists():
            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            print(f"  COPY: templates/{tmpl}")


def create_para_folders(dest_dir: Path, dry_run: bool = False):
    """Create standard PARA folders."""
    for folder in ["projects", "areas", "resources", "archives", "daily", "weekly"]:
        create_folder(folder, dest_dir, dry_run)


def setup_dev(args):
    dest_dir = Path(args.target).resolve()
    dry_run = args.dry_run
    action = "init" if args.init else "merge"

    print("=" * 60)
    print(f"  Developer Edition Setup ({action})")
    print("=" * 60)
    print()

    if dry_run:
        print("[DRY RUN] No files will be written.\n")

    if args.init:
        # Fresh install: create all folders and copy everything
        dest_dir.mkdir(parents=True, exist_ok=True)

        print("Creating folders...")
        create_para_folders(dest_dir, dry_run)

        print("\nCreating developer folders...")
        create_folder("adrs", dest_dir, dry_run)
        create_folder("snippets", dest_dir, dry_run)
        create_folder("learnings", dest_dir, dry_run)
        create_folder("errors", dest_dir, dry_run)

        print("\nCopying core files...")
        copy_core_files(dest_dir, dry_run)

        print("\nCopying templates...")
        copy_general_templates(dest_dir, dry_run)
        dev_templates = [
            "_adr.md", "_bug-tracker.md", "_code-snippet.md",
            "_tech-learning.md", "_sprint-review.md"
        ]
        for tmpl in dev_templates:
            copy_template(tmpl, dest_dir, dry_run)

        print("\nCopying OpenCode skills...")
        copy_skills(dest_dir, dry_run)
        copy_opencode_config(dest_dir, dry_run)

    elif args.merge:
        # Merge into existing vault: only add dev-specific extras
        if not dest_dir.exists():
            raise SystemExit(f"ERROR: Target directory does not exist: {dest_dir}")
        if not (dest_dir / "AGENTS.md").exists():
            print("WARNING: Target doesn't look like a second brain vault (no AGENTS.md found)")
            print("Use --init to create a fresh vault instead.")
            return

        print("Creating developer folders...")
        create_folder("adrs", dest_dir, dry_run)
        create_folder("snippets", dest_dir, dry_run)
        create_folder("learnings", dest_dir, dry_run)
        create_folder("errors", dest_dir, dry_run)

        print("\nCopying developer templates...")
        dev_templates = [
            "_adr.md", "_bug-tracker.md", "_code-snippet.md",
            "_tech-learning.md", "_sprint-review.md"
        ]
        for tmpl in dev_templates:
            copy_template(tmpl, dest_dir, dry_run)

        print("\nCopying developer skills...")
        copy_skills(dest_dir, dry_run)

        print("\nNOTE: AGENTS.md and Dashboard.md were NOT overwritten.")
        print("Review editions/dev/AGENTS.md for developer-specific agent rules.")

    print()
    print("-" * 60)
    print()
    print("Setup complete!")
    print()
    print(f"Open in Obsidian: File → Open Vault → {dest_dir}")
    print()
    print("Next steps:")
    print("  1. Open in Obsidian")
    print("  2. Press Ctrl+Shift+D for today's dev log")
    print("  3. Create an ADR: python -m scripts .opencode/skills/para-adr")
    print("  4. Log a snippet: python -m scripts .opencode/skills/para-snippet add")


def main():
    find_repo_root()

    parser = argparse.ArgumentParser(
        description="Developer Edition Setup for opencode-second-brain"
    )
    parser.add_argument("target", help="Target directory for the dev vault")
    parser.add_argument("--init", action="store_true", help="Create fresh dev vault")
    parser.add_argument("--merge", action="store_true", help="Add dev extras to existing vault")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")

    args = parser.parse_args()

    if not args.init and not args.merge:
        parser.print_help()
        print("\nUse --init for a fresh install or --merge to add to an existing vault.")
        sys.exit(1)

    setup_dev(args)


if __name__ == "__main__":
    main()
