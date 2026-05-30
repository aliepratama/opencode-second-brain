---
name: para-link-validator
description: Wikilink integrity checker for the PARA second brain. Scans all markdown files, resolves [[wikilinks]], and reports broken or orphaned links. Use when user says "check links", "broken links", "validate links", "fix wikilinks", or "link check".
id: para-link-validator
title: PARA — Wikilink Validator
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [para, validation, wikilinks, maintenance]
---

# PARA — Wikilink Validator

> **Goal**: Find every broken `[[wikilink]]` in the vault before you
> discover them by clicking. Reports broken targets and orphaned files.

---

## 1. Run Link Validation

```bash
python -m scripts .opencode/skills/para-link-validator [--folder projects] [--verbose]
```

The script:
1. Walks every `.md` file in the vault
2. Extracts all `[[wikilinks]]` using regex
3. Resolves each link relative to the source file
4. Checks if the target file exists (with and without `.md`)
5. Reports broken links with source file + line number
6. Optionally reports orphaned files (no incoming links)

---

## 2. Link Resolution Rules

| Wikilink Pattern | Resolves To |
|-----------------|-------------|
| `[[projects/foo]]` | `projects/foo.md` |
| `[[../projects/foo]]` | Relative to current file |
| `[[../projects/foo\|Display Name]]` | Strip `|Display Name` |
| `[[../projects/foo#heading]]` | Strip `#heading` |

---

## 3. Output Format

```
============================================================
  PARA Link Validator
============================================================

[Broken Links]
  daily/2026-05-30.md:12  → [[projects/nonexistent]]
  areas/design.md:5       → [[../resources/missing-file]]

[Orphaned Files] (no incoming links)
  projects/abandoned-idea.md
  resources/old-research.md

------------------------------------------------------------
  Total: 45 files scanned, 2 broken links, 2 orphans
```

---

## 4. Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing `.md` extension | Wikilink without extension | Try with/without `.md` |
| Wrong folder | File moved but links not updated | Use `para-monthly-review` to bulk-update |
| Relative path broken | File moved, `../` no longer correct | Check relative path depth |
| Case mismatch | `Foo.md` vs `foo.md` (Windows OK, not cross-platform) | Normalize to lowercase |

---

## 5. Fixing Broken Links

After validation, fix broken links by:
1. Moving the target file to the expected location
2. Updating the wikilink to point to the actual location
3. Removing the link if the target no longer exists
4. For orphans: consider if the file is still needed
