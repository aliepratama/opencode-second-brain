---
name: para-frontmatter-check
description: Frontmatter compliance checker for the PARA second brain. Validates that every markdown file has the required YAML frontmatter for its folder. Use when user says "check frontmatter", "validate metadata", "fix frontmatter", or "metadata check".
id: para-frontmatter-check
title: PARA — Frontmatter Compliance Checker
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, validation, frontmatter, metadata]
---

# PARA — Frontmatter Compliance Checker

> **Goal**: Ensure every file has correct frontmatter for its directory.
> Catch missing tags, invalid statuses, and inconsistent metadata.

---

## 1. Run Frontmatter Check

```bash
python -m scripts .opencode/skills/para-frontmatter-check [--fix]
```

The script:
1. Scans all `.md` files across `projects/`, `areas/`, `resources/`, `archives/`
2. Parses YAML frontmatter from each file
3. Validates required keys per folder
4. Validates status values against the allowed set
5. Reports missing, invalid, or inconsistent fields
6. With `--fix`: attempts to auto-correct common mistakes

---

## 2. Validation Rules by Folder

| Folder | Required | Valid Values |
|--------|----------|-------------|
| `projects/` | `tags: project`, `status` | `status`: active, on-hold, done, archived |
| `areas/` | `tags: area`, `status` | `status`: active, on-hold |
| `resources/` | `tags: resource`, `type` | `type`: reference, research |
| `archives/` | `tags: project`, `status` | `status`: archived |

---

## 3. Output Format

```
============================================================
  PARA Frontmatter Checker
============================================================

[MISSING FIELDS]
  projects/my-feature.md  → missing: status
  areas/design.md         → missing: tags

[INVALID VALUES]
  projects/broken.md      → status: "wip" (must be: active, on-hold, done, archived)
  resources/research.md   → type: "notes" (must be: reference, research)

[INCONSISTENT]
  projects/stale.md       → status: done but checklist shows incomplete

------------------------------------------------------------
  Total: 8 files scanned, 3 issues found
```

---

## 4. Common Mistakes

| Issue | Fix |
|-------|-----|
| `status:` empty or missing | Set to `active` for new files |
| `tags: project` missing in projects/ | Add `tags: project` |
| Old status value (`wip`, `in-progress`) | Migrate to: `active`, `on-hold`, `done`, `archived` |
| `status: done` but checklist not all checked | Either update checklist or revert status |
| Missing YAML delimiters (`---`) | Add `---` at start of file |
