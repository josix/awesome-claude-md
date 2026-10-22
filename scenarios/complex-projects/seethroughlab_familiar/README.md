# Familiar: An ADR-Driven CLAUDE.md That Records Execution Order and Hard-Won Traps

## Category: Complex Projects

**Source Repository:** [seethroughlab/familiar](https://github.com/seethroughlab/familiar)
**Original CLAUDE.md:** [View Source](https://github.com/seethroughlab/familiar/blob/main/CLAUDE.md)
**License:** MIT
**Language:** Python

## Overview

Familiar is an LLM-powered local music player: a FastAPI + PostgreSQL (pgvector) + Redis backend that analyzes a local library with librosa/torch, a React/TypeScript web management app, and separate native Apple clients. Its CLAUDE.md is unusual because it is organized around Architecture Decision Records (ADRs). Instead of only describing the code, it tells an assistant when a change needs an ADR, how ADRs must be written, which ADRs govern which areas, and the deliberate order in which they were executed. It also records specific traps found in production ("do not write a range parser", "a bare `uv run pytest` ... would empty DATABASE_URL's database"). The result reads like an architectural memory for the project, aimed at stopping an agent from repeating decisions that were already made or reversed.

## Key Features That Make This Exemplary

### 1. **A Clear Threshold for When an ADR Is Required**
The file separates direction-setting changes from ordinary work, so the assistant knows when to stop and propose a decision rather than just implement:

> An ADR is warranted when a change sets a direction rather than implements one: a new client or
> platform, a data model that other work will build on, moving responsibility between server and
> client, a new external dependency or protocol, or reversing something an existing ADR decided.
> — `CLAUDE.md`, Architecture Decisions (ADRs)

### 2. **ADR Writing Rules That Guard Against Weak Records**
Six numbered rules cover how decision records are written, and each one blocks a specific failure: ADRs must start as `proposed`, "Alternatives Considered" must list real rejected options, and cited metrics and line numbers must be checked against the repo:

> 3. **`## Alternatives Considered` must contain real rejected options with real reasons.** Strawmen
>    make the record worthless.
> 4. **Verify every metric, file path, and line number cited** against the repo at write time.
> — `CLAUDE.md`, Rules

### 3. **Execution-Order Tables With a Reason for Each Step**
Several ADR groups come with a table giving the order they shipped in and why. The file states the ordering principle directly:

> The ordering principle: **server-side work that every client inherits comes before client work**, and
> anything that accumulates data over time starts as early as possible.
> — `CLAUDE.md`, Current set and execution order

### 4. **Named Traps the Compiler Won't Catch**
The file repeatedly calls out mistakes a reasonable engineer would make, along with where the correct code lives. For example, music videos come with "three traps ... all of which the compiler is silent about": do not hand-roll a range parser, do not add `videos` to the generator's tags, and a bare-string `visualizerID` will keep stale values. It also explains why `uv run pytest` refuses to run without `TEST_DATABASE_URL`: it used to delete rows from eighteen tables.

### 5. **Step-by-Step Recipes With the Silent-Failure Steps Called Out**
The "Common Tasks" recipes (new audio feature, LLM tool, API endpoint, migration) mark the step that is easy to miss and say what happens if you miss it:

> **Add a typed column** to `TrackAnalysis` ... Features were promoted out of JSONB
> into typed columns — a new feature that skips this is computed and then silently dropped
> — `CLAUDE.md`, Add a new audio feature

## Specific Techniques to Learn

### Put ADR Governance in CLAUDE.md
```markdown
## Architecture Decisions
Read the relevant ADRs in docs/decisions/ before changing what they govern.
An ADR is required when a change: adds a platform, sets a shared data model,
moves responsibility between tiers, adds a dependency/protocol, or reverses an ADR.
New ADRs start `Status: proposed`. Never edit an accepted Decision — supersede it.
```
This tells an agent when to stop coding and write a proposal, which is the call agents most often get wrong.

### Record "Why This Order", Not Just "What"
A small table of `# | ADR | Why here` keeps an assistant from picking up work that depends on something unfinished, and it records ordering constraints like "start data collection early" that the code cannot show.

### Name the Trap and the Existing Fix
Write the warning as "do not do X; Y already exists and its docstring records the incident". This sends the agent to the existing fix instead of letting it rebuild the bug.

## Key Takeaways

1. **CLAUDE.md can index your decision records.** Pointing to ADRs and stating when a new one is needed keeps an agent consistent with past architectural choices.
2. **Rules about how records are written matter.** "Real alternatives" and "verify every cited number" keep decision records trustworthy months later.
3. **Write down ordering constraints.** Dependency and data-accumulation reasons for sequencing are invisible in code and easy for agents to violate.
4. **Turn incidents into named traps.** One sentence per trap, plus a pointer to the existing safe implementation, prevents regressions.
5. **Tradeoff to note:** the file is long and partly reads as a changelog. Teams adopting this pattern should keep the narrative in the ADRs and keep CLAUDE.md as the index.

## Attribution

This analysis references the original CLAUDE.md from [seethroughlab/familiar](https://github.com/seethroughlab/familiar). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
