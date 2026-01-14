# Analysis: cctx - Claude Code Context Manager

**Category: Developer Tooling**
**Source**: [nwiizo/cctx](https://github.com/nwiizo/cctx)
**CLAUDE.md**: [View Original](https://github.com/nwiizo/cctx/blob/main/CLAUDE.md)
**License**: Not specified
**Why it's exemplary**: Demonstrates exceptional UX philosophy documentation with clear design principles, deliberate simplicity, and comprehensive guidance specifically tailored for AI assistants.

## Key Features That Make This Exemplary

### 1. **Deliberate UX Philosophy**
- **Predictability Over Cleverness**: Explicitly states "Predictable defaults over clever auto-detection"
- **Progressive Disclosure**: Advanced features revealed only when relevant
- **Design Decisions**: Documents what was deliberately *rejected* and why
- **Simplicity Focus**: "Removed complex auto-detection that was confusing users"

### 2. **File-Based Architecture**
- **Transparent Design**: "Each context is a separate JSON file, making manual management possible"
- **Simple Naming**: "Filename (without .json) = context name"
- **Three Configuration Levels**: User-level, project-level, and local configurations
- **State Tracking**: Hidden `.cctx-state.json` for current/previous context

### 3. **Comprehensive Command Reference**
- **Organized Categories**: Commands grouped by functionality
- **Clear Examples**: Each command with usage patterns
- **Flag Documentation**: Explicit flags for level specification
- **Interactive Features**: fzf integration with built-in fallback

### 4. **AI Assistant Section**
- **Dedicated Guidance**: "Notes for AI Assistants" section
- **Philosophy Statement**: "Predictability beats cleverness"
- **Testing Checklist**: Explicit list for contributors
- **Error Handling**: Consistent anyhow::Result patterns

## Specific Techniques to Learn

### Design Philosophy Documentation
```
**UX Philosophy:**
- Predictable defaults over clever auto-detection
- Progressive disclosure: hints reveal advanced features when relevant
- Default always uses user-level for consistent behavior
- Explicit flags over implicit context switching
```
Captures the *why* behind design decisions, not just the *what*.

### Architecture Documentation
```
**File Structure:**
- ~/.claude/settings/ - Context storage directory
- ~/.claude/settings.json - Active configuration (symlinked)
- .cctx-state.json - Current/previous context tracking
```
Clear mapping from concepts to file locations.

### Error Handling Patterns
```
**Error Philosophy:**
- Consistent anyhow::Result usage throughout
- Contextual error messages with actionable guidance
- Graceful fallbacks (fzf → built-in fuzzy finder)
```
Documents the error handling strategy for consistent implementation.

### Testing Requirements
```
**Testing Checklist:**
- Context creation and deletion
- Context switching (current and previous)
- Edge cases (missing files, invalid JSON)
- Level-specific operations (user, project, local)
```
Explicit checklist ensures comprehensive coverage.

## Key Takeaways

1. **Document Design Philosophy**: State principles like "predictability over cleverness" explicitly
2. **Explain Rejected Approaches**: Document what was *not* done and why
3. **Include AI-Specific Guidance**: Add dedicated sections for AI assistants
4. **Provide Testing Checklists**: Help contributors verify changes comprehensively
5. **Map Concepts to Files**: Show exactly where data lives and how it's structured

## Attribution

This analysis references the original CLAUDE.md from [nwiizo/cctx](https://github.com/nwiizo/cctx). All credit for the original documentation belongs to the repository maintainers.
