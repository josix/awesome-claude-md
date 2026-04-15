# mivoa: Firebase Abstraction Pattern with Enforced StorageBackend Interface

## Category: Libraries & Frameworks

**Source Repository:** [mariepop13/mivoa](https://github.com/mariepop13/mivoa)
**Original CLAUDE.md:** [View Source](https://github.com/mariepop13/mivoa/blob/develop/CLAUDE.md)
**License:** Not specified
**Language:** TypeScript
**Branch:** develop

## Overview

mivoa is a Next.js 15 + TypeScript + Tailwind application with Shadcn UI / Radix UI and comprehensive Vitest testing. Its CLAUDE.md is notable for one specific pattern: the `StorageBackend` abstraction that completely decouples Firebase from UI components and hooks, enforced by an explicit rule ("Nothing in `components/` or `hooks/` may import from `firebase/*`"). This is a teachable example of dependency inversion applied to a Firebase application—a pattern that is widely applicable but rarely documented this clearly.

## Key Features That Make This Exemplary

### 1. **`StorageBackend` Interface as Architectural Cornerstone**
The CLAUDE.md defines a named interface (`StorageBackend`) that abstracts all Firebase access, and names the two concrete implementations.

> ```
> ### StorageBackend Abstraction
> - `storage-backend.ts`: Interface (subscribeToAuthState, subscribeToEntriesByDate, ...)
> - `firebase-storage-backend.ts`: Firebase implementation (default)
> - `local-storage-backend.ts`: In-memory implementation (no Firebase required)
> ```
> — `CLAUDE.md`, StorageBackend Abstraction section

The in-memory implementation (`local-storage-backend.ts`) is particularly significant: it means tests and local development can run without any Firebase configuration or network access. The abstraction is not purely theoretical—it has a second implementation that proves it works.

### 2. **Enforced Firebase Import Rule**
The abstraction is backed by an explicit prohibition, not just a recommendation.

> ```
> ### Firebase Abstraction Rule
> **Nothing in `src/components/` or `src/hooks/` may import from `firebase/*`.**
> Firebase types and instances belong only in:
> - `src/firebase/` — Firebase setup and auth
> - `src/repositories/firebase-storage-backend.ts` — Firebase data access
> ```
> — `CLAUDE.md`, Firebase Abstraction Rule section

This is a rules-based constraint, not a style preference. The explicit file paths for where Firebase types *are* allowed make the rule precise rather than vague.

### 3. **BYOK AI Model Integration**
The application supports Bring Your Own Key (BYOK) AI model integration. The CLAUDE.md documents this as an architectural feature rather than a deployment detail, reflecting that user-controlled AI configuration is a first-class design decision.

### 4. **Three Entry Kinds with Explicit Typing**
The data model distinguishes three entry kinds, each explicitly typed. This type-safe data model is documented in the CLAUDE.md, giving AI assistants the structure they need to reason about data mutations without reading source files.

### 5. **Layered Architecture with Directory-Level Enforcement**
The architecture is organized into explicit layers with directory assignments:
- `src/components/` and `src/hooks/` — UI layer (no Firebase)
- `src/repositories/` — Data access layer (Firebase allowed here)
- `src/firebase/` — Firebase initialization

This directory-as-layer pattern means the architecture is visible in the filesystem and enforceable via import rules.

### 6. **Code Style Standards with Specific Examples**
The CLAUDE.md specifies code style at a granular level: function component conventions, TypeScript strict mode patterns, Tailwind class ordering. This level of specificity helps AI assistants match the existing codebase style without reading many files.

## Specific Techniques to Learn

### Dependency Inversion via Named Interface
```typescript
// storage-backend.ts
interface StorageBackend {
  subscribeToAuthState(callback: (user: User | null) => void): Unsubscribe;
  subscribeToEntriesByDate(date: Date, callback: (entries: Entry[]) => void): Unsubscribe;
  // ...
}
```
Name the interface in your CLAUDE.md. The name (`StorageBackend`) becomes a shared vocabulary term that both human contributors and AI assistants can use when discussing architecture.

### Two-Implementation Test for Abstractions
An abstraction is only real if it has two implementations. Documenting both the production implementation and the in-memory/stub implementation in the CLAUDE.md signals that the abstraction is genuine and working.

### Import-Rule Documentation Pattern
```
Rule: Nothing in X or Y may import from Z.
Allowed locations for Z: [explicit list]
```
Stating both what is forbidden AND where the forbidden thing is allowed (explicit allowlist) is more complete than a prohibition alone. It tells contributors where to put Firebase code, not just where not to put it.

## Key Takeaways

1. **Prove your abstractions with a second implementation.** An in-memory backend that passes the same interface means the abstraction is genuine—not just a wrapper with one implementation.
2. **State import rules with explicit allowlists.** "Nothing in X may import from Y" plus "Y belongs only in [exact directories]" is more actionable than "please keep concerns separated."
3. **Name your key interfaces in the CLAUDE.md.** The `StorageBackend` interface name creates shared vocabulary that survives context switches between contributors and AI sessions.
4. **Enforce dependency inversion at the directory level.** Assigning layers to directories makes the architecture visible in the filesystem and checkable via linting or code review.
5. **Document BYOK patterns explicitly.** If your application allows user-supplied credentials or model keys, document the pattern as an architectural decision, not an implementation detail.

## Attribution

This analysis references the original CLAUDE.md from [mariepop13/mivoa](https://github.com/mariepop13/mivoa) (branch: `develop`). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
