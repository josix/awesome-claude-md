# Analysis: pkg-to-jsr

**Category: Developer Tooling**
**Source**: [ryoppippi/pkg-to-jsr](https://github.com/ryoppippi/pkg-to-jsr)
**CLAUDE.md**: [View Original](https://github.com/ryoppippi/pkg-to-jsr/blob/main/CLAUDE.md)
**License**: MIT License
**Why it's exemplary**: Demonstrates AI-optimized code navigation patterns, semantic indexing guidance, and efficient validation architecture for a zero-config CLI tool.

## Key Features That Make This Exemplary

### 1. **AI-Optimized Code Navigation**
- **Indexed Searches**: "Always prefer indexed searches" for efficient code exploration
- **Symbol Navigation**: Semantic code navigation with clear step-by-step acquisition
- **Intelligent Step-by-Step**: Progressive context building for complex operations
- **Tool Recommendations**: Explicit guidance on which tools to use when

### 2. **Validation Architecture**
- **zod-mini Integration**: Tree-shakable validation for minimal bundle size
- **Schema Definitions**: Clear validation patterns for package.json parsing
- **Error Handling**: Structured error types with actionable messages
- **Type Safety**: End-to-end TypeScript type inference

### 3. **Name Resolution Priority**
- **Priority System**: Clear precedence rules for package name resolution
- **Export Handling**: Comprehensive export field mapping logic
- **Edge Cases**: Documentation of special handling for various package structures
- **Fallback Patterns**: Default behaviors when optional fields are missing

### 4. **Constraint-Focused Guidelines**
- **Boolean Expressions**: Specific coding style requirements
- **Unused Imports**: Explicit rules about import management
- **Iteration Reduction**: Patterns to minimize back-and-forth development
- **Linting Rules**: Actionable code quality constraints

## Specific Techniques to Learn

### Semantic Navigation
```markdown
**Code Acquisition Pattern:**
1. Start with entry point (index.ts)
2. Trace imports to dependent modules
3. Use symbol indexing for function lookups
4. Build context progressively, not all at once
```
Efficient code exploration for AI assistants.

### CLI Architecture
```markdown
**Core Components:**
- index.ts - Main library exports
- cli.ts - Command-line interface with cleye
- schemas.ts - zod-mini validation schemas
```
Clean separation between library and CLI concerns.

### Validation Patterns
```markdown
**zod-mini Usage:**
- Tree-shakable for minimal bundle impact
- Type inference with z.infer<typeof schema>
- Custom error messages for user-friendly output
- Composable schemas for complex structures
```
Modern validation with bundle optimization.

### Tool Selection Guidance
```markdown
**Search Priority:**
1. Symbol index search (fastest)
2. Semantic grep (pattern matching)
3. Full-text search (last resort)
4. File browsing (avoid when possible)
```
Explicit guidance on tool selection for efficiency.

## Key Takeaways

1. **AI Navigation**: Provide explicit guidance on code exploration strategies
2. **Tool Preferences**: Document which tools to use in which situations
3. **Minimal Dependencies**: Choose tree-shakable libraries for bundle optimization
4. **Progressive Context**: Build understanding incrementally, not all at once
5. **Constraint Documentation**: Explicit coding style rules reduce iteration cycles

## Attribution

This analysis references the original CLAUDE.md from [ryoppippi/pkg-to-jsr](https://github.com/ryoppippi/pkg-to-jsr). All credit for the original documentation belongs to the repository maintainers.
