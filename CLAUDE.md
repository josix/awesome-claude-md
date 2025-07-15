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
    │       └── analysis.md      # Analysis with links to original files
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

### Adding New Examples
1. **Search for Quality Files**: Use GitHub search (`filename:claude.md` or `filename:CLAUDE.md`) to find examples
2. **Create Directory Structure**: `scenarios/[category]/[owner]_[repo]/`
3. **Write Analysis**: Create `analysis.md` with:
   - Category assignment and rationale
   - Source repository link and original CLAUDE.md link
   - License information (automatically detected via GitHub API)
   - Specific features that make it exemplary
   - 2-3 key takeaways for developers

### License Detection Automation
The repository includes automated license detection using the GitHub API:
- License information is automatically detected and added to analysis files
- Weekly GitHub Actions workflow keeps license information current
- Manual script available for immediate updates: `python detect_licenses.py --update`
- See [LICENSE_DETECTION.md](LICENSE_DETECTION.md) for complete documentation

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
After adding examples, update main `README.md` with table of contents linking to each `analysis.md`, organized by category.

## GitHub Copilot Integration

This repository includes `.github/copilot-instructions.md` for GitHub Copilot users. Both CLAUDE.md and copilot-instructions.md are kept in sync to ensure consistent AI assistant behavior across different tools.

## Search Strategies

Use these GitHub search queries to find quality examples:
- `filename:claude.md stars:>100`
- `filename:CLAUDE.md language:TypeScript`
- `"## Architecture" filename:claude.md`
- `"## Development Commands" filename:claude.md`
