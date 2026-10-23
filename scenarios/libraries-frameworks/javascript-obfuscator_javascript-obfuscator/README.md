# JavaScript Obfuscator: A Ten-Stage AST Pipeline Mapped for AI Contributors

## Category: Libraries & Frameworks

**Source Repository:** [javascript-obfuscator/javascript-obfuscator](https://github.com/javascript-obfuscator/javascript-obfuscator)
**Original CLAUDE.md:** [View Source](https://github.com/javascript-obfuscator/javascript-obfuscator/blob/master/CLAUDE.md)
**License:** BSD-2-Clause
**Language:** TypeScript

## Overview

JavaScript Obfuscator is a widely used (16k+ stars) TypeScript library and CLI that parses JavaScript with Acorn, runs it through a long chain of AST transformers (renaming, string-array extraction, control-flow flattening, dead-code injection), and regenerates code with escodegen. Its CLAUDE.md, maintained alongside the code and updated repeatedly through 2026, is a large reference document whose real value is in the internals: it spells out the exact order of the node-transformation stages, how InversifyJS wires every component together (including what changed in InversifyJS v7), step-by-step checklists for adding a transformer, an option or a runtime code helper, and the exact `mocha` invocations to run any slice of a big test suite. It is long and partly overlaps with the user-facing README, but the architecture and testing sections give an AI assistant a reliable map of a complex codebase that has been around for a decade.

## Key Features That Make This Exemplary

### 1. **The Pipeline Is Written Down in Execution Order**
Rather than listing transformers alphabetically, the document walks through the obfuscation flow in the order it runs: code-level pre-processing, Acorn parsing, ten sequential node-transformation stages, code generation, code-level post-processing, and source maps. Each stage gets a one-line purpose.

> ```
> 3. Node Transformation Stages (sequential):
>    ├─> Initializing
>    │   └─> Initial AST setup, parentification, metadata
>    ├─> Preparing
>    │   └─> Scope analysis, obfuscating guards, identifier collection
> ```
> — `CLAUDE.md`, Core Workflow → Obfuscation Pipeline

In a transformer-based system, ordering bugs are common (for example, renaming identifiers before or after strings are pulled into the string array). Giving the model the canonical order up front lets it reason about where a new transformation belongs.

### 2. **Framework Migration Notes for the DI Container**
The project relies on InversifyJS, and the CLAUDE.md lists the specific API changes in v7 that would otherwise trip up a model trained mostly on older examples.

> ```
> - `getNamed`, `getTagged`, etc. are replaced by `get(serviceId, { name: ... })` or `get(serviceId, { tag: ... })`
> - `load()` and `unload()` are now async, with `loadSync()` and `unloadSync()` alternatives
> ```
> — `CLAUDE.md`, Dependency Injection Architecture

This targets a real failure mode: assistants confidently writing deprecated library APIs. A short "what changed in version N" list for a core dependency prevents a whole class of compile errors.

### 3. **Extension-Point Checklists**
The "Extension Points" section turns the most common contribution types into numbered recipes that name every file to touch: the abstract base class to extend, the DI module to register in, the main list to add to, and the enum to update.

> ```
> 1. Create transformer class extending `AbstractNodeTransformer`
> 2. Implement `getVisitor()` and `transformNode()` methods
> 3. Register in appropriate module (`src/container/modules/node-transformers/`)
> ```
> — `CLAUDE.md`, Extension Points → Adding Custom Transformers

In DI-heavy codebases, forgetting a registration step causes runtime errors rather than compile errors. Spelling out the full list of steps addresses exactly that.

### 4. **Precise Test Targeting for a Slow Suite**
The document warns that the full suite is slow and explains what each npm test script really does (for example, coverage runs with a 4 GB heap, and the memory-performance test runs with only 280 MB). It then gives the raw `mocha` command with the needed `--require` flags and many path and glob examples, so a single analyzer, transformer family or the CLI can be tested on its own.

> ```
> # Run all control flow tests
> npx mocha --require ts-node/register --require source-map-support/register "test/functional-tests/**/*ControlFlow*.spec.ts"
> ```
> — `CLAUDE.md`, Testing → Pattern Matching

### 5. **Symptom-to-Option Troubleshooting**
A "Common Issues and Solutions" section links symptoms the user reports (code breaks after obfuscation, output too slow or too large, domain lock not working) to specific options such as `reservedNames`, `renamePropertiesMode: 'safe'` and `target: 'browser-no-eval'`. This helps an assistant answer user issues, not just change code.

## Specific Techniques to Learn

### Document Ordered Pipelines as Ordered Lists
If your system has stages (middleware, compiler passes, ETL steps), list them in the order they execute, with one line on each stage's job. Models infer a lot from order, and alphabetical directory listings hide it.

### Pin Breaking Changes in Key Dependencies
```
## <Library> vN notes
- Old API X is replaced by Y
- Method Z is now async; use zSync() for synchronous code
```
A few bullets on a major-version migration of a core dependency is cheap to write and prevents repeated, plausible-looking mistakes.

### Give Single-Test Commands, Not Just `npm test`
When the full suite is slow, document the underlying runner command with the required flags plus glob examples per subsystem. That allows a fast edit-test loop without the assistant having to reverse-engineer the test config.

## Key Takeaways

1. **Order matters in transformer architectures.** Writing down stage order is some of the most useful context you can give for a pipeline-based codebase.
2. **Registration checklists prevent DI mistakes.** When adding a component means editing four or five files, list them all.
3. **Explain what each test script really does.** Heap limits, slowness and scope tell the assistant which command to run when.
4. **A caveat on length.** At roughly 1,500 lines, with npm/yarn variants repeated throughout, this file pays a context-window cost. Its architecture and testing sections are the parts worth copying, while the product-marketing material could live in the README.

## Attribution

This analysis references the original CLAUDE.md from [javascript-obfuscator/javascript-obfuscator](https://github.com/javascript-obfuscator/javascript-obfuscator). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
