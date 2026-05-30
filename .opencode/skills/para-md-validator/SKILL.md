---
name: para-md-validator
description: Auto-validator that cleans AI-generated markdown artifacts: stray Chinese characters, emoji in tables, backslash-n in Mermaid, ampersand, broken numbering. Essential dependency for other skills that generate markdown output. Use when user says "validate markdown", "clean document", "check output", "fix formatting", or "remove Chinese characters".
id: para-md-validator
title: PARA — Markdown Output Validator
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [validation, markdown, formatting, cleaning]
---

# PARA — Markdown Output Validator

> **Goal**: Automatically detect and fix common AI output artifacts.
> AI models (especially those trained on Chinese corpora) often leave
> behind stray characters, broken Mermaid syntax, and table-breaking emoji.

---

## 1. Run Validation

```bash
# Check a single file
python -m scripts .opencode/skills/para-md-validator path/to/file.md

# Check all files in a folder
python -m scripts .opencode/skills/para-md-validator daily/

# Auto-fix when possible
python -m scripts .opencode/skills/para-md-validator path/to/file.md --fix
```

The script checks 5 categories automatically.

---

## 2. What Gets Checked

| # | Category | Detects | Example |
|---|----------|---------|---------|
| 1 | **Chinese characters** | `依据` `设置` `信息` `自动` in non-Chinese text | `wajib依据 peraturan` |
| 2 | **Emoji in tables** | `✅` `❌` `🟠` `🟡` inside markdown table cells | `| Status | ✅ Done |` |
| 3 | **Backslash-n in Mermaid** | `\n` inside Mermaid code block nodes | `"Line1\nLine2"` |
| 4 | **Numbering in Mermaid nodes** | `"1."` `"1a."` at start of node text | `"1. Prompt"` |
| 5 | **Special chars in Mermaid** | `&` `/` `%` inside node text | `"Confirm & Send"` |

---

## 3. Quick Fix Reference

```
FOUND                →  REPLACE WITH
─────────────────────────────────────────────
依据                 →  based on / according to
设置                 →  setting / configure
信息                 →  information
自动                 →  automatic
─────────────────────────────────────────────
✅ in table          →  Done / Yes / [Y]
❌ in table          →  Not done / No / [N]
🟠 🟡 in table      →  text label
─────────────────────────────────────────────
\n in Mermaid node   →  " - " or " — "
"1. Text" in node    →  "Text - Regular"
& in node            →  "and"
/ in node            →  "or"
% in node            →  "percent"
```

---

## 4. Output Format

```
============================================================
  PARA Markdown Validator
  File: daily/2026-05-30.md
============================================================

  [Emoji in tables]
  Line 45: Table cell contains ✅ → replace with 'Done'
  Line 52: Table cell contains ❌ → replace with 'Not done'

  [Chinese characters]
  Line 78: Found '依据' → replace with 'based on'

  [Backslash-n in Mermaid]
  Line 135: Found '\n' in node → replace with ' - '

  [Numbering in Mermaid nodes]
  OK

  [Special characters in Mermaid]
  OK

------------------------------------------------------------
  [FAIL] 3 issue(s) found. Fix before finalizing.
```

---

## 5. Integration

This skill is a **dependency** for other skills:

```yaml
depends_on:
  - para-md-validator
```

Skills that depend on this automatically:
1. Know how to validate their output before finalizing
2. Have access to the quick fix cheatsheet
3. Can invoke the validation script

Skills using this:
- `para-daily-log` — validates daily log before saving
- `para-weekly-review` — validates review before saving
