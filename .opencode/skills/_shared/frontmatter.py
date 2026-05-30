"""Parse and validate YAML frontmatter from markdown files."""

import re
from pathlib import Path

YAML_BLOCK_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

STATUS_VALUES = {"active", "on-hold", "done", "archived"}
TAG_VALUES = {"project", "area", "resource"}
TYPE_VALUES = {"reference", "research"}

REQUIRED_BY_FOLDER = {
    "projects": {"tags": lambda v: "project" in str(v), "status": lambda v: v in STATUS_VALUES},
    "areas": {"tags": lambda v: "area" in str(v), "status": lambda v: v in STATUS_VALUES},
    "resources": {"tags": lambda v: "resource" in str(v)},
    "archives": {"tags": lambda v: "project" in str(v), "status": lambda v: v == "archived"},
}


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter as a flat dict of key-value pairs."""
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


def get_frontmatter(filepath: str) -> dict:
    """Read a file and return its frontmatter."""
    with open(filepath, encoding="utf-8") as f:
        return parse_frontmatter(f.read())


def write_frontmatter(filepath: str, updates: dict) -> None:
    """Update frontmatter fields in a markdown file. Only changes existing keys."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    match = YAML_BLOCK_RE.match(content)
    if not match:
        return

    fm_block = match.group(1)
    fm_dict = parse_frontmatter(content)
    fm_dict.update(updates)

    new_fm = "---\n"
    for k, v in fm_dict.items():
        new_fm += f"{k}: {v}\n"
    new_fm += "---\n"

    new_content = new_fm + content[match.end():]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)


def validate_status(value: str | None) -> tuple[bool, str]:
    """Validate a status value. Returns (is_valid, error_message)."""
    if not value:
        return False, "status is missing"
    if value not in STATUS_VALUES:
        return False, f"invalid status '{value}' — must be one of: {STATUS_VALUES}"
    return True, ""


def validate_frontmatter_for_file(filepath: str) -> list[str]:
    """Check a file's frontmatter against rules for its folder. Returns list of errors."""
    path = Path(filepath)
    folder = path.parent.name
    fm = get_frontmatter(filepath)
    errors = []

    rules = REQUIRED_BY_FOLDER.get(folder)
    if not rules:
        return errors

    for key, check in rules.items():
        value = fm.get(key)
        if value is None:
            errors.append(f"{filepath}: missing '{key}' in frontmatter")
        elif not check(value):
            errors.append(f"{filepath}: invalid '{key}' value: '{value}'")

    return errors
