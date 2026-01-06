# PROJECT KNOWLEDGE BASE

**Generated:** 2025-01-07
**Commit:** 206fb84
**Branch:** main

## OVERVIEW

Curated collection of high-quality CLAUDE.md files from GitHub. Python-based discovery system + Jekyll site for browsing 89+ examples across 6 categories.

## STRUCTURE

```
awesome-claude-md/
├── scenarios/              # 89 examples in 6 categories
│   ├── complex-projects/   # Multi-service architectures (22)
│   ├── developer-tooling/  # CLI tools, build systems (36)
│   ├── libraries-frameworks/  # APIs, patterns (24)
│   ├── getting-started/    # Onboarding focused (5)
│   ├── infrastructure-projects/  # Runtime systems (5)
│   └── project-handoffs/   # Transition docs (3)
├── scripts/                # Automated discovery system
│   └── discovery/          # Modular architecture (see AGENTS.md)
├── tests/                  # Mirrors scripts/ structure
├── .github/                # CI/CD workflows
│   └── workflows/          # test, discover, jekyll-gh-pages
└── .claude/                # Agent configs, commands
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add new example | `scenarios/[category]/[owner]_[repo]/README.md` | Link only, never copy |
| Modify discovery | `scripts/discovery/` | Modular, see subdir AGENTS.md |
| Update scoring | `scripts/discovery/evaluator.py` | 100-point content-first system |
| Add category | `scenarios/` + `README.md` TOC | 6 categories defined |
| Fix CI | `.github/workflows/test.yml` | Python 3.11/3.12 matrix |
| Run tests | `pytest tests/` | Mirrors module structure |

## CONVENTIONS

### Naming
- Scenario dirs: `[owner]_[repo]` (underscore separator)
- Analysis files: `README.md` or `analysis.md`

### Quality Standards (Content-First)
- **60+ points required** for inclusion
- Stars = only 10% of score
- Primary: Content Depth (30%), Educational Value (25%), AI Effectiveness (15%)
- Secondary: Project Maturity (20%), Community Recognition (10%)

### Ethical Rules (CRITICAL)
- **NEVER** copy CLAUDE.md files into repo
- **ALWAYS** link to original source
- **ALWAYS** include attribution + license

## ANTI-PATTERNS (THIS PROJECT)

| Forbidden | Reason |
|-----------|--------|
| Copy CLAUDE.md content | Copyright violation |
| Star-based selection | Content quality > popularity |
| Skip attribution | Legal + ethical requirement |
| Edit generated files | Update source, not output |

## COMMANDS

```bash
# Quality checks (run before commit)
ty check && ruff check . && ruff format .

# Testing
pytest                     # All tests
pytest --cov               # With coverage

# Discovery (requires GITHUB_TOKEN)
uv run discover-claude-files

# Pre-commit
pre-commit install         # Once after clone
pre-commit run --all-files # Full check

# Complexity analysis
complexipy scripts/ --max-complexity 10
```

## CI/CD

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `test.yml` | Push/PR to main | Type check, lint, test |
| `discover-claude-files.yml` | Weekly Monday 9AM UTC | Find new examples |
| `jekyll-gh-pages.yml` | Push to main | Deploy static site |

## NOTES

- **No docs/ folder**: Jekyll builds from root (CLAUDE.md mentions docs/ but it doesn't exist)
- **UV package manager**: Use `uv sync` not pip
- **Pre-commit required**: Type checking via `uv run ty check` hook
- **Issue templates**: New example, improvement, bug report in `.github/ISSUE_TEMPLATE/`
