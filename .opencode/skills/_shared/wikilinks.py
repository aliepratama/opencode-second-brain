"""Extract, resolve, and validate [[wikilinks]] across the vault."""

import re
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

EXTENSIONS = (".md", ".png", ".jpg", ".pdf", ".json")


def extract_wikilinks(text: str) -> list[str]:
    """Return raw link targets from all [[wikilinks]] in text."""
    return WIKILINK_RE.findall(text)


def resolve_wikilink(link: str, from_file: str, vault_root: str) -> Path | None:
    """Resolve a wikilink target relative to the source file. Returns absolute path or None."""
    root = Path(vault_root)
    source = Path(from_file)

    # Split link on | and | to get raw target
    target_raw = link.split("|")[0].split("#")[0].strip()

    # Handle relative paths (starting with ../)
    if target_raw.startswith("../"):
        target_path = (source.parent / target_raw).resolve()
    elif target_raw.startswith("/"):
        target_path = (root / target_raw.lstrip("/")).resolve()
    else:
        # Non-relative: search in folders
        target_path = _search_vault(target_raw, root)

    if target_path and target_path.exists():
        return target_path

    # Try adding .md extension
    for ext in EXTENSIONS:
        candidate = target_path.with_suffix(ext) if target_path else None
        if candidate and candidate.exists():
            return candidate

    return None


def _search_vault(target: str, vault_root: Path) -> Path | None:
    """Search for a file by name across the vault folders."""
    search_folders = ["projects", "areas", "resources", "archives", "daily", "weekly"]
    target_name = target.replace("\\", "/").split("/")[-1]

    for folder in search_folders:
        folder_path = vault_root / folder
        if not folder_path.exists():
            continue
        for ext in [""] + list(EXTENSIONS):
            candidate = folder_path / f"{target_name}{ext}"
            if candidate.exists():
                return candidate

    return None


def find_all_references(target_file: str, vault_root: str) -> list[tuple[str, int]]:
    """Find all files and line numbers that reference a target file. Returns [(filepath, line_number), ...]."""
    root = Path(vault_root)
    target_path = Path(target_file).resolve()
    target_rel = target_path.relative_to(root)
    target_name = target_path.stem

    results = []
    for md_file in root.rglob("*.md"):
        if md_file.resolve() == target_path:
            continue
        if ".obsidian" in str(md_file) or ".opencode" in str(md_file):
            continue

        try:
            with open(md_file, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    links = extract_wikilinks(line)
                    for link in links:
                        link_target = link.split("|")[0].split("#")[0].strip()
                        if target_name in link_target or str(target_rel) in link_target:
                            results.append((str(md_file.relative_to(root)), i))
        except Exception:
            continue

    return results
