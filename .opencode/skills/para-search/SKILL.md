---
name: para-search
description: Vault search and query engine for the PARA second brain. Builds an index from frontmatter and supports filtered search by tag, status, date range, and full-text. Use when user says "find in vault", "search projects", "what's active", "show me all", or "list projects by status".
id: para-search
title: PARA — Vault Search Engine
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, search, query, navigation]
---

# PARA — Vault Search Engine

> **Goal**: Answer questions about vault contents without scanning files
> one by one. Index frontmatter for fast filtered queries.

---

## 1. Run a Search

```bash
python -m scripts .opencode/skills/para-search [--tag project] [--status active] [--since 2026-05-01] [--query "keyword"]
```

The script:
1. Walks all `.md` files in content folders
2. Parses frontmatter from each (cached for speed)
3. Filters by any combination of flags
4. Falls back to full-text grep if `--query` is used for body content
5. Outputs results as wikilinks with metadata

---

## 2. Filter Options

| Flag | Example | Matches |
|------|---------|---------|
| `--tag` | `project`, `area`, `resource` | Files with matching `tags` |
| `--status` | `active`, `on-hold`, `done`, `archived` | Files with matching `status` |
| `--type` | `reference`, `research` | Resources with matching `type` |
| `--since` | `2026-05-01` | Files modified after date |
| `--before` | `2026-04-30` | Files modified before date |
| `--folder` | `projects`, `daily`, `areas` | Files in specific folder |
| `--query` | `"keyword phrase"` | Full-text search in body |
| `--count` | (flag) | Show counts only, not file list |

---

## 3. Output Format

```
============================================================
  PARA Search: tag=project, status=active
============================================================

  3 results:

  [[projects/website-redesign]]    status=active    started=2026-05-15
  [[projects/api-migration]]       status=active    started=2026-05-20
  [[projects/docs-overhaul]]       status=active    started=2026-05-25

------------------------------------------------------------
  Found 3 files
```

With `--count`:
```
active: 3 | on-hold: 1 | done: 2 | archived: 5
```

---

## 4. Common Queries

| Question | Command |
|----------|---------|
| "What's active?" | `--tag project --status active` |
| "Show blocked projects" | `--tag project --status on-hold` |
| "What did I do this week?" | `--folder daily --since YYYY-MM-DD` |
| "Find everything about X" | `--query "X"` |
| "How many projects total?" | `--tag project --count` |

---

## 5. Performance Notes

- First run builds an index (~1s for 100 files)
- Subsequent runs are instant (cached)
- The index invalidates when files are modified
- For very large vaults (>1000 files), use `--folder` to limit scope
