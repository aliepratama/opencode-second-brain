# Contributing to opencode-second-brain

Thanks for your interest in contributing! This project is a second brain starter pack — a template for personal knowledge management using the PARA method with Obsidian and OpenCode.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/aliepratama/opencode-second-brain/issues) first
2. Use the [Bug Report](https://github.com/aliepratama/opencode-second-brain/issues/new?template=bug_report.md) template
3. Include: steps to reproduce, expected vs actual behavior, environment details

### Suggesting Features

1. Check [existing issues](https://github.com/aliepratama/opencode-second-brain/issues) and [discussions](https://github.com/aliepratama/opencode-second-brain/discussions)
2. Use the [Feature Request](https://github.com/aliepratama/opencode-second-brain/issues/new?template=feature_request.md) template
3. Describe: the problem, your proposed solution, alternatives considered

### Pull Requests

1. Fork the repository
2. Create a branch: `feat/your-feature` or `fix/your-bugfix`
3. Make your changes
4. Ensure Python scripts run without errors: `python -m scripts <skill-dir>`
5. Follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`)
6. Submit a PR using the template

### Development Setup

```bash
git clone https://github.com/aliepratama/opencode-second-brain.git
cd opencode-second-brain
python -m scripts .opencode/skills/para-daily-log  # example: test a script
```

### Code Conventions

| Language | Convention |
|----------|-----------|
| **Python** | 4-space indent, snake_case, docstrings on modules |
| **Markdown** | 4-space indent in code blocks, language fences (`<!--python-->`) |
| **SKILL.md** | YAML frontmatter with `name`, `description`, `depends_on` |
| **Commits** | [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `docs:`, `chore:` |

### Skill Conventions

When adding a new skill to `.opencode/skills/`:

1. Create `para-skill-name/SKILL.md` with proper frontmatter
2. If it needs automation, add `scripts/__init__.py` + `scripts/__main__.py`
3. Import shared utilities: `from _shared import vault, frontmatter, ...`
4. Add `depends_on` for any skill dependencies
5. Update the root README skills table

### Running Scripts

All automation scripts are run from the vault root:

```bash
python -m scripts .opencode/skills/para-daily-log
python -m scripts .opencode/skills/para-search --status active
```

The shared library in `_shared/` is automatically available to all scripts.

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see [LICENSE](LICENSE)).
