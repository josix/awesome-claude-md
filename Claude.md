# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **awesome-claude-md** - a curated collection of high-quality `claude.md` files from public GitHub repositories. The goal is to showcase best practices for using `claude.md` files to onboard AI assistants to codebases.

## Repository Structure

The repository follows this directory structure:
```
awesome-claude-md/
├── README.md                    # Main landing page
├── claude.md                    # Project planning instructions  
└── scenarios/                   # Categorized examples
    ├── [category]/
    │   └── [owner]_[repo]/
    │       ├── claude.md        # Original file (unmodified)
    │       └── analysis.md      # Analysis of why it's exemplary
```

## Core Categories

When adding examples, use these primary categories:
- **complex-projects**: Multi-service projects with detailed architecture
- **libraries-frameworks**: Core concepts, APIs, and usage patterns
- **developer-tooling**: CLI tools with commands and configuration  
- **project-handoffs**: Current state with blocking issues and next steps
- **getting-started**: Development environment setup focused

## Repository Maintenance Tasks

### Adding New Examples
1. **Search for Quality Files**: Use GitHub search (`filename:claude.md` or `filename:CLAUDE.md`) to find examples
2. **Create Directory Structure**: `scenarios/[category]/[owner]_[repo]/`
3. **Add Original File**: Place unmodified `claude.md` from source
4. **Write Analysis**: Create `analysis.md` with:
   - Category assignment and rationale
   - Specific features that make it exemplary
   - 2-3 key takeaways for developers

### Quality Standards
- Preserve original files without modification
- Focus analysis on concrete, learnable patterns
- Highlight specific techniques (Mermaid diagrams, command lists, etc.)
- Emphasize unique approaches over generic advice

### README Maintenance
After adding examples, update main `README.md` with table of contents linking to each `analysis.md`, organized by category.

## Search Strategies

Use these GitHub search queries to find quality examples:
- `filename:claude.md stars:>100`
- `filename:CLAUDE.md language:TypeScript`
- `"## Architecture" filename:claude.md`
- `"## Development Commands" filename:claude.md`