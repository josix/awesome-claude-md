# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **awesome-claude-md** - a curated collection of high-quality `claude.md` files from public GitHub repositories. The goal is to showcase best practices for using `claude.md` files to onboard AI assistants to codebases.

## Repository Structure

The repository follows this directory structure:
```
awesome-claude-md/
├── README.md                    # Main landing page with table of contents
├── CLAUDE.md                    # Project guidance for Claude Code
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot instructions
└── scenarios/                   # Categorized examples
    ├── [category]/
    │   └── [owner]_[repo]/
    │       └── README.md        # Analysis with links to original files
```

## Core Categories

When adding examples, use these primary categories:
- **complex-projects**: Multi-service projects with detailed architecture
- **libraries-frameworks**: Core concepts, APIs, and usage patterns
- **developer-tooling**: CLI tools with commands and configuration
- **project-handoffs**: Current state with blocking issues and next steps
- **getting-started**: Development environment setup focused
- **infrastructure-projects**: Large-scale systems and runtime environments

## Repository Maintenance Tasks

### Automated Discovery System
The repository includes an automated discovery system for finding new CLAUDE.md files:
- **GitHub Action**: `.github/workflows/discover-claude-files.yml` runs weekly
- **Discovery Script**: `scripts/discover_claude_files.py` orchestrates the discovery workflow
- **Modular Architecture**: Discovery system is split into focused modules:
  - `scripts/discovery/loader.py`: Loads existing repositories to avoid duplicates
  - `scripts/discovery/searcher.py`: Searches GitHub for CLAUDE.md files
  - `scripts/discovery/evaluator.py`: Evaluates and scores repository candidates
  - `scripts/discovery/reporter.py`: Creates issues and reports
  - `scripts/discovery/reporters/`: Specialized reporter components for formatting
  - `scripts/discovery/utils.py`: Shared utilities (retry logic, logging)
- **Community Review**: Creates issues with ranked candidates for manual review
- **Documentation**: See `AUTOMATED_DISCOVERY.md` for complete details

### Adding New Examples
1. **Automated Path**: Review discovery issues created by the automation system
2. **Manual Search**: Use GitHub search (`filename:claude.md` or `filename:CLAUDE.md`) to find examples
3. **Create Directory Structure**: `scenarios/[category]/[owner]_[repo]/`
4. **Write Analysis**: Create `analysis.md` with:
   - Category assignment and rationale
   - Source repository link and original CLAUDE.md link
   - License information and proper attribution
   - Specific features that make it exemplary
   - 2-3 key takeaways for developers

### Ethical Guidelines
- **Never copy** `claude.md` files directly into this repository
- **Always link** to the original source repository
- **Include attribution** with source links, licensing information, and proper credit
- **Respect copyright** and only reference publicly available files under permissive licenses

### Quality Standards
- Focus analysis on concrete, learnable patterns
- Highlight specific techniques (Mermaid diagrams, command lists, etc.)
- Emphasize unique approaches over generic advice
- Ensure educational value while respecting original authors

### README Maintenance
After adding examples, update main `README.md` with table of contents linking to each `README.md`, organized by category.

## GitHub Copilot Integration

This repository includes `.github/copilot-instructions.md` for GitHub Copilot users. Both CLAUDE.md and copilot-instructions.md are kept in sync to ensure consistent AI assistant behavior across different tools.

## Search Strategies

Use these GitHub search queries to find quality examples:
- `filename:claude.md stars:>100`
- `filename:CLAUDE.md language:TypeScript`
- `"## Architecture" filename:claude.md`
- `"## Development Commands" filename:claude.md`

## Development Commands

### Code Quality Tools
- `ty check`: Run type checking
- `ruff check .`: Lint entire project
- `ruff format .`: Format code using Ruff
- `complexipy scripts/`: Analyze code complexity
- `ty check && ruff check . && ruff format .`: Combined type checking, linting, and formatting
- `pre-commit run --all-files`: Run all pre-commit hooks on all files
- `pre-commit run`: Run pre-commit hooks on staged files only
- **Remember to fix type errors and linting errors after running ty and ruff**

### Development Workflow
- `uv sync`: Install dependencies
- `pre-commit install`: Install pre-commit hooks (run once after cloning)
- `uv run discover-claude-files`: Run the discovery script
- `pytest`: Run tests
- `pytest --cov`: Run tests with coverage

### File Synchronization
- **Sync CLAUDE.md with copilot-instructions.md**: Keep both AI assistant instruction files synchronized when making changes to project structure, guidelines, or development commands

### Code Analysis
- `complexipy scripts/discover_claude_files.py`: Check complexity of main discovery script
- `complexipy scripts/discovery/`: Analyze complexity of discovery modules
- `complexipy scripts/ --max-complexity 10`: Set custom complexity threshold
- `complexipy scripts/ --output json`: Export complexity analysis as JSON

### Discovery System Architecture
The discovery system follows a modular design with single responsibility principle:
- **Main Script** (`discover_claude_files.py`): 45 lines - lightweight orchestrator
- **Individual Modules**: Each module handles one specific concern (loading, searching, evaluating, reporting)
- **Reduced Complexity**: Complex functions split into smaller, focused components
- **Better Testability**: Each module can be tested independently with 70+ comprehensive tests
- **Maintainability**: Changes to one component don't affect others
- **Clean Test Structure**: Test files mirror module structure in `tests/discovery/`
