---
name: para-daily-log
description: Daily log workflow for the PARA second brain. Creates daily entries from template, auto-links recent projects, enforces Daily Summary section. Use when user says "daily log", "today's log", "create log entry", "what happened today", or "log my day".
id: para-daily-log
title: PARA — Daily Log Workflow
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, daily, logging, tracking]
depends_on:
  - para-search
  - para-md-validator
---

# PARA — Daily Log Workflow

> **Goal**: Create consistent, well-linked daily logs that capture progress,
> blockers, insights, and next actions. Every log ends with a Daily Summary.

---

## 1. Create Today's Daily Log

### Option A: Use the script (recommended)

```bash
python -m scripts .opencode/skills/para-daily-log
```

The script:
1. Loads `templates/_daily-log.md`
2. Substitutes `{{date:YYYY-MM-DD}}` with today's date
3. Sets `tags: #daily/YYYY-MM`
4. Auto-links recently modified projects (from `projects/`)
5. Writes to `daily/YYYY-MM-DD.md`
6. Validates the Daily Summary section is present

### Option B: Manual creation

1. Copy `templates/_daily-log.md` to `daily/YYYY-MM-DD.md`
2. Update `{{date:YYYY-MM-DD}}` → today
3. Update `{{date:YYYY-MM}}` → current month
4. Fill in each section manually

---

## 2. Daily Log Sections

| Section | Purpose | Format |
|---------|---------|--------|
| **Progress** | What got done today | Bullet list with issue/project refs |
| **Blockers** | What's holding things up | Bullet list, mention project |
| **Insights** | Lessons, decisions, discoveries | Free-form bullets |
| **References** | Links to projects, resources | `[[../projects/xxx.md]]` |
| **Next Actions** | For tomorrow, prioritized | `- [ ] Task` checklist |
| **Daily Summary** | **REQUIRED** — completed + in-progress | Checklists with `[x]` and `[ ]` |

---

## 3. Daily Summary Format (Required)

```markdown
## Daily Summary

### Completed
- [x] Task A — [[projects/foo]]
- [x] Task B — #issue-42

### In Progress / Pending
- [ ] Task C — waiting on review
- [ ] Task D — follow up tomorrow
```

**Rule**: If the Daily Summary section is missing, add it. Never leave a daily log without it.

---

## 4. Auto-Linking Logic

When creating a daily log, automatically link:
1. All projects modified in the last 3 days → `[[../projects/xxx.md]]`
2. Any project with `status: active` → list in References
3. Previous day's "Next Actions" → carry over to today's "Next Actions"

---

## 5. Validation

After creating a daily log, run `para-md-validator` to check for:
- Stray Chinese characters
- Emoji in tables
- Broken Mermaid syntax
- Backslash-n in code blocks
