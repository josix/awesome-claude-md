# brix-lang: Full LLVM 18 Compiler Pipeline with Documented Test Baselines

## Category: Libraries & Frameworks

**Source Repository:** [guycanella/brix-lang](https://github.com/guycanella/brix-lang)
**Original CLAUDE.md:** [View Source](https://github.com/guycanella/brix-lang/blob/main/CLAUDE.md)
**License:** Not specified
**Language:** Rust

## Overview

brix-lang is a new imperative, structured, data-oriented ("Array first") programming language implemented in Rust with a full LLVM 18 compiler pipeline. The CLAUDE.md documents the complete compilation chain from source text to native binary, provides an exact test baseline with counts across three test categories, and gives a step-by-step "Adding Features" guide that references real file paths and function names. It is one of the most complete compiler-project CLAUDE.md files available for educational study.

## Key Features That Make This Exemplary

### 1. **Complete Compilation Pipeline Documented**
The entire compilation pipeline is laid out in a single line, making the architecture immediately graspable.

> ```
> ### Compilation Pipeline
> .bx source → Lexer (logos) → Parser (chumsky) → AST → Codegen (inkwell/LLVM 18) → Object + runtime.o → Native Binary
> ```
> — `CLAUDE.md`, Compilation Pipeline section

The pipeline names both the stage (Lexer, Parser) and the Rust crate powering it (logos, chumsky, inkwell). This is actionable: a contributor knows exactly which dependency to examine for each stage.

### 2. **Precise Test Baseline with Three Categories**
Rather than saying "we have tests," the CLAUDE.md states exact numbers across unit, integration, and Test Library categories.

> ```
> **Current test baseline (post Phase 4):** 1,194 unit + 152 integration + 390 Test Library (23 `.test.bx` files)
> ```
> — `CLAUDE.md`, Test Baseline section

Pinning a baseline number has two practical effects: regressions are immediately visible (run `cargo test` and see the count drop), and AI assistants know what "all tests passing" means quantitatively.

### 3. **Step-by-Step Feature Addition Guide with Line Numbers**
The CLAUDE.md provides an ordered checklist for adding new language features, mapping each step to a specific file and function.

> ```
> **New operator:** Token in `lexer/src/token.rs` → precedence in `parser/src/parser.rs`
> → handler in `compile_binary_op()` in `lib.rs`.
> ```
> — `CLAUDE.md`, Adding Features section

Naming the actual function (`compile_binary_op()`) rather than describing the general area means a new contributor can open the file and find the insertion point immediately.

### 4. **Language Specification Embedded in the CLAUDE.md**
The document includes the language's type system, syntax grammar fragments, and the "Array first" philosophy directly. This gives an AI assistant the context needed to reason about new language constructs without fetching separate specification files.

### 5. **Phase-Based Development Tracking**
The project is organized into numbered phases (Phase 1–4 completed; Phase 5+ upcoming). Each phase has a one-line description of what was introduced. This gives temporal context: a contributor understands which features are stable versus experimental.

## Specific Techniques to Learn

### Pipeline-as-a-Line Documentation
```
Component A (library) → Component B (library) → Component C → Output
```
A single-line pipeline with implementation libraries named is more useful than a multi-paragraph prose description. It functions as a navigation map and a dependency declaration simultaneously.

### Quantified Test Baselines
Instead of qualitative statements ("comprehensive tests"), use numbers:
```
Current baseline: X unit + Y integration + Z acceptance
```
This creates a regression signal: if the count drops unexpectedly, something was deleted or broken.

### Function-Level Feature Addition Guides
When documenting how to add a new feature, don't stop at the file—name the function. The reader should be able to `grep -n "compile_binary_op"` and land on the right line.

### Type System Documentation in CLAUDE.md
For language or framework projects, embedding the core type system or grammar fragments (even abbreviated) prevents AI assistants from hallucinating syntax. Short, precise excerpts are better than prose descriptions.

## Key Takeaways

1. **Name the crates or libraries powering each pipeline stage.** `Lexer (logos)` is more useful than just `Lexer` because it tells the reader where to look for bugs and documentation.
2. **Commit to a quantified test baseline.** Exact counts across test categories make regressions visible and set a clear success criterion for "all tests passing."
3. **Give feature addition guides at function granularity, not file granularity.** `compile_binary_op()` in `lib.rs` is actionable; "somewhere in the codegen layer" is not.
4. **Use phase labels to communicate stability.** "Post Phase 4" tells contributors which features are considered stable and which are still evolving.
5. **Embed language spec fragments in the CLAUDE.md.** For a language implementation, core type rules embedded in the document prevent AI hallucination of syntax.

## Attribution

This analysis references the original CLAUDE.md from [guycanella/brix-lang](https://github.com/guycanella/brix-lang). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
