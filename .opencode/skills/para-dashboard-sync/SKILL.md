---
name: para-dashboard-sync
description: Dashboard synchronization utility for the PARA second brain. Scans the vault, counts projects by status, and updates Dashboard.md tables automatically. Use when user says "sync dashboard", "update dashboard", "refresh counts", or after any project status change.
id: para-dashboard-sync
title: PARA — Dashboard Sync Utility
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, dashboard, sync, maintenance]
---

# PARA — Dashboard Sync Utility

> **Goal**: Keep Dashboard.md accurate by scanning the vault and updating
> all counts and tables. Run this after any project status change.

---

## 1. Run Dashboard Sync

```bash
python -m scripts .opencode/skills/para-dashboard-sync [--dry-run]
```

The script:
1. Scans `projects/*.md` — counts by status (active, on-hold, done)
2. Scans `areas/*.md` — counts active areas
3. Scans `resources/*.md` — counts resources
4. Scans `archives/*.md` — counts archived projects
5. Scans `daily/*.md` — counts daily entries
6. Scans `weekly/*.md` — counts weekly reviews
7. Updates the PARA Structure table in Dashboard.md
8. Rebuilds the Active Projects table from frontmatter
9. Updates the "Recent Activity" section

---

## 2. What Gets Updated

| Dashboard Section | Source | Update |
|-------------------|--------|--------|
| PARA Structure table | File counts | Refresh all counts |
| Active Projects table | `projects/*.md` frontmatter | Rebuild from active/on-hold projects |
| Recent Activity | `daily/*.md` file dates | Last 5 daily logs |

---

## 3. When to Run

Run `para-dashboard-sync` after:
- Creating a new project (`para-project-brief`)
- Changing a project status
- Moving a project to archives
- Deleting a project
- Creating a new area or resource

---

## 4. Manual Sync Checklist

If the script can't run, update Dashboard.md manually:

```
- [ ] PARA Structure: update all counts
- [ ] Active Projects: verify every row matches frontmatter
- [ ] Blockers: check daily logs for unresolved blockers
- [ ] Recent Activity: list last 5 daily logs
- [ ] Last updated: set to today's date
```
