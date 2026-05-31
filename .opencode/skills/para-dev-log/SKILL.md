---
name: para-dev-log
description: Developer daily log workflow. Creates dev-focused daily entries with commits, PRs, code review notes, and architectural decisions. Extends para-daily-log with developer-specific sections. Use when user says "dev log", "what I coded today", "log my commits", "daily coding log", or "log my dev day".
id: para-dev-log
title: PARA Developer — Daily Dev Log
version: 1.0
updated: 2026-05-31
author: OpenCode
domain: [dev, daily, logging, tracking]
depends_on:
  - para-md-validator
---

# PARA Developer — Daily Dev Log

> **Goal**: Track what you coded today — commits, PRs, code reviews,
> decisions made, and bugs encountered. The developer's version of the
> standard daily log with extra technical sections.

---

## 1. Create a Dev Daily Log

```bash
python -m scripts .opencode/skills/para-dev-log
```

The script:
1. Creates `daily/YYYY-MM-DD.md` with developer-specific sections
2. Auto-links recent projects and ADRs
3. Adds Commits, PRs, Code Reviews sections
4. Includes standard Daily Summary

---

## 2. Dev Daily Log Sections

| Section | Purpose | Example |
|---------|---------|---------|
| **Commits** | Git hashes and short descriptions | `abc1234 - fix: handle null in parser` |
| **PRs** | Pull requests opened/reviewed/merged | `#42 - WIP: auth refactor` |
| **Code Reviews** | Reviews done today with status | `PR #38 - approved with nits` |
| **Progress** | What got built today | Feature X: completed endpoint |
| **Decisions** | Architectural decisions made | Chose zod over joi → `[[../adrs/0003]]` |
| **Bugs** | Bugs found or fixed | Memory leak in parser → `[[../errors/xxx]]` |
| **Blockers** | What's holding things up | CI failing on Windows |
| **Insights** | Lessons, discoveries, patterns | Redis pipelining reduced latency 10x |
| **Next Actions** | For tomorrow | Finish auth middleware |

---

## 3. Commit Format in Daily Log

```markdown
## Commits
- `a1b2c3d` feat: add user auth middleware ([[../projects/auth-v2]])
- `e4f5g6h` fix: handle null in response parser
- `i7j8k9l` refactor: extract validation to shared
```

Use `feat/fix/refactor/chore/perf/test/docs` type prefixes.

---

## 4. PR Tracking

```markdown
## PRs
- #42 opened: Auth middleware refactor [WIP]
- #38 reviewed: Fix memory leak [APPROVED]
- #39 merged: Add retry logic for HTTP client
```

Status tags: `[WIP]` `[REVIEWING]` `[APPROVED]` `[MERGED]` `[CLOSED]`

---

## 5. Code Review Notes

```markdown
## Code Reviews
- [x] PR #38 — approved, left 3 nits
- [x] PR #40 — requested changes: split into smaller commits
- [ ] PR #44 — needs second pass
```

---

## 6. Decisions Section

Cross-reference ADRs created or referenced today:

```markdown
## Decisions
- Chose Redis for cache layer → [[../adrs/0008-redis-caching]]
- Rejected GraphQL for now → too complex for current scale
```

---

## 7. Daily Summary (Required)

Same as general edition but dev-focused:

```markdown
## Daily Summary

### Completed
- [x] Auth middleware (3 commits) — [[../projects/auth-v2]]
- [x] Reviewed 2 PRs
- [x] Fixed parser null bug → [[../errors/null-parser]]

### In Progress / Pending
- [ ] Finish Redis cache implementation
- [ ] Review PR #44
```

---

## 8. Weekly Aggregation Tips

At end of week, count your dev stats:
- Total commits: 18
- PRs merged: 4
- Bugs fixed: 2
- ADRs created: 1
- Lines changed: +340 / -120

Use these in your sprint review.
