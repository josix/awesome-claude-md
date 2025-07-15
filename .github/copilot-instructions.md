# GitHub Copilot Instructions

This file provides guidance to GitHub Copilot when working with code in this repository.

## Project Overview

**awesome-claude-md** is a curated collection of high-quality `claude.md` files from public GitHub repositories. The goal is to showcase best practices for using `claude.md` files to onboard AI assistants to codebases.

## Repository Structure

When suggesting file paths or navigation, follow this structure:
```
awesome-claude-md/
├── README.md                    # Main landing page with table of contents
├── CLAUDE.md                    # Project guidance for Claude Code
├── .github/
│   └── copilot-instructions.md  # This file
└── scenarios/                   # Categorized examples
    ├── [category]/
    │   └── [owner]_[repo]/
    │       ├── claude.md        # Original file (unmodified)
    │       └── analysis.md      # Analysis of why it's exemplary
```

## Core Categories

When adding new examples, use these primary categories:
- `complex-projects/` - Multi-service projects with detailed architecture
- `libraries-frameworks/` - Core concepts, APIs, and usage patterns  
- `developer-tooling/` - CLI tools with commands and configuration
- `project-handoffs/` - Current state with blocking issues and next steps
- `getting-started/` - Development environment setup focused
- `infrastructure-projects/` - Large-scale systems and runtime environments

## File Naming Conventions

### Directory Names
- Use lowercase with hyphens: `complex-projects`, `developer-tooling`
- Repository directories: `[owner]_[repo]` format (e.g., `microsoft_semanticworkbench`)

### File Names
- Original files: `claude.md` (preserve exactly as found)
- Analysis files: `analysis.md` (our evaluation)
- Some projects use: `README.md` for analysis (legacy pattern)

## Common Development Patterns

### Documentation Structure
When creating analysis.md files, follow this pattern:
```markdown
# Analysis: [Project Name]

**Category**: [Category Name]
**Repository**: [GitHub URL]
**Why it's exemplary**: [Brief explanation]

## Key Features That Make This Exemplary

### 1. **[Feature Name]**
- **[Aspect]**: [Description]
- **[Commands/Examples]**: [Specific examples]

## Specific Techniques to Learn

### [Technique Name]
```[language]
[Code example]
```
[Explanation]

## Key Takeaways

1. **[Takeaway 1]**: [Description]
2. **[Takeaway 2]**: [Description]
```

### README.md Updates
When adding new examples, update the main README.md:
- Add entry in appropriate category section
- Include project name, repository link, and star count
- List 2-3 key features in bullet points
- Link to the analysis.md file

### Search Commands
For finding new examples, suggest these GitHub search patterns:
```
filename:claude.md stars:>100
filename:CLAUDE.md language:TypeScript
"## Architecture" filename:claude.md
"## Development Commands" filename:claude.md
```

## Quality Standards

### Original Files
- Preserve `claude.md` files exactly as they appear in source repositories
- Never modify original content
- If file has different name (e.g., `CLAUDE.md`), rename to `claude.md` for consistency

### Analysis Files
- Focus on concrete, learnable patterns
- Highlight specific techniques (Mermaid diagrams, command lists, etc.)
- Emphasize unique approaches over generic advice
- Include 3-5 key takeaways with specific examples

### Repository Selection Criteria
- **Industry Recognition**: From organizations with proven track records
- **Production Usage**: Actively maintained and used in production
- **Comprehensive Documentation**: Detailed architecture, setup, and workflow information
- **Best Practices**: Demonstrate advanced patterns and techniques
- **AI-Friendly**: Structured to maximize AI assistant effectiveness

## Development Workflow Patterns

### Command Organization
Suggest commands grouped by purpose:
```markdown
### Building
- `[build command]` - Build description
- `[release build]` - Release build description

### Testing  
- `[test command]` - Test description
- `[integration tests]` - Integration test description

### Development
- `[dev command]` - Development description
- `[watch command]` - Watch mode description
```

### Architecture Documentation
Structure architecture sections like:
```markdown
## Architecture Overview

**Core Components:**
- `[directory/]` - Component description
- `[package]` - Package purpose

**Key Workflows:**
- [Workflow 1] - Description
- [Workflow 2] - Description
```

## Code Completion Context

When working with this repository:

### For Python code
- No specific Python code in this repository (documentation only)

### For Markdown files
- Use consistent heading levels (## for main sections, ### for subsections)
- Include code blocks with language specification
- Use bold for emphasis on key terms
- Include links to repositories and documentation

### For GitHub search
- Use specific filename searches: `filename:claude.md`
- Combine with filters: `stars:>100`, `language:TypeScript`
- Include quoted strings for specific content: `"## Architecture"`

### For file operations
- Always use absolute paths within the repository
- Preserve original file content when copying
- Follow directory naming conventions strictly
- Update README.md table of contents after adding examples

## Organizations to Prioritize

When suggesting new examples, prioritize these organizations:
- **Cloudflare**: Infrastructure runtime and developer tooling
- **Microsoft**: AI systems and enterprise tooling  
- **PyTorch**: Machine learning infrastructure
- **LangChain**: AI application frameworks
- **Sentry**: Error tracking and monitoring
- **Ethereum Foundation**: Blockchain infrastructure
- **Vercel**: Frontend deployment platform
- **Supabase**: Backend-as-a-Service platform