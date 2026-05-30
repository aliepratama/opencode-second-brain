"""Validate all [[wikilinks]] across the vault.

Usage:
    python -m scripts .opencode/skills/para-link-validator [--folder projects] [--verbose]
"""

import os
import re
import sys
from pathlib import Path

VAULT_ROOT = None
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def _find_vault_root():
    global VAULT_ROOT
    current = Path(os.getcwd())
    for parent in [current, *current.parents]:
        if (parent / "AGENTS.md").exists():
            VAULT_ROOT = parent
            return
    raise SystemExit("ERROR: AGENTS.md not found. Run from inside a second brain vault.")


def _resolve(link: str, source: Path) -> Path | None:
    target_raw = link.split("|")[0].split("#")[0].strip()

    if target_raw.startswith("../"):
        target_path = (source.parent / target_raw).resolve()
    elif target_raw.startswith("/"):
        target_path = (VAULT_ROOT / target_raw.lstrip("/")).resolve()
    else:
        # Search in well-known folders
        target_stem = Path(target_raw).stem
        search_folders = ["projects", "areas", "resources", "archives", "daily", "weekly", "templates"]
        for folder in search_folders:
            for ext in [".md", ""]:
                candidate = VAULT_ROOT / folder / f"{target_stem}{ext}"
                if candidate.exists():
                    return candidate
        # Try relative to source
        target_path = (source.parent / target_raw).resolve()

    if target_path and target_path.exists():
        return target_path

    # Try adding .md
    candidate = target_path.with_suffix(".md")
    if candidate.exists():
        return candidate

    return None


def main():
    global VAULT_ROOT
    _find_vault_root()

    verbose = "--verbose" in sys.argv
    folder_filter = None

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--folder" and i < len(sys.argv) - 1:
            folder_filter = sys.argv[i + 1]

    broken = []
    total_files = 0
    total_links = 0

    content_folders = ["projects", "areas", "resources", "archives", "daily", "weekly"]
    if folder_filter:
        content_folders = [folder_filter]

    all_files = []
    for folder in content_folders:
        d = VAULT_ROOT / folder
        if d.exists():
            all_files.extend([f for f in d.glob("*.md") if f.name != ".gitkeep"])

    # Find orphans (files with no incoming links)
    outgoing = set()
    incoming_counts = {}
    for f in all_files:
        incoming_counts[f.stem] = 0

    for source in all_files:
        total_files += 1
        try:
            content = source.read_text(encoding="utf-8")
            links = WIKILINK_RE.findall(content)

            for link in links:
                total_links += 1
                target_raw = link.split("|")[0].split("#")[0].strip()
                target = _resolve(link, source)
                outgoing.add(source.stem)

                if target is None:
                    broken.append((str(source.relative_to(VAULT_ROOT)), link))
                    if verbose:
                        print(f"  BROKEN: {source.relative_to(VAULT_ROOT)} → [[{link}]]")
                else:
                    target_stem = target.stem
                    if target_stem in incoming_counts:
                        incoming_counts[target_stem] += 1

        except Exception as e:
            if verbose:
                print(f"  ERROR reading {source.relative_to(VAULT_ROOT)}: {e}")

    # Report
    print("=" * 60)
    print("  PARA Link Validator")
    print("=" * 60)
    print()

    if broken:
        print("[Broken Links]")
        for source, link in broken:
            print(f"  {source}  →  [[{link}]]")
        print()
    else:
        print("[Broken Links]  None found.")
        print()

    orphans = [k for k, v in incoming_counts.items() if v == 0 and k not in outgoing]
    if orphans:
        print("[Orphaned Files] (no incoming links)")
        for o in orphans:
            print(f"  {o}.md")
        print()
    else:
        print("[Orphaned Files]  None found.")
        print()

    print("-" * 60)
    print(f"  Total: {total_files} files scanned, {total_links} links")
    print(f"  Broken: {len(broken)}, Orphans: {len(orphans)}")
    if broken:
        print("  [FAIL] Fix broken links before archiving or moving files.")


if __name__ == "__main__":
    main()
