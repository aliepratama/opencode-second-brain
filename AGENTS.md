# Second Brain — OpenCode Agent Manual

This vault uses the **PARA method** (Projects, Areas, Resources, Archives) combined with daily notes. Open this vault in Obsidian for the best experience, but the agent works with plain Markdown.

## 1. Directory Rules

| Folder | Purpose | Frontmatter |
|--------|---------|-------------|
| `projects/` | Active projects — one file per project | `tags: project`, `status: active` |
| `areas/` | Ongoing responsibilities (no end date) | `tags: area`, `status: active` |
| `resources/` | Reference material and research | `tags: resource`, `type: reference\|research` |
| `archives/` | Completed or cancelled projects | Moved from `projects/` when done |
| `daily/` | Daily logs (`YYYY-MM-DD.md`) | `tags: #daily/YYYY-MM` |
| `weekly/` | Weekly reviews (`YYYY-WNN.md`) | `tags: #review/weekly` |
| `templates/` | Reusable templates (prefixed `_`) | Do NOT modify without explicit request |

## 2. Status Convention

| Status | Meaning | Location |
|--------|---------|----------|
| `active` | Currently working on | `projects/` |
| `on-hold` | Paused, waiting for something | `projects/` |
| `done` | Fully completed | `projects/` → move to `archives/` on monthly review |
| `archived` | No longer active | `archives/` |

## 3. Agent Behavior Rules

When interacting with this vault:

1. **Search First**: Search `projects/`, `areas/`, `resources/`, and `daily/` before answering questions about vault contents.
2. **Status Gate**: When mentioning a project, always include its current status from frontmatter.
3. **No Template Edits**: Never modify `templates/_*.md` unless explicitly asked.
4. **Preserve Dashboard**: Never delete or restructure `Dashboard.md` — it is the landing page.
5. **Link Everything**: When creating daily logs or project briefs, link between related files using `[[wikilinks]]`.
6. **Daily Summary Required**: Every daily log must end with a "Daily Summary" section with completed and in-progress checklists.
7. **Weekly Review Trigger**: If asked about "progress this week" or "what's done", suggest creating a weekly review.
8. **Strikethrough Done**: Completed items in lists and tables should use `~~strikethrough~~` to signal completion.
9. **Dashboard Sync**: When project statuses change, update the Dashboard table accordingly.

## 4. Workflow Rules

### Starting a New Project
1. Copy `templates/_project-brief.md` to `projects/project-name.md`
2. Fill in frontmatter (`status: active`, `started: today`)
3. Add to Dashboard active projects table
4. Reference in today's daily log

### Daily Log
1. Generate via Obsidian (`Ctrl+Shift+D`) or manually create `daily/YYYY-MM-DD.md`
2. Fill in: Progress, Blockers, Insights, References, Next Actions
3. Link to relevant project briefs via `[[../projects/xxx.md]]`
4. Complete the Daily Summary section

### Weekly Review
1. Use `templates/_weekly-review.md` at end of week
2. Identify patterns from daily logs
3. Set top 3 priorities for next week
4. Check for projects ready to archive

### Monthly Review
1. Use `templates/_monthly-review.md` at end of month
2. Move `done` projects from `projects/` to `archives/`
3. Review all areas for updates
4. Reflect on quarterly progress

## 5. Linking Conventions

- **Wikilinks**: Use `[[foldername/filename]]` for internal links (e.g., `[[projects/my-project]]`)
- **Daily → Project**: `[[../projects/project-name.md]]` from daily logs
- **Project → Dashboard**: `[[../Dashboard|Dashboard]]` from project briefs
- **Dashboard → Daily**: `[[daily/YYYY-MM-DD]]` from Dashboard
