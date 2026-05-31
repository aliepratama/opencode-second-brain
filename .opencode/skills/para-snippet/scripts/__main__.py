"""Manage code snippets: add, search, and list.

Usage:
    python -m scripts .opencode/skills/para-snippet add "Title" --lang python --tags "async,http"
    python -m scripts .opencode/skills/para-snippet search --lang python --tag "async"
    python -m scripts .opencode/skills/para-snippet list [--lang python]
"""

import os
import re
import sys
from datetime import date
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
        if ":" in line and not line.strip().startswith("#"):
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _sanitize_name(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-").strip("-")[:60]


def _parse_args(argv):
    """Parse command-line arguments into a dict."""
    result = {"command": argv[0] if argv else "help"}
    i = 1
    while i < len(argv):
        if argv[i] == "--lang" and i + 1 < len(argv):
            result["lang"] = argv[i + 1]; i += 2
        elif argv[i] == "--tags" and i + 1 < len(argv):
            result["tags"] = argv[i + 1]; i += 2
        elif argv[i] == "--tag" and i + 1 < len(argv):
            result["tag"] = argv[i + 1]; i += 2
        elif argv[i] == "--query" and i + 1 < len(argv):
            result["query"] = argv[i + 1]; i += 2
        else:
            i += 1
    return result


def cmd_add(args: dict):
    title = args.get("_title", "Untitled")
    lang = args.get("lang", "python")
    tags_val = args.get("tags", "")

    slug = _sanitize_name(title)
    filepath = VAULT_ROOT / "snippets" / f"{slug}.md"

    if filepath.exists():
        print(f"Snippet already exists: snippets/{slug}.md")
        return

    template_path = VAULT_ROOT / "templates" / "_code-snippet.md"
    if not template_path.exists():
        template_path = VAULT_ROOT / "editions" / "dev" / "templates" / "_code-snippet.md"
    if not template_path.exists():
        raise SystemExit("ERROR: _code-snippet.md template not found")

    content = template_path.read_text(encoding="utf-8")
    today = date.today().strftime("%Y-%m-%d")

    content = content.replace("{{title}}", title)
    content = content.replace("{{date:YYYY-MM-DD}}", today)
    content = content.replace("language: ", f"language: {lang}")
    content = content.replace("tags: []", f"tags: [{tags_val}]")
    content = content.replace("```<!-- language -->", f"```{lang}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: snippets/{slug}.md")
    print(f"  Language: {lang}")
    print(f"  Tags: {tags_val}")


def cmd_search(args: dict):
    lang_filter = args.get("lang", "").lower()
    tag_filter = args.get("tag", "").lower()
    query = args.get("query", "").lower()

    snippets_dir = VAULT_ROOT / "snippets"
    if not snippets_dir.exists():
        print("No snippets found. Create one with 'para-snippet add'")
        return

    results = []
    for f in snippets_dir.glob("*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            fm = _parse_frontmatter(text)

            if lang_filter and fm.get("language", "").lower() != lang_filter:
                continue
            if tag_filter:
                tags = fm.get("tags", "")
                if tag_filter not in tags.lower():
                    continue
            if query and query not in text.lower():
                continue

            results.append((f.stem, fm.get("language", "?"), fm.get("tags", "")))
        except Exception:
            continue

    print("=" * 60)
    filters = []
    if lang_filter: filters.append(f"lang={lang_filter}")
    if tag_filter: filters.append(f"tag={tag_filter}")
    if query: filters.append(f"query='{query}'")
    print(f"  Snippets ({', '.join(filters) if filters else 'all'})")
    print("=" * 60)
    print()

    if not results:
        print("  No snippets found.")
        return

    for name, lang, tags in results:
        print(f"  [[snippets/{name}]]  lang={lang}  tags=[{tags}]")

    print()
    print("-" * 60)
    print(f"  Found {len(results)} snippet(s)")


def cmd_list(args: dict):
    args["_no_filter"] = True
    cmd_search(args)


def main():
    _find_vault_root()

    argv = sys.argv[1:]
    if not argv or argv[0] == "help":
        print("Usage:")
        print("  add 'Title' --lang python --tags 'async,http'")
        print("  search --lang python --tag 'async'")
        print("  list [--lang python]")
        return

    cmd = argv[0]
    args = _parse_args(argv)
    if cmd not in ("add", "search", "list"):
        # first arg is title for add
        args["_title"] = cmd
        cmd_add(args)
    elif cmd == "add":
        if len(argv) > 1 and not argv[1].startswith("--"):
            args["_title"] = argv[1]
        cmd_add(args)
    elif cmd in ("search", "list"):
        (cmd_search if cmd == "search" else cmd_list)(args)


if __name__ == "__main__":
    main()
