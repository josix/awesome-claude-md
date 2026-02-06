# Analysis: Dymension Hub - Cosmos SDK Settlement Layer

**Category: Infrastructure Projects**
**Source**: [dymensionxyz/dymension](https://github.com/dymensionxyz/dymension)
**CLAUDE.md**: [View Original](https://github.com/dymensionxyz/dymension/blob/main/CLAUDE.md)
**License**: NOASSERTION
**Stars**: 391

## Why This Example

This is one of the most comprehensive CLAUDE.md files in the blockchain infrastructure space. It documents the Dymension Hub, a Cosmos SDK-based settlement layer, with extraordinary depth covering module architecture, inter-module dependencies, a complete CLI user guide, and critical blockchain-specific constraints like determinism requirements and single-threaded execution. The document serves as both a development guide and an operational reference.

### Key Features That Make This Exemplary

### 1. Critical Blockchain Facts Section
The document opens with essential "FACTS" about Cosmos SDK behavior: single-threaded execution, atomic transaction rollback, and the requirement that BeginBlocker/EndBlocker functions must never panic to avoid chain halts. These constraints are critical for any AI assistant generating code for this project.

### 2. Deep Module Architecture Documentation
The CLAUDE.md maps out the entire module hierarchy under `x/` with clear categorization into Core Modules (rollapp, sequencer, lightclient, delayedack, eibc), Economic Modules (iro, incentives, sponsorship, streamer, lockup), and Utility Modules (denommetadata, dymns, gamm). Each module includes a brief description of its responsibility and key behaviors.

### 3. Inter-Module Dependency Graph
A dedicated section documents key cross-module dependencies (e.g., `rollapp` depends on `sequencer` for validation, `delayedack` depends on `rollapp` for state finalization). This is invaluable for an AI assistant that needs to understand the impact of changes across module boundaries.

### 4. Exhaustive CLI User Guide
The document includes a remarkably complete CLI reference for the `dymd` binary covering key management, querying blockchain state, creating transactions, governance, IBC operations, snapshot management, and debug tools. This transforms the CLAUDE.md into a self-contained operational manual.

### 5. Code Style Guidelines with Anti-Patterns
The code style section explicitly states to "NEVER comment the WHAT" and "ONLY add comments to explain WHY," with concrete good and bad examples. This opinionated guidance prevents AI assistants from generating verbose, redundant comments.

### 6. CI Tool Usage Efficiency Guidance
The document advises running tools "only as needed" to avoid unnecessary work, specifying which tools to run based on which files were modified. This practical optimization guidance is rare and highly useful for AI-assisted development.

## Key Takeaways

1. **State Domain-Specific Constraints Prominently** - Blockchain projects have unique constraints (determinism, no panics in consensus code). Placing these at the top of CLAUDE.md prevents AI assistants from generating code that could cause chain halts or consensus failures.
2. **Map Module Dependencies Explicitly** - In modular architectures, documenting which modules depend on which others helps AI assistants understand the blast radius of changes and write properly integrated code.
3. **Include Operational References** - A comprehensive CLI guide within the CLAUDE.md means AI assistants can help with operational tasks without needing to consult external documentation, making the file a single source of truth.

## Attribution

- **Repository**: [dymensionxyz/dymension](https://github.com/dymensionxyz/dymension)
- **Original CLAUDE.md**: [Direct Link](https://github.com/dymensionxyz/dymension/blob/main/CLAUDE.md)
- **License**: NOASSERTION
- **Organization**: Dymension
