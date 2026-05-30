---
name: para-project-brief
description: Project brief creation workflow for the PARA second brain. Copies template, sets frontmatter, links in daily log, updates Dashboard. Use when user says "new project", "start a project", "create project brief", or "kick off a project".
id: para-project-brief
title: PARA — Project Brief Workflow
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, project, planning, tracking]
depends_on:
  - para-dashboard-sync
  - para-table-formatter
---

# PARA — Project Brief Workflow

> **Goal**: Create a well-structured project brief from template, set correct
> frontmatter, link to daily log, and keep Dashboard in sync.

---

## 1. Create a New Project Brief

### Option A: Use the script (recommended)

```bash
python -m scripts .opencode/skills/para-project-brief "project-name" [--status active] [--priority medium]
```

The script:
1. Copies `templates/_project-brief.md` → `projects/<project-name>.md`
2. Sets frontmatter: `status: active`, `started: YYYY-MM-DD`
3. Optional: adds `priority: 🟡 Medium`
4. Optionally injects a row into Dashboard's Active Projects table
5. Adds a reference in today's daily log (if it exists)

### Option B: Manual creation

1. Copy `templates/_project-brief.md` → `projects/<name>.md`
2. Change `{{title}}` to the project name
3. Set `status: active` and `started: YYYY-MM-DD`
4. Add a link from today's daily log

---

## 2. Project Brief Structure

| Section | Purpose |
|---------|---------|
| **Metadata** | Status, priority, external links |
| **Brief** | One-paragraph summary of the project |
| **Status Progress** | Checklist: Research → Planning → In Progress → Review → Complete → Archived |
| **Edge Cases** | Important scenarios to account for |
| **Notes & Decisions** | Chronological log of key decisions |

---

## 3. Status Progress Checklist

Every project brief includes this checklist:

```markdown
## Status Progress

- [ ] Research / Discovery
- [ ] Planning
- [ ] In Progress
- [ ] Review
- [ ] Complete
- [ ] Archived
```

**Rules:**
- Only ONE item checked at a time
- When `Complete` is checked → set frontmatter `status: done`
- When `Archived` is checked → move file to `archives/`

---

## 4. Dashboard Integration

After creating a project:
1. Run `para-dashboard-sync` to update Dashboard counts
2. Manually add the project row to Dashboard's Active Projects table:

```markdown
| [[projects/project-name\|Project Name]] | 🟢 Active | 🟡 Medium | First action |
```

---

## 5. Naming Convention

- Use kebab-case: `my-new-feature.md`, `website-redesign.md`
- Keep it short (3-5 words max)
- No special characters, no spaces
- Can include version: `api-v2-migration.md`
