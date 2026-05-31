---
name: para-snippet
description: Code snippet manager for the developer second brain. Save, tag, search, and organize reusable code snippets by language and pattern. Use when user says "save snippet", "store code", "find snippet", "search code by language", or "show me that X snippet".
id: para-snippet
title: PARA Developer — Code Snippet Manager
version: 1.0
updated: 2026-05-31
author: OpenCode
domain: [dev, code, snippet, reference]
---

# PARA Developer — Code Snippet Manager

> **Goal**: Save context-rich code snippets so you never have to Google
> the same thing twice. Every snippet includes purpose, usage, and gotchas.

---

## 1. Save a Snippet

### Use the script

```bash
python -m scripts .opencode/skills/para-snippet add "Async HTTP retry" --lang python --tags "async,http,retry"
```

The script:
1. Creates `snippets/snippet-name.md` from `templates/_code-snippet.md`
2. Sets frontmatter: language, tags, date
3. Prompts for code content via stdin or env

### Manual creation

1. Copy `templates/_code-snippet.md` → `snippets/async-http-retry.md`
2. Fill in: Purpose, Code, Usage, Notes
3. Set `language` and `tags` in frontmatter

---

## 2. Search Snippets

```bash
python -m scripts .opencode/skills/para-snippet search --lang python --tag "async"
python -m scripts .opencode/skills/para-snippet search --query "retry logic"
```

Filters: `--lang` (language), `--tag` (tag keyword), `--query` (full-text).

---

## 3. Snippet Structure

| Section | Purpose |
|---------|---------|
| **Purpose** | What this snippet does, one sentence |
| **Code** | The code block with language fence |
| **Usage** | How to use, parameters, returns |
| **Notes** | Edge cases, dependencies, gotchas |

### Example frontmatter
```yaml
---
tags: snippet
language: python
tags: [async, http, client, retry]
source: https://docs.python.org/3/library/asyncio.html
date: 2026-05-31
---
```

---

## 4. Tag Convention

Use short, reusable tags:

| Tag | Category | Examples |
|-----|----------|----------|
| Language | `python`, `go`, `js`, `ts`, `rust`, `sql` | Always include as first tag |
| Pattern | `async`, `error-handling`, `testing`, `auth` | Design pattern or concern |
| Framework | `fastapi`, `react`, `django`, `nextjs` | Library/framework specific |
| Context | `snippet`, `recipe`, `reference` | Type of content |

---

## 5. Snippet Naming

```
kebab-case-use-case-language.md

Examples:
  async-http-client-python.md
  error-middleware-go.md
  auth-jwt-fastapi.md
  sql-migration-postgres.md
```

Keep under 5 words. Make it searchable by skimming filenames.
