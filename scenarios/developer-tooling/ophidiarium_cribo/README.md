# Analysis: Cribo - Python Source Bundler in Rust

**Category: Developer Tooling**
**Source**: [ophidiarium/cribo](https://github.com/ophidiarium/cribo)
**CLAUDE.md**: [View Original](https://github.com/ophidiarium/cribo/blob/main/CLAUDE.md)
**License**: NOASSERTION
**Stars**: 4

## Why This Example

Despite its small star count, this CLAUDE.md is one of the most technically detailed and AI-engineering-focused documents in the collection. It provides an exhaustive navigation guide through a Rust codebase that bundles Python projects into single files, with precise function-level pointers, critical decision point documentation, debugging commands, and an unusually rigorous set of directives for AI agent behavior. This is a textbook example of optimizing a CLAUDE.md for AI-assisted development.

### Key Features That Make This Exemplary

### 1. Function-Level Navigation Guide
The document provides exact file paths and function names for every critical code path: `BundleOrchestrator::bundle()` as entry point, `PhaseOrchestrator::bundle()` for 9-phase bundling, `classify_modules()` for the wrapper-vs-inline decision, and more. This level of precision eliminates the need for AI assistants to search through the codebase.

### 2. Critical Decision Point Documentation
Three key decision points are documented with their exact logic: the wrapper-vs-inline module classification, circular dependency classification (with five distinct types), and global variable lifting. Each includes the relevant code paths, the conditions that trigger each branch, and the implications. This is invaluable for understanding the bundler's behavior.

### 3. Debugging Command Reference
The document includes targeted debug commands using `RUST_LOG` environment variables with grep filters for specific concerns: module classification decisions, import transformation traces, circular dependency detection, and tree-shaking decisions. This transforms debugging from exploration into targeted investigation.

### 4. Mandatory Git Flow Template
A structured checklist template covers pre-work baseline verification, feature branch creation with test and clippy validation, and PR creation with comprehensive descriptions. The emphasis on `git worktree` over `git checkout` to preserve uncommitted changes shows deep operational awareness.

### 5. Strict AI Agent Behavioral Directives
The document includes remarkably specific directives: enforce `.clippy.toml` disallowed types, never use `#[allow]` annotations as fixes, never hardcode test values in production code, remove dead code immediately rather than deprecating, and always select technically optimal solutions without factoring in human constraints. These transform the CLAUDE.md into an enforceable policy document.

### 6. Deterministic Output Requirements
A dedicated section explains why deterministic, reproducible output is critical (avoiding unnecessary redeployments, simplifying diff inspection) and links this to specific implementation rules: sort imports, use `IndexMap`/`IndexSet` instead of `HashMap`/`HashSet`, and apply consistent formatting regardless of input order.

## Key Takeaways

1. **Provide Function-Level Code Pointers** - For complex codebases, documenting exact file paths and function names for critical paths saves AI assistants enormous search time and reduces the chance of modifying the wrong code.
2. **Document Decision Points, Not Just Architecture** - Explaining the specific conditions that trigger different code paths (wrapper vs inline, circular dependency types) gives AI assistants the context needed to make correct modifications.
3. **Encode Engineering Policies as Directives** - Explicit prohibitions (no `#[allow]` annotations, no hardcoded test values, no deprecation markers) are more effective than general guidelines because they give AI assistants clear boundaries to enforce.

## Attribution

- **Repository**: [ophidiarium/cribo](https://github.com/ophidiarium/cribo)
- **Original CLAUDE.md**: [Direct Link](https://github.com/ophidiarium/cribo/blob/main/CLAUDE.md)
- **License**: NOASSERTION
- **Organization**: Ophidiarium
