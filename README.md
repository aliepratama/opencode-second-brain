# opencode-second-brain

A minimal, ready-to-use PARA second brain starter pack — designed to work with [OpenCode](https://opencode.ai) and [Obsidian](https://obsidian.md). Ships with 12 AI skills, 9 Python automation scripts, and a shared utility library.

## What This Is

A directory structure and set of templates for managing your projects, knowledge, and daily work using the **PARA method** (Projects, Areas, Resources, Archives) by Tiago Forte. Comes with an `AGENTS.md` that gives OpenCode clear instructions on how to interact with your vault, plus a full `.opencode/skills/` directory with automation scripts.

## Quick Start

1. **Clone or copy** this folder to your preferred location
2. **Open in Obsidian** — File → Open Vault → select this folder
3. **Read `AGENTS.md`** — this is the manual OpenCode uses to understand your vault
4. **Start logging** — press `Ctrl+Shift+D` in Obsidian for today's daily log
5. **Create a project** — copy `templates/_project-brief.md` to `projects/` and fill it in

## Structure

```
├── AGENTS.md                      ← OpenCode instruction manual
├── Dashboard.md                   ← Your landing page / navigation hub
├── README.md                      ← This file
├── .obsidian/                     ← Obsidian config (wikiLinks, daily notes, templates)
├── .opencode/                     ← OpenCode skills & automation
│   ├── opencode.jsonc             ← Agent config (enables all para-* skills)
│   └── skills/
│       ├── _shared/               ← Shared Python utility library (5 modules)
│       ├── para-vault/            ← 🧠 Orchestrator — dispatches to sub-skills
│       ├── para-daily-log/        ← 📅 Daily log workflow + script
│       ├── para-project-brief/    ← 📋 Project creation + script
│       ├── para-weekly-review/    ← 📊 Weekly review + script
│       ├── para-monthly-review/   ← 📆 Monthly review + archive script
│       ├── para-dashboard-sync/   ← 🔄 Dashboard auto-update script
│       ├── para-link-validator/   ← 🔗 Wikilink integrity checker
│       ├── para-frontmatter-check/← ✅ Frontmatter compliance checker
│       ├── para-search/           ← 🔍 Vault search & query engine
│       ├── para-mermaid/          ← 🎨 Mermaid diagram best practices
│       ├── para-md-validator/     ← 🧹 Markdown artifact auto-cleaner
│       └── para-table-formatter/  ← 📏 Error-free table formatting
├── projects/                      ← Active projects (one file per project)
├── areas/                         ← Ongoing responsibilities
├── resources/                     ← Reference material & research
├── archives/                      ← Completed projects
├── daily/                         ← Daily logs (YYYY-MM-DD.md)
├── weekly/                        ← Weekly reviews (YYYY-WNN.md)
└── templates/                     ← Reusable templates
    ├── _daily-log.md
    ├── _project-brief.md
    ├── _weekly-review.md
    └── _monthly-review.md
```

## How OpenCode Uses This

When you run OpenCode in this directory, it reads `AGENTS.md` and `.opencode/opencode.jsonc` for context and knows:

- Where to find your active projects, daily logs, and reference material
- How statuses work (`active → on-hold → done → archived`)
- What workflow to follow for creating projects, daily logs, and reviews
- That it must never modify templates without your permission
- Which skill to load for each user request (auto-dispatched by `para-vault`)

## Skills (12)

All skills are in `.opencode/skills/` and enabled via `opencode.jsonc`. The orchestrator (`para-vault`) auto-dispatches the right skill based on what you ask.

### Core Workflow Skills

| # | Skill | Trigger Phrase | Script |
|---|-------|---------------|--------|
| 1 | `para-vault` | "manage my vault", "second brain" | — |
| 2 | `para-daily-log` | "daily log", "today's log", "log my day" | Yes |
| 3 | `para-project-brief` | "new project", "start a project" | Yes |
| 4 | `para-weekly-review` | "weekly review", "progress this week" | Yes |
| 5 | `para-monthly-review` | "monthly review", "archive projects" | Yes |

### Utility Skills

| # | Skill | Trigger Phrase | Script |
|---|-------|---------------|--------|
| 6 | `para-dashboard-sync` | "sync dashboard", "update dashboard" | Yes |
| 7 | `para-link-validator` | "check links", "broken links" | Yes |
| 8 | `para-frontmatter-check` | "check frontmatter", "validate metadata" | Yes |
| 9 | `para-search` | "find in vault", "what's active" | Yes |

### Formatting & Quality Skills

| # | Skill | Trigger Phrase | Script |
|---|-------|---------------|--------|
| 10 | `para-mermaid` | "create diagram", "mermaid", "flowchart" | — |
| 11 | `para-md-validator` | "validate markdown", "clean document" | Yes |
| 12 | `para-table-formatter` | "format table", "fix table" | — |

### Skill Dependency Graph

```
para-vault (orchestrator)
│
├── para-daily-log ────────── depends: para-search, para-md-validator
├── para-project-brief ────── depends: para-dashboard-sync, para-table-formatter
├── para-weekly-review ────── depends: para-search, para-mermaid, para-md-validator
├── para-monthly-review ───── depends: para-dashboard-sync, para-link-validator
│
├── para-dashboard-sync ───── standalone utility
├── para-link-validator ───── standalone utility
├── para-frontmatter-check ─── standalone utility
├── para-search ────────────── standalone utility
├── para-mermaid ───────────── standalone (guidance only)
├── para-md-validator ──────── standalone utility
└── para-table-formatter ───── standalone (guidance only)
```

## Python Scripts

9 skills ship with automation scripts. Run them from the vault root:

```bash
# Create today's daily log with auto-linking
python -m scripts .opencode/skills/para-daily-log

# Create a new project brief
python -m scripts .opencode/skills/para-project-brief "My New Project" --priority high

# Generate weekly review (aggregates daily logs)
python -m scripts .opencode/skills/para-weekly-review

# Archive done projects (always dry-run first)
python -m scripts .opencode/skills/para-monthly-review --dry-run
python -m scripts .opencode/skills/para-monthly-review

# Sync dashboard counts
python -m scripts .opencode/skills/para-dashboard-sync

# Validate all wikilinks
python -m scripts .opencode/skills/para-link-validator --verbose

# Check frontmatter compliance
python -m scripts .opencode/skills/para-frontmatter-check --fix

# Search vault
python -m scripts .opencode/skills/para-search --status active
python -m scripts .opencode/skills/para-search --tag project --since 2026-05-01

# Validate markdown for AI artifacts
python -m scripts .opencode/skills/para-md-validator daily/ --fix
```

### Shared Library

All scripts share a common utility library in `_shared/`:

| Module | What it does |
|--------|-------------|
| `vault.py` | Find vault root, list files, date utilities |
| `frontmatter.py` | Parse/validate/write YAML frontmatter |
| `wikilinks.py` | Extract/resolve/validate `[[wikilinks]]` |
| `dashboard.py` | Parse/update Dashboard.md tables |

Import from any script:
```python
from _shared import vault, frontmatter, wikilinks, dashboard
```

## Review Cadence

| Frequency | Action | Script |
|-----------|--------|--------|
| Daily | Log progress, blockers, and insights | `para-daily-log` |
| Weekly | Review accomplishments, set next-week priorities | `para-weekly-review` |
| Monthly | Archive completed projects, review all areas | `para-monthly-review` |

## Configuration

- **`.obsidian/app.json`**: wikiLinks enabled, relative paths, symlink support
- **`.obsidian/daily-notes.json`**: auto-generate to `daily/` using `_daily-log.md` template
- **`.obsidian/templates.json`**: template folder set to `templates/`
- **`.opencode/opencode.jsonc`**: all `para-*` skills allowed for default agent

## Developer Edition

This repo also includes a **Developer Edition** — the same PARA foundation extended with developer-specific workflows: Architecture Decision Records, code snippet management, bug tracking, and tech learning journals.

### What's Different

| Feature | General Edition | Developer Edition |
|---------|----------------|-------------------|
| **Extra folders** | — | `adrs/`, `snippets/`, `learnings/`, `errors/` |
| **Templates** | 4 (daily, project, weekly, monthly) | + `_adr.md`, `_bug-tracker.md`, `_code-snippet.md`, `_tech-learning.md`, `_sprint-review.md` |
| **Skills** | 12 PARA + formatting | + `para-adr`, `para-snippet`, `para-bug-tracker`, `para-dev-log` |
| **Daily log** | Progress, blockers, insights | + Commits, PRs, code reviews |
| **Status flows** | `active → on-hold → done → archived` | + bugs: `open → investigating → fixed → verified → closed` |

### Quick Install

```bash
# Fresh dev vault
python editions/dev/setup.py ~/my-dev-brain --init

# Add dev extras to existing vault
python editions/dev/setup.py ~/my-existing-vault --merge
```

Or copy manually:
```bash
cp -r editions/dev ~/my-dev-brain
```

See `editions/dev/README.md` for full documentation.

## License

MIT — use it, fork it, share it.
