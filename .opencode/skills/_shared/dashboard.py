"""Parse and update Dashboard.md tables."""

import re
from pathlib import Path

TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|")


def parse_active_projects(dashboard_path: str) -> list[dict]:
    """Extract active projects from the Dashboard table. Returns list of {project, status, priority, next_action}."""
    with open(dashboard_path, encoding="utf-8") as f:
        content = f.read()

    in_table = False
    projects = []

    for line in content.split("\n"):
        if "Active Projects" in line:
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("| --") or line.strip().startswith("|-"):
                continue
            if not line.strip().startswith("|"):
                break
            if "—" in line:
                continue  # Empty row placeholder

            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 4 and cells[0] and cells[0] != "Project":
                projects.append({
                    "project": cells[0],
                    "status": cells[1] if len(cells) > 1 else "",
                    "priority": cells[2] if len(cells) > 2 else "",
                    "next_action": cells[3] if len(cells) > 3 else "",
                })

    return projects


def count_by_status(vault_root: str) -> dict:
    """Count projects by status, areas, and resources."""
    root = Path(vault_root)
    counts = {
        "active_projects": 0,
        "on_hold_projects": 0,
        "done_projects": 0,
        "areas": 0,
        "resources": 0,
        "archived": 0,
        "daily": 0,
        "weekly": 0,
    }

    for f in (root / "projects").glob("*.md"):
        if f.name == ".gitkeep":
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                content = fh.read(500)
            if "status: active" in content:
                counts["active_projects"] += 1
            elif "status: on-hold" in content:
                counts["on_hold_projects"] += 1
            elif "status: done" in content:
                counts["done_projects"] += 1
        except Exception:
            pass

    counts["areas"] = len([f for f in (root / "areas").glob("*.md") if f.name != ".gitkeep"])
    counts["resources"] = len([f for f in (root / "resources").glob("*.md") if f.name != ".gitkeep"])
    counts["archived"] = len([f for f in (root / "archives").glob("*.md") if f.name != ".gitkeep"])
    counts["daily"] = len([f for f in (root / "daily").glob("*.md") if f.name != ".gitkeep"])
    counts["weekly"] = len([f for f in (root / "weekly").glob("*.md") if f.name != ".gitkeep"])

    return counts


def update_para_counts(dashboard_path: str, counts: dict) -> bool:
    """Update the PARA Structure counts in Dashboard.md. Returns True if changes were made."""
    with open(dashboard_path, encoding="utf-8") as f:
        lines = f.readlines()

    changed = False
    folder_map = {
        "projects/": f"{counts['active_projects']} active",
        "areas/": f"{counts['areas']} areas",
        "resources/": f"{counts['resources']} resources",
        "archives/": f"{counts['archived']} archived",
        "daily/": f"{counts['daily']} entries",
        "weekly/": f"{counts['weekly']} entries",
    }

    new_lines = []
    for line in lines:
        updated = line
        for folder, new_count in folder_map.items():
            if f"[[{folder}" in line:
                match = re.match(r"(\|\s*\[\[" + re.escape(folder) + r"\]\]\s*\|[^|]*\|)\s*.*?(\s*\|)", line)
                if match:
                    updated = f"{match.group(1)} {new_count} {match.group(2)}\n"
                    if updated != line:
                        changed = True
                break
        new_lines.append(updated)

    if changed:
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return changed
