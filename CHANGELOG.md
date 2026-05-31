# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Developer edition (`editions/dev/`) with ADR, snippet, bug-tracker, and dev-log workflows
- 4 new skills: `para-adr`, `para-snippet`, `para-bug-tracker`, `para-dev-log`
- Setup script `editions/dev/setup.py` for one-command dev vault creation
- Public repository standards: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY
- GitHub issue templates, PR template, and CI workflow
- pyproject.toml for Python project metadata
- EditorConfig for consistent editor settings

## [0.1.0] — 2026-05-31

### Added
- Full PARA second brain starter pack with Obsidian integration
- 12 OpenCode skills: `para-vault`, `para-daily-log`, `para-project-brief`, `para-weekly-review`, `para-monthly-review`, `para-dashboard-sync`, `para-link-validator`, `para-frontmatter-check`, `para-search`, `para-mermaid`, `para-md-validator`, `para-table-formatter`
- 9 Python automation scripts for daily logs, project briefs, reviews, search, validation
- Shared utility library (`_shared/`) with 5 modules (vault, frontmatter, wikilinks, dashboard)
- `AGENTS.md` — OpenCode instruction manual for the PARA vault
- `Dashboard.md` — generic landing page / navigation hub
- 4 reusable templates: `_daily-log`, `_project-brief`, `_weekly-review`, `_monthly-review`
- Obsidian configuration (`.obsidian/`) with wikiLinks, daily notes, and template settings
- `opencode.jsonc` — agent config enabling all `para-*` skills

[Unreleased]: https://github.com/aliepratama/opencode-second-brain/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/aliepratama/opencode-second-brain/releases/tag/v0.1.0
