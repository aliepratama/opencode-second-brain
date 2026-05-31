# Second Brain — OpenCode Agent Manual (Developer Edition)

This vault follows the **PARA method** (Projects, Areas, Resources, Archives) with **developer-specific extensions**: ADRs, code snippets, bug tracking, and tech learning journals.

## 1. Directory Rules

| Folder | Purpose | Frontmatter |
|--------|---------|-------------|
| `projects/` | Active coding projects | `tags: project`, `status: active`, `language`, `repo` |
| `areas/` | Ongoing dev responsibilities | `tags: area`, `status: active` |
| `resources/` | Tech references, docs | `tags: resource`, `type: reference\|research` |
| `archives/` | Completed/cancelled projects | Moved from `projects/` when done |
| `adrs/` | Architecture Decision Records | `tags: adr`, `status: proposed\|accepted\|deprecated` |
| `snippets/` | Reusable code snippets | `tags: snippet`, `language`, `tags` |
| `learnings/` | Tech learning journal | `tags: learning`, `topic`, `status: learning\|understood\|mastered` |
| `errors/` | Bug/error tracking | `tags: bug`, `status: open\|investigating\|fixed\|verified` |
| `daily/` | Daily dev logs (`YYYY-MM-DD.md`) | `tags: #daily/YYYY-MM` |
| `weekly/` | Sprint/weekly reviews | `tags: #review/weekly` |
| `templates/` | Reusable templates (prefixed `_`) | Do NOT modify without explicit request |

## 2. Status Convention

### Projects
| Status | Meaning | Location |
|--------|---------|----------|
| `active` | Currently working on | `projects/` |
| `on-hold` | Paused, waiting for something | `projects/` |
| `done` | Fully completed | `projects/` → move to `archives/` |
| `archived` | No longer active | `archives/` |

### Bugs
| Status | Meaning |
|--------|---------|
| `open` | Reported, not yet investigated |
| `investigating` | Actively debugging |
| `fixed` | Fix applied, unverified |
| `verified` | Fix confirmed working |
| `closed` | Resolved and documented |

### ADRs
| Status | Meaning |
|--------|---------|
| `proposed` | Suggested, under discussion |
| `accepted` | Approved and active |
| `deprecated` | No longer applies |
| `superseded` | Replaced by another ADR |

### Learnings
| Status | Meaning |
|--------|---------|
| `learning` | Actively studying |
| `understood` | Can apply independently |
| `mastered` | Can teach others |

## 3. Agent Behavior Rules

1. **Search First**: Search all folders before answering vault questions.
2. **Status Gate**: When mentioning a project or bug, always include its status.
3. **No Template Edits**: Never modify `templates/_*.md` unless explicitly asked.
4. **Preserve Dashboard**: Never delete or restructure `Dashboard.md`.
5. **Link Everything**: Use `[[wikilinks]]` between related files.
6. **Commit References**: When logging daily work, reference git commit hashes.
7. **ADR Links**: Every project brief should link to relevant ADRs.
8. **Snippet Convention**: Code snippets use language-specific code fences (```python, ```go).
9. **Bug Documentation**: Always include reproduction steps before suggesting fixes.
10. **Dashboard Sync**: Update Dashboard when statuses change.

## 4. Workflow Rules

### Starting a New Project
1. Copy `templates/_project-brief.md` to `projects/project-name.md`
2. Fill in: tech stack, repo link, language
3. Add to Dashboard active projects table
4. Create ADR for key architectural decisions
5. Reference in today's dev log

### Daily Dev Log
1. Generate via `Ctrl+Shift+D` or `python -m scripts para-dev-log`
2. Include: commits (with hashes), PRs reviewed, decisions made
3. Link to project briefs, ADRs, bug reports
4. Complete the Daily Summary section

### ADR Workflow
1. Use `templates/_adr.md` for every significant architectural decision
2. Number sequentially: `adrs/0001-`, `adrs/0002-`, etc.
3. Status changes: `proposed → accepted` after review
4. Never edit a published ADR — supersede with a new one

### Bug Tracking
1. Create `errors/bug-short-name.md` from `templates/_bug-tracker.md`
2. Track status: `open → investigating → fixed → verified → closed`
3. Include reproduction steps and environment details
4. Link fix commits in the resolution section

### Sprint Review
1. Use `templates/_sprint-review.md` at end of each sprint
2. Review commitments vs completed
3. Document what went well and what to improve
4. Carry over unfinished work

## 5. Linking Conventions

- **Wikilinks**: `[[foldername/filename]]` for internal links
- **Daily → Project**: `[[../projects/project-name.md]]`
- **Project → ADR**: `[[../adrs/0001-decision-name]]`
- **Bug → Project**: `[[../projects/project-name]]`
- **Dashboard → Daily**: `[[daily/YYYY-MM-DD]]`

## 6. Developer-Specific Frontmatter

Projects should include:
```yaml
---
tags: project
status: active
started: YYYY-MM-DD
language: python|go|javascript|etc
repo: github.com/user/repo
tech_stack: [fastapi, postgres, redis]
---
```

Code snippets should include:
```yaml
---
tags: snippet
language: python
tags: [async, http, client]
source: URL or reference
date: YYYY-MM-DD
---
```
