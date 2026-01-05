# Foam - Personal Knowledge Management for VSCode

## Category: Developer Tooling

**Why this category?** Foam is a VSCode extension ecosystem for personal knowledge management, providing developers with tools for note-taking, knowledge graph visualization, and Zettelkasten-style workflows within their development environment.

## Source Repository

- **Repository**: [foambubble/foam](https://github.com/foambubble/foam)
- **Original CLAUDE.md**: [View on GitHub](https://github.com/foambubble/foam/blob/master/CLAUDE.md)
- **Stars**: 16,500+
- **Language**: TypeScript
- **License**: MIT
- **Last Updated**: Active (daily commits)

## Quality Score: 85/100 (Exceptional)

### Scoring Breakdown
- **Content Depth** (35/40): Comprehensive architecture documentation with platform-agnostic core isolation
- **Educational Value** (30/30): Demonstrates unique patterns like reversed trie indexing and event-driven architecture
- **AI Effectiveness** (20/20): Explicit workflow scaffolding with deterministic execution paths
- **Project Maturity** (8/10): Mature ecosystem with active community

## Why This Example Is Exceptional

### 1. Architecture-First Documentation
The CLAUDE.md establishes clear separation of concerns with platform-agnostic core logic isolated in `src/core/`. This pattern ensures the core business logic remains testable and portable across different environments.

### 2. Structured Development Workflow
Implements a "Research -> Plan -> Implement -> Validate" methodology requiring planning artifacts before implementation:
- Mandates planning documentation in `/.agent/current-plan.md`
- Requires test-first development with explicit failure before success
- Prevents architectural rework through upfront design

### 3. Sophisticated Testing Architecture
The testing guidance distinguishes three test categories:
- Unit tests (`*.test.ts`)
- Integration tests (`*.spec.ts`)
- VS Code-dependent tests using mock modules

Key principle: "Never mock anything that is inside `packages/foam-vscode/src/core/`" ensures core logic remains directly testable.

### 4. Unique Technical Patterns
- **Reversed trie indexing** in FoamWorkspace for efficient resource lookup
- **Event-driven architecture** with `onDidAdd`, `onDidUpdate`, `onDidDelete` patterns
- **Feature registration pattern** injecting ExtensionContext and deferred Foam promises
- **Platform-agnostic DataStore interface** abstracting filesystem operations
- **Placeholder resource handling** for broken links within FoamGraph

### 5. AI Collaboration Guidelines
Explicitly permits critical evaluation with directives like "Be honest and objective" and "challenge assumptions" rather than compliance-first responses.

## Key Takeaways

1. **Platform-Agnostic Core**: Isolate core business logic from platform-specific code to maximize testability and portability
2. **Planning-First Development**: Require explicit planning artifacts before implementation to prevent architectural drift
3. **Test Category Distinction**: Clearly differentiate unit, integration, and platform-dependent tests with specific patterns for each
4. **Constraint-Based Guidance**: Document prohibitions explicitly (e.g., "never mock core") rather than relying on assumptions

## Notable Sections

- Project Overview with architectural principles
- Development workflow with planning requirements
- Testing guidance with category-specific patterns
- Feature registration and extension patterns
- Event-driven state management

## Attribution

This analysis references the original CLAUDE.md from [foambubble/foam](https://github.com/foambubble/foam), created and maintained by Jani Evakallio and the Foam community. All credit for the original documentation belongs to the repository maintainers.
