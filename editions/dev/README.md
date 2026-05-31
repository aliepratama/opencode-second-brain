# Second Brain — Developer Edition

A developer-focused PARA second brain starter pack. Includes extensions for tracking architecture decisions, code snippets, bugs, and tech learnings alongside standard project management.

This is the **Developer Edition** of [opencode-second-brain](https://github.com/aliepratama/opencode-second-brain). It extends the general-purpose starter with developer-specific workflows.

## Quick Start

### Option A: Setup script (recommended)

```bash
python editions/dev/setup.py /path/to/my-dev-vault --init
```

This creates a complete developer vault at the target path with all folders, templates, and skills pre-configured.

### Option B: Manual copy

```bash
cp -r editions/dev /path/to/my-dev-vault
cd /path/to/my-dev-vault
```

Then copy the shared skills from the repo root:
```bash
cp -r ../.opencode/skills .opencode/
cp ../.opencode/opencode.jsonc .opencode/
```

### Option C: Overlay on existing general vault

```bash
python editions/dev/setup.py --merge /path/to/existing-vault
```

Adds developer folders and templates to an existing general edition vault.

---

## What's Different from General Edition

| Feature | General Edition | Developer Edition |
|---------|----------------|-------------------|
| **Folders** | projects, areas, resources, archives | + `adrs/`, `snippets/`, `learnings/` |
| **Templates** | daily, project, weekly, monthly | + ADR, bug-tracker, code-snippet, tech-learning, sprint-review |
| **Skills** | 12 PARA + formatting skills | + para-adr, para-snippet, para-bug-tracker, para-dev-log |
| **Daily log** | Progress, blockers, insights | + Commits, PRs, code reviews |
| **Project brief** | Generic metadata | + Tech stack, repo link, language |
| **Status flow** | active → on-hold → done → archived | Same + bugs: open → investigating → fixed → verified |

---

## Developer Folders

| Folder | Purpose | Template |
|--------|---------|----------|
| `adrs/` | Architecture Decision Records | `templates/_adr.md` |
| `snippets/` | Reusable code snippets by language | `templates/_code-snippet.md` |
| `learnings/` | Tech learning journal entries | `templates/_tech-learning.md` |
| `errors/` | Bug reports and debugging notes | `templates/_bug-tracker.md` |

---

## Developer Skills (4 new)

| Skill | Trigger Phrase | What it Does |
|-------|---------------|-------------|
| `para-adr` | "create ADR", "architecture decision", "record decision" | Generate ADR from template, link to project, manage decision log |
| `para-snippet` | "save snippet", "find snippet", "search code" | Save, tag, and search code snippets by language and pattern |
| `para-bug-tracker` | "log bug", "track error", "bug report" | Create bug entries with reproduction steps, track to resolution |
| `para-dev-log` | "dev log", "what did I code today", "log commits" | Enhanced daily log: auto-links commits, PRs, code review notes |

---

## Python Scripts

```bash
# Create an Architecture Decision Record
python -m scripts .opencode/skills/para-adr "Use PostgreSQL for primary store"

# Save a code snippet
python -m scripts .opencode/skills/para-snippet add "Async HTTP client" --lang python --tags "async,http"

# Search snippets
python -m scripts .opencode/skills/para-snippet search --lang python --tag "async"

# Log a bug
python -m scripts .opencode/skills/para-bug-tracker new "Memory leak in parser" --severity high --lang go

# Create developer daily log
python -m scripts .opencode/skills/para-dev-log
```

---

## Template Reference

### ADR (`_adr.md`)
MADR format: Context → Options → Decision → Consequences. One ADR per architectural decision.

### Bug Tracker (`_bug-tracker.md`)
Full debugging workflow: Environment → Reproduction → Root Cause → Fix → Prevention.

### Code Snippet (`_code-snippet.md`)
Purpose + Code + Usage + Notes. Tagged by language and pattern.

### Tech Learning (`_tech-learning.md`)
Feynman-inspired: Mental Model → Key Insight → Code Examples → Trade-offs.

### Sprint Review (`_sprint-review.md`)
Sprint retrospective: Goal → Commitments → Blockers → What Went Well/Improve.

---

## License

MIT — same as the base [opencode-second-brain](https://github.com/aliepratama/opencode-second-brain).
