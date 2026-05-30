---
name: para-monthly-review
description: Monthly review and archival workflow for the PARA second brain. Moves done projects to archives, updates cross-references, reviews all areas. Use when user says "monthly review", "end of month", "archive projects", or "quarterly review".
id: para-monthly-review
title: PARA — Monthly Review & Archive Workflow
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, review, monthly, archive, maintenance]
depends_on:
  - para-dashboard-sync
  - para-link-validator
---

# PARA — Monthly Review & Archive Workflow

> **Goal**: Clean up the vault at the end of each month. Move completed
> projects to archives, update all references, and reflect on progress.

---

## 1. Generate a Monthly Review

### Use the script

```bash
python -m scripts .opencode/skills/para-monthly-review [--dry-run]
```

The script:
1. Scans `projects/*.md` for `status: done`
2. Lists projects ready to archive
3. In non-dry-run mode: moves files to `archives/`
4. Changes `status: done` → `status: archived` in frontmatter
5. Finds and updates ALL `[[projects/xxx]]` references across the vault
6. Regenerates Dashboard tables
7. Creates `weekly/YYYY-M.md` monthly review file

**Always run with `--dry-run` first** to review what will change.

---

## 2. Archive Workflow (Step by Step)

For each project with `status: done`:

```
1. Move:   projects/my-project.md  →  archives/my-project.md
2. Update: status: done  →  status: archived
3. Search: find all [[projects/my-project]] references
4. Replace: [[projects/my-project]] → [[archives/my-project]]
5. Log:    add entry to today's daily log
```

---

## 3. Monthly Review Sections

| Section | Purpose |
|---------|---------|
| **Highlights** | Top 3 accomplishments this month |
| **Project Status** | Table: all projects and their outcomes |
| **Areas Check** | Review each area — needs update? |
| **Lessons Learned** | What worked, what didn't |
| **Next Month Focus** | Top 3 priorities |
| **Archives** | Checklist of projects moved |

---

## 4. Safety Rules

- **Always dry-run first**: `--dry-run` flag shows what will happen
- **Backup**: Consider git commit before running archive
- **Don't delete**: Files are moved, not deleted. Archives is permanent.
- **Update Dashboard**: Run `para-dashboard-sync` after archiving
- **Validate links**: Run `para-link-validator` after mass updates

---

## 5. Area Review Checklist

During monthly review, check each area:

```markdown
- [ ] Area still relevant?
- [ ] Status up to date?
- [ ] New sub-items added?
- [ ] Linked projects current?
```

If an area hasn't been touched in 3+ months, flag it for review.
