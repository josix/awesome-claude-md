# Analysis: Pixel Banner

**Category: Developer Tooling**
**Source**: [jparkerweb/pixel-banner](https://github.com/jparkerweb/pixel-banner)
**CLAUDE.md**: [View Original](https://github.com/jparkerweb/pixel-banner/blob/main/CLAUDE.md)
**License**: MIT License
**Why it's exemplary**: Demonstrates task-oriented plugin documentation with clear architectural flow, multi-layered testing guidance, and explicit integration patterns for Obsidian plugin development.

## Key Features That Make This Exemplary

### 1. **Task-Based Documentation Organization**
- **Goal-Oriented Sections**: "Adding a New Image Provider" instead of file-centric navigation
- **Workflow Priority**: Labels `npm run test-build` as "PRIMARY DEVELOPMENT COMMAND"
- **User-Focused Structure**: Organized by what developers want to accomplish
- **Quick Navigation**: Helps developers find solutions without deep codebase knowledge

### 2. **Complete Architectural Flow Mapping**
- **Entry Point Tracing**: Tracks from plugin initialization through DOM insertion
- **Decision Trees**: Shows how keywords trigger API vs vault paths use Obsidian API
- **Component Relationships**: Maps apiService.js, bannerManager.js, bannerUtils.js interactions
- **Data Flow Clarity**: Explains transformation from input to rendered banner

### 3. **Multi-Layered Testing Strategy**
- **Test Location Documentation**: Explicit paths for `tests/unit` and `tests/integration`
- **Pattern Matching Examples**: `npx vitest -t "getInputType"` for targeted testing
- **Key Test Files**: Identifies `bannerWorkflow.test.js` for integration scenarios
- **Framework Integration**: Vitest setup with Obsidian-specific mocking

### 4. **Frontmatter Processing Clarity**
- **Dual-Format Explanation**: Distinguishes input formats from output formats
- **Bidirectional Awareness**: Prevents confusion about read vs write operations
- **Format Compatibility**: Documents supported input variations
- **Setting Configuration**: Explains Image Property Format Setting behavior

## Specific Techniques to Learn

### Path Resolution Logic
```
1. Check for URL pattern (http/https)
2. Look for vault path (starts with /)
3. Check Obsidian attachment folder
4. Try relative to current file
5. Search entire vault
6. Check external providers (Unsplash, etc.)
7. Apply default if all fail
```
Numbered step-by-step mental model for complex logic.

### Development Command Hierarchy
```
PRIMARY: npm run test-build
  ├── npm run build        # Compile TypeScript
  ├── npm test            # Run all tests
  └── npm run dev         # Watch mode for development
```
Clear prioritization of essential vs. supporting commands.

### Plugin Architecture Flow
```
main.ts (entry) → bannerManager.js (orchestration)
  ├→ apiService.js (external APIs)
  ├→ bannerUtils.js (rendering logic)
  └→ Obsidian Vault API (file operations)
```
Visual component relationship mapping.

### IDE Integration Notes
```
Remember to update `inventory.md` per `.cursor/rules`
```
Documents tool-aware development conventions.

## Key Takeaways

1. **Task-Oriented Structure**: Organize by developer goals, not just file structure
2. **Priority Signaling**: Explicitly label primary commands to reduce cognitive load
3. **Flow Documentation**: Trace data transformation from input to output
4. **Dual-Format Awareness**: Document both input processing and output generation
5. **Testing Tiers**: Distinguish unit vs integration with specific examples

## Unique Patterns

- **Primary Command Designation**: Explicit "PRIMARY DEVELOPMENT COMMAND" label
- **7-Step Path Resolution**: Numbered logic flow for complex decision trees
- **Frontmatter Bidirectionality**: Clear separation of read vs write formats
- **Cursor IDE Integration**: Documents AI-specific development workflow conventions

## Educational Value

This example is particularly valuable for:
- Teams building Obsidian plugins with external API integrations
- Projects requiring complex path resolution logic
- Developers creating plugins with frontmatter processing
- Understanding task-based documentation organization for plugin ecosystems

## Common Development Tasks

### Adding a New Image Provider
File locations and code patterns clearly documented for:
- Creating new API service modules
- Registering providers in apiService.js
- Adding configuration options
- Testing provider integrations

### Debugging Banner Issues
Specific files to check based on issue type:
- Input not recognized → bannerUtils.js (getInputType function)
- API failures → apiService.js (provider-specific handlers)
- Rendering issues → bannerManager.js (DOM manipulation)
- Frontmatter problems → bannerUtils.js (format parsing)
