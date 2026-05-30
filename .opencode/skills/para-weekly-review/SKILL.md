---
name: para-weekly-review
description: Weekly review workflow for the PARA second brain. Aggregates daily logs, identifies patterns, sets next-week priorities. Use when user says "weekly review", "progress this week", "end of week", or "what got done this week".
id: para-weekly-review
title: PARA — Weekly Review Workflow
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, review, weekly, reflection, planning]
depends_on:
  - para-search
  - para-mermaid
  - para-md-validator
---

# PARA — Weekly Review Workflow

> **Goal**: Aggregate the week's daily logs into a structured review.
> Identify patterns, blockers, and set clear priorities for next week.

---

## 1. Generate a Weekly Review

### Option A: Use the script (recommended)

```bash
python -m scripts .opencode/skills/para-weekly-review
```

The script:
1. Determines the current ISO week (YYYY-WNN)
2. Finds all daily logs from Monday to Sunday
3. Extracts Progress, Blockers, Insights from each daily
4. Aggregates into summary sections
5. Identifies recurring blockers
6. Carries over incomplete "Next Actions"
7. Populates `templates/_weekly-review.md`
8. Writes to `weekly/YYYY-WNN.md`

### Option B: Manual creation

1. Copy `templates/_weekly-review.md` → `weekly/YYYY-WNN.md`
2. Review each daily log manually
3. Fill in all sections

---

## 2. Weekly Review Sections

| Section | Purpose | Source |
|---------|---------|--------|
| **Accomplished** | What got done this week | Extract "Progress" from dailies |
| **In Progress** | Still in motion | Extract "Next Actions" unchecked |
| **On Hold / Blocked** | Stalled and why | Extract "Blockers" from dailies |
| **Insights & Patterns** | Recurring themes, lessons | Extract "Insights" from dailies |
| **Next Week Focus** | Top 3 priorities | Manual or from incomplete tasks |
| **Archive Check** | Projects ready to archive | Check `status: done` projects |

---

## 3. Pattern Detection

When aggregating daily logs, look for:

| Pattern | Signal |
|---------|--------|
| Same blocker appearing 3+ days | Escalation needed |
| "Next Actions" carry-over 3+ days | Task too big — break down |
| No progress on a project all week | Project may be `on-hold` |
| Multiple completed items on same project | Consider marking `done` |

---

## 4. Post-Review Actions

After creating the weekly review:
1. Run `para-dashboard-sync` to refresh counts
2. Move any `done` projects to `archives/` (or flag for monthly review)
3. Set top 3 priorities for next week
4. Validate output with `para-md-validator`
