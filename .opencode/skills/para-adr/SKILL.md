---
name: para-adr
description: Architecture Decision Record workflow for the developer second brain. Creates ADRs from MADR template, manages status lifecycle, and links decisions to projects. Use when user says "create ADR", "architecture decision", "record decision", "log design decision", or "why did we choose X".
id: para-adr
title: PARA Developer — Architecture Decision Records
version: 1.0
updated: 2026-05-31
author: OpenCode
domain: [dev, architecture, decision, documentation]
---

# PARA Developer — Architecture Decision Records

> **Goal**: Document every significant architectural decision with context,
> options considered, and consequences. ADRs are immutable once accepted.

---

## 1. Create an ADR

### Use the script

```bash
python -m scripts .opencode/skills/para-adr "Use PostgreSQL for primary store" [--status proposed]
```

The script:
1. Determines the next ADR number (0001, 0002, ...)
2. Copies `templates/_adr.md` → `adrs/NNNN-title.md`
3. Fills in date, title, status
4. Prints link for daily log reference

### Manual creation

1. Copy `templates/_adr.md` → `adrs/0001-use-postgres.md`
2. Fill in Context, Drivers, Options, Decision, Consequences
3. Set `status: proposed`
4. Link from relevant project brief

---

## 2. ADR Structure (MADR format)

| Section | Purpose |
|---------|---------|
| **Context and Problem Statement** | Why this decision is needed |
| **Decision Drivers** | Forces, concerns, constraints |
| **Considered Options** | Table: all options evaluated |
| **Decision Outcome** | Chosen option + justification |
| **Consequences** | What becomes easier/harder |
| **Pros and Cons** | Detailed comparison per option |

---

## 3. ADR Status Lifecycle

```
proposed → accepted → deprecated → superseded by ADR-NNNN
```

**Rules:**
- **proposed**: Under discussion. Default for new ADRs.
- **accepted**: Approved and active. Change only via new ADR.
- **deprecated**: No longer applies. Preserve for historical context.
- **superseded**: Replaced by another ADR. Add `superseded_by: ADR-NNNN` to frontmatter.

**Never edit** a published ADR's content. Create a new ADR and supersede the old one.

---

## 4. Naming Convention

```
adrs/NNNN-kebab-case-title.md

Examples:
  adrs/0001-use-postgres-over-mysql.md
  adrs/0002-adopt-event-sourcing.md
  adrs/0003-migrate-to-typescript.md
```

Number sequentially. Pad to 4 digits.

---

## 5. When to Create an ADR

| Situation | Create ADR? |
|-----------|------------|
| Choosing a database | Yes |
| Selecting a framework/library | Yes |
| Architectural pattern change | Yes |
| API contract decision | Yes |
| Small implementation detail | No — code comment is enough |
| Obvious best practice | No |
| Experimental spike | Yes if it becomes permanent |

---

## 6. Linking ADRs

```markdown
<!-- In a project brief: -->
## Architecture Decisions
- [[../adrs/0001-use-postgres]]
- [[../adrs/0004-auth-strategy]]

<!-- In a daily dev log: -->
- Decided on caching strategy → [[../adrs/0007-redis-cache-layers]]
```
