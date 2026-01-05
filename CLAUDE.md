# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **awesome-claude-md** - a curated collection of high-quality `CLAUDE.md` files from public GitHub repositories. The goal is to showcase best practices for using `CLAUDE.md` files to onboard AI assistants to codebases.

## Repository Structure

The repository follows this directory structure:
```
awesome-claude-md/
├── README.md                    # Main landing page with table of contents
├── CLAUDE.md                    # Project guidance for Claude Code
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot instructions
├── docs/                        # GitHub Pages static site
│   ├── _config.yml              # Jekyll configuration
│   ├── _layouts/                # HTML layouts
│   ├── assets/                  # CSS and JavaScript
│   │   ├── css/style.css        # Dark-themed responsive styles
│   │   └── js/main.js           # Search and filter functionality
│   └── index.html               # Main browsable page
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
2. **Manual Search**: Use GitHub search (`filename:CLAUDE.md`) to find examples
3. **Create Directory Structure**: `scenarios/[category]/[owner]_[repo]/`
4. **Write Analysis**: Create `analysis.md` with:
   - Category assignment and rationale
   - Source repository link and original CLAUDE.md link
   - License information and proper attribution
   - Specific features that make it exemplary
   - 2-3 key takeaways for developers

### Ethical Guidelines
- **Never copy** `CLAUDE.md` files directly into this repository
- **Always link** to the original source repository
- **Include attribution** with source links, licensing information, and proper credit
- **Respect copyright** and only reference publicly available files under permissive licenses

### Quality Standards

Our selection prioritizes **content quality and educational value over popularity metrics**:

#### Primary Criteria (70% weight)
1. **Content Depth** - Comprehensive architecture, workflows, and context
2. **Educational Value** - Demonstrates unique patterns and best practices
3. **AI Effectiveness** - Well-structured for AI assistant consumption

#### Secondary Criteria (30% weight)
4. **Project Maturity** - Active maintenance and production usage
5. **Community Recognition** - Industry validation and engagement

#### Scoring Framework
- **100-point scale** emphasizing content quality
- **60+ points required** for inclusion
- **Stars contribute only 10%** of total score
- **No hard star minimums** - quality content from any repository size

#### Selection Process
1. **Automated Discovery** finds candidates using enhanced content analysis
2. **Community Review** evaluates educational value and uniqueness
3. **Manual Curation** ensures alignment with quality standards

### README Maintenance
After adding examples, update main `README.md` with table of contents linking to each `README.md`, organized by category.

## GitHub Pages Static Site

The repository includes a browsable static site at `https://josix.github.io/awesome-claude-md/` for easy example navigation.

### Site Structure
- **Location**: `docs/` folder (served via GitHub Pages)
- **Technology**: Jekyll with custom dark theme
- **Features**: Search, category filters, language filters, responsive design

### Key Files
- `docs/_config.yml`: Jekyll configuration (baseurl, title, theme settings)
- `docs/_layouts/default.html`: Base HTML layout with header, footer, navigation
- `docs/assets/css/style.css`: Dark-themed responsive CSS with CSS variables
- `docs/assets/js/main.js`: Client-side search and filter functionality
- `docs/index.html`: Main page with all examples as filterable cards

### Adding New Examples to the Site
When adding new examples to `scenarios/`, also update `docs/index.html`:
1. Add a new `<div class="example-card">` in the appropriate category section
2. Include required data attributes: `data-category`, `data-language`, `data-title`, `data-repo`, `data-description`
3. Follow the existing card structure with icon, title, description, tags, and links

### Site Features
- **Search**: Real-time filtering by title, repo name, or description (Ctrl+K shortcut)
- **Category Filters**: Filter by 6 categories (complex-projects, developer-tooling, etc.)
- **Language Filters**: Filter by programming language (TypeScript, Python, Rust, Go, Swift, Java)
- **Responsive Design**: Mobile-friendly layout with dark theme
- **Direct Links**: Each card links to both the analysis page and original repository

### Local Development
To preview the site locally:
```bash
cd docs
bundle install  # First time only
bundle exec jekyll serve
# Visit http://localhost:4000/awesome-claude-md/
```

## GitHub Copilot Integration

This repository includes `.github/copilot-instructions.md` for GitHub Copilot users. Both CLAUDE.md and copilot-instructions.md are kept in sync to ensure consistent AI assistant behavior across different tools.

## Search Strategies

### Manual Search Queries
Use these GitHub search queries to find quality examples:
- `filename:CLAUDE.md "## Architecture"`
- `filename:CLAUDE.md "## Development Commands"`
- `"## Testing" filename:CLAUDE.md`
- `"## Deployment" filename:CLAUDE.md`
- `filename:CLAUDE.md language:TypeScript`

### KOL and Expert Organization Search
Target repositories from key opinion leaders and expert organizations:
- `filename:CLAUDE.md user:anthropics` - AI experts and Claude creators
- `filename:CLAUDE.md user:pydantic` - Python validation library experts
- `filename:CLAUDE.md user:microsoft` - Enterprise AI and infrastructure
- `filename:CLAUDE.md user:gaearon` - React co-creator Dan Abramov
- `filename:CLAUDE.md user:openai` - AI research and development
- `filename:CLAUDE.md user:cloudflare` - Infrastructure and runtime systems
- `filename:CLAUDE.md user:pytorch` - Machine learning frameworks

### Domain-Specific Searches
- **Python Ecosystem**: `filename:CLAUDE.md user:fastapi OR user:tiangolo OR user:pydantic`
- **JavaScript/React**: `filename:CLAUDE.md user:vercel OR user:facebook OR user:nextjs`
- **AI/ML**: `filename:CLAUDE.md user:huggingface OR user:langchain-ai`
- **Infrastructure**: `filename:CLAUDE.md user:docker OR user:kubernetes`

### Current Top Examples from Expert Search
Based on embedding-based similarity search for high-quality patterns:

#### Exceptional Quality (Industry Leaders)
- **pydantic/genai-prices**: Expert Python data processing pipeline patterns
- **gaearon/overreacted.io**: React co-creator's advanced Next.js blog architecture
- **anthropics/anthropic-quickstarts**: Official AI development best practices
- **microsoft/semanticworkbench**: Enterprise AI assistant platform

#### High Quality (Established Organizations)  
- **openai/openai-agents-python**: Multi-agent workflow framework
- **microsoft/recipe-tool**: Automation recipe patterns
- **blueprintui/blueprintui**: UI component library architecture

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
