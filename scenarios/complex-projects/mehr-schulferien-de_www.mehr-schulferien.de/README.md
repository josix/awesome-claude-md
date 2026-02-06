# Analysis: mehr-schulferien.de - German School Vacation Web Application

**Category: Complex Projects**
**Source**: [mehr-schulferien-de/www.mehr-schulferien.de](https://github.com/mehr-schulferien-de/www.mehr-schulferien.de)
**CLAUDE.md**: [View Original](https://github.com/mehr-schulferien-de/www.mehr-schulferien.de/blob/master/CLAUDE.md)
**License**: Not specified
**Stars**: 29

## Why This Example

This CLAUDE.md is an outstanding example of documenting a production Phoenix/Elixir web application with exceptional attention to test quality standards, code quality enforcement through hooks, and migration status tracking. It demonstrates how to maintain a living document that evolves with the project, including detailed maintenance mode documentation for temporarily disabled features.

### Key Features That Make This Exemplary

### 1. Automated Code Quality Enforcement via Hooks
The document explains that Claude Code hooks automatically run `mix format`, `mix test`, and `mix compile --warnings-as-errors` after each response. This creates a feedback loop where the AI assistant's responsibilities are explicitly defined: fix test failures when UI changes break assertions, fix all warnings immediately, and verify clean test output.

### 2. Rigorous Test Quality Standards
An entire section is dedicated to defining what "clean" tests look like: no debug output (`IO.puts`, `IO.inspect`, `dbg()`), no skipped tests, no placeholder tests (`assert true`), no warnings in output, and no flaky tests. A concrete test quality checklist with exact shell commands is provided for verification before every commit.

### 3. Feature Maintenance Mode Documentation
The wiki functionality is documented as "temporarily disabled" with a precise step-by-step re-enablement guide: uncomment routes in router.ex, remove `@moduletag :skip` from 13 specific test files (all listed by path), and run verification tests. This pattern of documenting disabled features is valuable for long-lived projects.

### 4. Phoenix Migration Status Tracking
The document tracks the completed Phoenix 1.7 to 1.8 migration with specific details: View modules migrated to format-specific modules (HTML, JSON, ICS, XML), controller configuration updated, and test dependencies added. It also documents the completed migration to Phoenix verified routes with the `~p` sigil pattern.

### 5. Styling Guidelines with Design System Reference
The document specifies Tailwind CSS as the mandatory styling framework with references to shared components (`<.heading>`, `<.card>`, `<.button>`), design tokens, and specific patterns for list formatting and wiki form elements including exact CSS class strings for form inputs.

### 6. Proactive Test Maintenance Protocol
A dedicated protocol defines how to approach test issues systematically: always check test output quality first, identify all issues (not just the obvious one), fix root causes rather than symptoms, and verify fixes with multiple runs. "Red flags" requiring immediate action are listed explicitly.

## Key Takeaways

1. **Enforce Quality Through Hooks, Not Just Instructions** - Documenting automated quality gates (hooks that run tests and linting after each AI response) creates a more reliable feedback loop than relying on the AI assistant to remember to run checks.
2. **Define Test Quality as a Measurable Standard** - Specifying exact criteria for clean tests (no debug output, no skipped tests, no warnings) with verification commands transforms test quality from a subjective judgment into an auditable checklist.
3. **Document Feature States with Re-enablement Steps** - For temporarily disabled features, providing exact file paths and steps to re-enable prevents knowledge loss and makes it trivial for an AI assistant to restore functionality when needed.

## Attribution

- **Repository**: [mehr-schulferien-de/www.mehr-schulferien.de](https://github.com/mehr-schulferien-de/www.mehr-schulferien.de)
- **Original CLAUDE.md**: [Direct Link](https://github.com/mehr-schulferien-de/www.mehr-schulferien.de/blob/master/CLAUDE.md)
- **License**: Not specified
- **Creator**: mehr-schulferien.de community
