# FHIR Validator Wrapper: Kotlin Multiplatform Full-Stack Guide With a Documented State-Management Migration

## Category: Complex Projects

**Source Repository:** [hapifhir/org.hl7.fhir.validator-wrapper](https://github.com/hapifhir/org.hl7.fhir.validator-wrapper)
**Original CLAUDE.md:** [View Source](https://github.com/hapifhir/org.hl7.fhir.validator-wrapper/blob/master/CLAUDE.md)
**License:** Apache-2.0
**Language:** Kotlin

## Overview

The FHIR Validator Wrapper is the CLI, desktop GUI and web server around the HAPI FHIR validation engine, and it powers the public instance at validator.fhir.org. It is a Kotlin Multiplatform project: a Ktor/Koin JVM backend, a Kotlin/JS React frontend using Material-UI, and shared `commonMain` models. Its CLAUDE.md is a good reference for multiplatform codebases. It explains the `expect`/`actual` model pattern with a concrete example, maps the frontend's three React Context providers down to their state fields and callbacks, and documents the 2025 migration from Redux to Context with a before/after table. An assistant trained on older Redux-era Kotlin/JS code would otherwise go back to those patterns.

## Key Features That Make This Exemplary

### 1. **`expect`/`actual` Explained With One Concrete Type**
Rather than describing multiplatform in the abstract, the file shows how one model resolves on each platform:

> - Common: `expect class ValidationContext`
> - JVM: `actual typealias ValidationContext = org.hl7.fhir.validation.ValidationContext`
> - JS: `actual data class ValidationContext(...) { /* serializable fields */ }`
> — `CLAUDE.md`, Multiplatform Data Models

### 2. **A Migration Record That Keeps the Agent Off the Old Patterns**
The "React Context Migration (2025)" section maps each old Redux slice to its new context and gives a pattern table (`dispatch(UpdateState(value))` → `ctx?.updateState?.invoke(value)`, Redux-Thunk → `MainScope().launch`). It also lists related commit hashes. It names the tradeoffs too, such as "Any context update re-renders ALL consumers of that context (unlike Redux memoized selectors)".

### 3. **End-to-End Request Flow Diagram**
One vertical diagram follows a validation from a React component, through a coroutine, the Ktor JS client, Ktor server routes, the Koin-injected controller, `ValidationServiceFactory`, and the HAPI FHIR library, then back to a context `setState`. It covers the whole stack in about 20 lines.

### 4. **Coupled Dependency Versions Called Out**
> The project uses tightly coupled dependencies. **Always update related versions together**. See comments in `gradle.properties`.
> — `CLAUDE.md`, Dependency Version Compatibility

The file then lists the current Kotlin, coroutines, serialization, wrappers, Ktor and Koin versions, and links reference projects that show known-good combinations. This matters because Kotlin/JS wrappers break when versions drift apart.

### 5. **Separate Feature Checklists for Backend and Frontend**
"When Adding New Features" gives a four-step backend recipe (controller interface + impl → `<Feature>Module.kt` routes → register in `Module.kt` → Koin bindings). The frontend recipe starts by asking which context should own the new state, and ends with a worked `deleteFile` example.

## Specific Techniques to Learn

### Document a Migration as a Mapping Table
```markdown
| Aspect          | Before (Redux)          | After (Context)              |
|-----------------|-------------------------|------------------------------|
| Dispatch        | dispatch(Action(v))     | ctx?.update?.invoke(v)       |
| Async           | Thunk middleware        | MainScope().launch { ... }   |
```
After a framework migration, a mapping table is the quickest way to stop an assistant from writing the old pattern.

### Explain Cross-Platform Abstractions With One Real Type
For each platform-split pattern (`expect`/`actual`, conditional exports, platform modules), show one actual type on each target rather than a generic description.

### Make the First Step "Decide Where State Lives"
In the frontend recipe, choosing which context owns the state comes before writing UI code. That keeps new features from scattering state across providers.

## Key Takeaways

1. **Record migrations in CLAUDE.md, not just in commit history.** A slice-to-context map and a pattern table keep an agent from bringing back removed dependencies.
2. **Concrete multiplatform examples beat descriptions.** One type shown on three targets explains `expect`/`actual` faster than a paragraph.
3. **Warn about coupled dependency versions.** Telling the agent which versions must move together prevents breakage that is hard to debug.
4. **State the tradeoffs of your architecture.** Noting that every context consumer re-renders helps an assistant reason about performance.

## Attribution

This analysis references the original CLAUDE.md from [hapifhir/org.hl7.fhir.validator-wrapper](https://github.com/hapifhir/org.hl7.fhir.validator-wrapper). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
