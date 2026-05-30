---
name: para-table-formatter
description: Markdown table formatting best practices for the PARA second brain. Covers alignment, escaping, column consistency, and anti-error rules for creating clean, renderer-compatible tables. Use when user says "format table", "create table", "fix table", "table alignment", or "markdown table".
id: para-table-formatter
title: PARA — Markdown Table Formatter
version: 1.0
updated: 2026-05-30
author: OpenCode
domain: [formatting, table, markdown, documentation]
---

# PARA — Markdown Table Formatter

> **Goal**: Create consistently formatted, error-free Markdown tables.
> Poorly formatted tables break in Obsidian, GitHub, PDF exports, and Google Docs.

---

## 1. Table Structure Rules

### Minimum Valid Table
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

### Alignment Syntax
```markdown
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| text     | text     | 123      |
```

---

## 2. Cell Content Rules

| Forbidden in Cells | Replace With | Why |
|-------------------|-------------|-----|
| `✅` `❌` `🟠` `🟡` | `Done`, `Yes`, `No`, text | Breaks PDF/Google Docs export |
| `\n` newline | ` - ` or ` / ` | Tables don't support multi-line cells |
| `|` pipe character | `\|` (escape) or remove | Breaks column parsing |
| Empty cell (no content) | `—` or `N/A` | Some renderers collapse empty cells |
| Very long text (>50 chars) | Summary + see note | Breaks table layout |

---

## 3. Column Consistency Rules

Every row MUST have the same number of columns:

```markdown
❌ BROKEN:                          ✅ FIXED:
| A | B | C |                       | A | B | C |
|---|---|---|                       |---|---|---|
| 1 | 2 |                           | 1 | 2 | — |
| x | y | z | w |                   | x | y | z |
```

---

## 4. Common Table Patterns

### Status Table
```markdown
| Project | Status | Priority |
|---------|--------|----------|
| Alpha   | 🟢 Active | 🟡 Medium |
```
Better (export-safe):
```markdown
| Project | Status | Priority |
|---------|--------|----------|
| Alpha   | Active | Medium   |
```

### Numbered Table
```markdown
| # | Item | Detail |
|:-:|:-----|:-------|
| 1 | First | Detail |
| 2 | Second | Detail |
```

### Checklist Table
```markdown
| Task | Owner | Done |
|------|-------|:----:|
| Design | Alie | Yes |
| Review | Bob | No  |
```

---

## 5. Anti-Error Checklist

Before finalizing any table:

```
[ ] All rows have the same number of columns?
[ ] No emoji in cells? (use text instead)
[ ] No pipe | characters inside cells? (escape with \|)
[ ] No empty cells? (use — or N/A)
[ ] All column widths consistent?
[ ] Alignment markers (:--, :--:, --:) correctly placed?
[ ] Separator row present after header?
```

---

## 6. Obsidian-Specific Notes

- Obsidian's live preview is **more forgiving** than standard markdown
- PDF export is **more strict** — always test with export
- Use `|:-:|` for centered columns, `|:---|` for left-aligned
- Avoid HTML inside tables (`<br>`, `<span>`) — breaks in some contexts
