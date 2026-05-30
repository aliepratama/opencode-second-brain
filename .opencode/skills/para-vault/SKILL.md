---
name: para-vault
description: Core orchestrator for the PARA second brain. Loads vault conventions from AGENTS.md and dispatches to sub-skills. Use when user says "second brain", "manage my vault", "update vault", "organize notes", or any command related to the knowledge management system.
id: para-vault
title: PARA Second Brain — Core Orchestrator
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, second-brain, knowledge-management, productivity]
---

# PARA Second Brain — Core Orchestrator

> **Goal**: Coordinate all PARA operations. This skill knows the full vault
> structure, conventions, and routing rules. When loaded, it makes the agent
> aware of the second brain context and dispatches to the right sub-skill.

---

## 1. Vault Context

Load these conventions immediately:

```
Root:       Find AGENTS.md — that's the vault root
Structure:  projects/ areas/ resources/ archives/ daily/ weekly/ templates/
Config:     .obsidian/ (wikiLinks=true, relative paths)
Agents:     .opencode/ (skill configs, shared libs)
```

### Status Flow
```
active → on-hold → done → archived
  ↑                    │
  └────────────────────┘ (reactivate)
```

### File Conventions
| Folder | Frontmatter Required | Pattern |
|--------|---------------------|---------|
| `projects/` | `tags: project`, `status: {active\|on-hold\|done\|archived}` | kebab-case.md |
| `areas/` | `tags: area`, `status: active` | kebab-case.md |
| `resources/` | `tags: resource`, `type: {reference\|research}` | kebab-case.md |
| `archives/` | `tags: project`, `status: archived` | kebab-case.md |
| `daily/` | `tags: #daily/YYYY-MM` | YYYY-MM-DD.md |
| `weekly/` | `tags: #review/weekly` | YYYY-WNN.md |
| `templates/` | N/A (prefixed `_`) | _*.md |

---

## 2. Skill Dispatch Table

Based on user intent, route to the appropriate sub-skill:

| User says | Load this skill | What happens |
|-----------|----------------|-------------|
| "daily log", "today's log", "what's happening today" | `para-daily-log` | Create/view daily log |
| "new project", "start a project", "create brief" | `para-project-brief` | Create project brief |
| "weekly review", "progress this week" | `para-weekly-review` | Generate weekly review |
| "monthly review", "end of month" | `para-monthly-review` | Archive + monthly review |
| "sync dashboard", "update dashboard" | `para-dashboard-sync` | Refresh Dashboard counts |
| "check links", "broken links" | `para-link-validator` | Validate wikilinks |
| "check frontmatter", "validate metadata" | `para-frontmatter-check` | Validate frontmatter |
| "search vault", "find project", "what's active" | `para-search` | Search across vault |
| "create diagram", "mermaid", "flowchart" | `para-mermaid` | Mermaid best practices |
| "validate document", "clean output", "check for errors" | `para-md-validator` | Auto-validate markdown |
| "format table", "create table", "fix table" | `para-table-formatter` | Table formatting |

---

## 3. Golden Rules

These are non-negotiable. Enforce them in every interaction:

1. **Search First**: Always search `projects/`, `areas/`, `resources/`, `daily/` before answering vault questions.
2. **Status Gate**: When mentioning a project, always include its `status` from frontmatter.
3. **No Template Edits**: Never modify `templates/_*.md` unless explicitly asked.
4. **Preserve Dashboard**: Never delete or restructure `Dashboard.md`.
5. **Link Everything**: Use `[[wikilinks]]` between related files.
6. **Daily Summary Required**: Every daily log must end with `## Daily Summary`.
7. **Weekly Review Trigger**: If asked about weekly progress, suggest creating/updating the review.
8. **Strikethrough Done**: Completed items use `~~strikethrough~~`.
9. **Dashboard Sync**: When project statuses change, run `para-dashboard-sync`.

---

## 4. Script Invocation

All scripts live in `scripts/` subdirectories alongside their SKILL.md:

```bash
python -m scripts <skill-dir> <args...>
```

Shared utilities in `_shared/` are importable by all scripts:
```python
from _shared import vault, frontmatter, wikilinks, dashboard
```

---

## 5. When NOT to Use Sub-Skills

Some queries are simple enough to answer directly:
- "What's the status convention?" → Answer from this SKILL.md
- "What folder does X go in?" → Answer from directory rules
- "Show me the file naming convention" → Answer from conventions table

Don't load a sub-skill for a one-line factual answer.
