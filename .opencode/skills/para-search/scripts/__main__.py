"""Search the vault by tag, status, folder, date range, or full-text query.

Usage:
    python -m scripts .opencode/skills/para-search [--tag project] [--status active]
        [--since 2026-05-01] [--folder projects] [--query "keyword"] [--count]
"""

import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

VAULT_ROOT = None

YAML_BLOCK_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


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
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _parse_args():
    args = {
        "tag": None,
        "status": None,
        "type": None,
        "since": None,
        "before": None,
        "folder": None,
        "query": None,
        "count": False,
    }

    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        if argv[i] == "--tag" and i + 1 < len(argv):
            args["tag"] = argv[i + 1]; i += 2
        elif argv[i] == "--status" and i + 1 < len(argv):
            args["status"] = argv[i + 1]; i += 2
        elif argv[i] == "--type" and i + 1 < len(argv):
            args["type"] = argv[i + 1]; i += 2
        elif argv[i] == "--since" and i + 1 < len(argv):
            args["since"] = argv[i + 1]; i += 2
        elif argv[i] == "--before" and i + 1 < len(argv):
            args["before"] = argv[i + 1]; i += 2
        elif argv[i] == "--folder" and i + 1 < len(argv):
            args["folder"] = argv[i + 1]; i += 2
        elif argv[i] == "--query" and i + 1 < len(argv):
            args["query"] = argv[i + 1]; i += 2
        elif argv[i] == "--count":
            args["count"] = True; i += 1
        else:
            i += 1

    return args


def main():
    global VAULT_ROOT
    _find_vault_root()
    args = _parse_args()

    folders = [args["folder"]] if args["folder"] else ["projects", "areas", "resources", "archives", "daily", "weekly"]
    results = []
    status_counts = {}
    type_counts = {}

    for folder in folders:
        d = VAULT_ROOT / folder
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
            if f.name == ".gitkeep":
                continue
            try:
                text = f.read_text(encoding="utf-8")
                fm = _parse_frontmatter(text)

                # Apply filters
                if args["tag"] and args["tag"] not in fm.get("tags", ""):
                    continue
                if args["status"] and fm.get("status") != args["status"]:
                    continue
                if args["type"] and fm.get("type") != args["type"]:
                    continue
                if args["since"]:
                    mtime = date.fromtimestamp(f.stat().st_mtime)
                    if mtime < date.fromisoformat(args["since"]):
                        continue
                if args["before"]:
                    mtime = date.fromtimestamp(f.stat().st_mtime)
                    if mtime > date.fromisoformat(args["before"]):
                        continue
                if args["query"]:
                    if args["query"].lower() not in text.lower():
                        continue

                rel = str(f.relative_to(VAULT_ROOT))
                status = fm.get("status", "")
                results.append((rel, status, fm.get("started", "")))

                status_counts[status] = status_counts.get(status, 0) + 1
                type_val = fm.get("type", "")
                if type_val:
                    type_counts[type_val] = type_counts.get(type_val, 0) + 1

            except Exception as e:
                print(f"  [SKIP] {f.relative_to(VAULT_ROOT)}: {e}")

    # Build filter label
    filters = []
    if args["tag"]: filters.append(f"tag={args['tag']}")
    if args["status"]: filters.append(f"status={args['status']}")
    if args["type"]: filters.append(f"type={args['type']}")
    if args["since"]: filters.append(f"since={args['since']}")
    if args["folder"]: filters.append(f"folder={args['folder']}")
    if args["query"]: filters.append(f"query='{args['query']}'")
    filter_str = ", ".join(filters) if filters else "all files"

    print("=" * 60)
    print(f"  PARA Search: {filter_str}")
    print("=" * 60)
    print()

    if args["count"]:
        if status_counts:
            print("  By status:")
            for s, c in sorted(status_counts.items()):
                print(f"    {s}: {c}")
        if type_counts:
            print("  By type:")
            for t, c in sorted(type_counts.items()):
                print(f"    {t}: {c}")
        print()
        print("-" * 60)
        print(f"  Total: {len(results)} files")
    elif results:
        for path, status, started in results:
            meta = f"status={status}" if status else ""
            if started:
                meta += f" started={started}"
            print(f"  [[{path}]]  {meta}")
        print()
        print("-" * 60)
        print(f"  Found {len(results)} file(s)")
    else:
        print("  No results found.")
        print()
        print("-" * 60)
        print("  Try different filters or use --folder to narrow search.")


if __name__ == "__main__":
    main()
