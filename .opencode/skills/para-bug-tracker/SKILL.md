---
name: para-bug-tracker
description: Bug and error tracking workflow for the developer second brain. Creates structured bug reports with reproduction steps, environment details, and resolution tracking. Use when user says "log bug", "track error", "bug report", "debug this", "document this error", or "I found a bug".
id: para-bug-tracker
title: PARA Developer — Bug & Error Tracking
version: 1.0
updated: 2026-05-31
author: OpenCode
domain: [dev, bug, debugging, error, tracking]
---

# PARA Developer — Bug & Error Tracking

> **Goal**: Turn every bug into a learning opportunity. Document
> reproduction steps, root cause, and fix so you never debug the same
> problem twice.

---

## 1. Create a Bug Report

### Use the script

```bash
python -m scripts .opencode/skills/para-bug-tracker new "Memory leak in parser" \
    --severity high --lang go --project "compiler"
```

The script:
1. Creates `errors/bug-short-name.md` from `templates/_bug-tracker.md`
2. Sets frontmatter: status, severity, language, project, date
3. Prints link for daily log reference

### Manual creation

1. Copy `templates/_bug-tracker.md` → `errors/memory-leak-parser.md`
2. Fill in: Environment, Error, Reproduction, Expected vs Actual
3. Set `status: open` and appropriate severity

---

## 2. Bug Status Lifecycle

```
open → investigating → fixed → verified → closed
```

| Status | Meaning | When to Use |
|--------|---------|------------|
| `open` | Reported, not yet investigated | Initial creation |
| `investigating` | Actively debugging | You have a hypothesis |
| `fixed` | Fix applied, unverified | Code committed or deployed |
| `verified` | Fix confirmed working | Tested and confirmed |
| `closed` | Resolved and documented | Archive-worthy |

---

## 3. Bug Report Structure

| Section | Purpose | Priority |
|---------|---------|----------|
| **Environment** | OS, runtime, version, deps | Critical for reproduction |
| **Error / Symptom** | Error message, stack trace | Critical — the first thing others see |
| **Reproduction Steps** | Step-by-step to trigger | Critical — numbered list |
| **Expected vs Actual** | What should happen vs what happens | High |
| **Root Cause** | The actual underlying cause | Fill after investigation |
| **Fix** | The solution with code | Fill after fixing |
| **Prevention** | Test, lint rule, guard clause | Fill after verified |

---

## 4. Severity Levels

| Severity | Meaning | Examples |
|----------|---------|----------|
| `critical` | Production down, data loss | Crash on startup, DB corruption |
| `high` | Major feature broken | Login fails, payment broken |
| `medium` | Feature degraded | Slower rendering, missing label |
| `low` | Cosmetic, minor | Wrong color, typo |

---

## 5. Naming Convention

```
errors/brief-descriptive-name.md

Examples:
  errors/null-pointer-auth-middleware.md
  errors/memory-leak-image-parser.md
  errors/race-condition-websocket.md
```

Keep it descriptive so you can find bugs by filename.
