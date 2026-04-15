# action-idle: Cross-Platform Game with ESLint-Enforced Portability Constraint

## Category: Complex Projects

**Source Repository:** [ebergstedt/action-idle](https://github.com/ebergstedt/action-idle)
**Original CLAUDE.md:** [View Source](https://github.com/ebergstedt/action-idle/blob/main/CLAUDE.md)
**License:** Not specified
**Language:** TypeScript

## Overview

action-idle is a "Total Idle" TypeScript game featuring a Battle System (active) and an Economy System (dormant). What makes this CLAUDE.md exceptional is not its star count (0) but the architectural rigor it documents: a hard portability constraint enforced at the tooling level, a translation table between TypeScript and GDScript patterns, and 11 named design principles with inline code examples. This is one of the most thoroughly documented CLAUDE.md files in any small game project.

## Key Features That Make This Exemplary

### 1. **ESLint-Enforced Architectural Boundary**
The single most noteworthy pattern: `/src/core/` must remain pure TypeScript with zero React or browser dependencies, and this constraint is enforced by ESLint—not just documented as a guideline.

> ```
> ## Primary Constraint
> All non-presentation code must be easily portable to Godot. Everything in `/src/core/` uses
> interfaces and pure TypeScript with zero React/browser dependencies.
> **ESLint enforces this**: The `eslint.config.js` has a rule blocking React imports in `/src/core/`.
> ```
> — `CLAUDE.md`, Primary Constraint section

This elevates documentation from aspiration to enforcement: violating the boundary causes a lint failure, not a code review comment.

### 2. **TypeScript↔GDScript Translation Table**
The CLAUDE.md includes a mapping table that directly translates TypeScript idioms to their GDScript equivalents, giving future contributors (or AI assistants) a concrete reference for the "why" behind code patterns.

> ```
> | TypeScript       | GDScript Equivalent                 |
> |------------------|-------------------------------------|
> | `tick(delta: number)` | `_process(delta: float)`       |
> | `interface State { ... }` | `class_name State extends Resource` |
> ```
> — `CLAUDE.md`, TypeScript↔GDScript section

This is rare: most game projects document one language; this one documents the intentional correspondence between two.

### 3. **11 Named Design Principles with Code Examples**
Each principle is named, explained, and illustrated with a ✅/❌ code comparison. For example:

> ```
> ### 2. Pure Functions Over Stateful Classes
> Prefer pure functions that take state and return new state. This maps directly to Godot's functional patterns:
> // ✅ Good - pure function, easy to port
> function selectUnit(state: SelectionState, unitId: string): SelectionState {
>   return { selectedIds: [unitId] };
> }
> ```
> — `CLAUDE.md`, Design Principles section

Having 11 documented principles is unusual. Most CLAUDE.md files name 3–4 at most.

### 4. **Entity-to-Godot-Signal Architecture Mapping**
The document maps game entity types (units, buildings, economy objects) to their expected Godot signal equivalents. This means any developer extending the game knows exactly how TypeScript types will eventually translate to engine signals—and can write code accordingly from the start.

### 5. **Dormant vs. Active System Documentation**
The CLAUDE.md explicitly distinguishes the Battle System (active, under development) from the Economy System (dormant, not yet implemented). This state awareness prevents wasted effort and tells AI assistants where to focus.

## Specific Techniques to Learn

### Enforced Architectural Constraints via Linting
```
// eslint.config.js patterns that block cross-layer imports
// Core rule: no React/browser imports inside /src/core/
```
Using ESLint to enforce architecture means the constraint survives team changes and AI session resets. Document the tooling configuration that enforces your boundaries, not just the boundaries themselves.

### Translation Table for Cross-Platform Projects
When a project targets multiple runtimes or languages, provide an explicit translation table rather than leaving the mapping implicit. Format it as a two-column markdown table: source idiom → target idiom.

### Named Principles at Scale
Naming principles (rather than listing bullet points) creates anchors for discussion: "This violates Principle 3" is more actionable than "this doesn't follow our style." 11 named principles is high; 3–5 is a good starting point for most projects.

### ✅/❌ Code Comparisons
Showing what to do AND what not to do side-by-side is more informative than showing only the correct pattern. The "bad" example makes the constraint concrete.

## Key Takeaways

1. **Enforce architectural constraints via linting, not just documentation.** An ESLint rule that blocks cross-layer imports is more durable than a paragraph telling developers to be careful.
2. **Document cross-runtime correspondences explicitly.** If your code will be ported or translated, a translation table between idioms is far more useful than a prose description of the target platform.
3. **Name your design principles.** Named principles create shared vocabulary and make code review comments more precise than anonymous bullet lists.
4. **Mark system state in the document.** Explicitly labeling subsystems as "active" or "dormant" prevents AI assistants and new contributors from working on the wrong area.
5. **Use ✅/❌ comparisons.** Pairing a correct example with its incorrect counterpart makes constraints unambiguous.

## Attribution

This analysis references the original CLAUDE.md from [ebergstedt/action-idle](https://github.com/ebergstedt/action-idle). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
