# go-clean-template: Clean Architecture Enforced Through Decision Tables and Named Traps

## Category: Libraries & Frameworks

**Source Repository:** [evrone/go-clean-template](https://github.com/evrone/go-clean-template)
**Original CLAUDE.md:** [View Source](https://github.com/evrone/go-clean-template/blob/master/CLAUDE.md)
**License:** MIT
**Language:** Go

## Overview

go-clean-template is Evrone's widely used reference implementation of Clean Architecture for Go services: three domains (`user`, `task`, `translation`) served over four transports (REST/Fiber, gRPC, RabbitMQ RPC, NATS RPC) from one shared use-case layer. Its CLAUDE.md is notable because it turns architecture into decisions an agent can actually make. A "Use this / Not this" command table explains why each raw tool is the wrong choice. A "where code goes" table is keyed on what the code *knows about*. A six-step handler contract applies to every transport. The document also names the traps (broken Make targets, the linters that reject otherwise valid code, a package that breaks the naming rule) that would otherwise cost an agent several failed attempts.

## Key Features That Make This Exemplary

### 1. **"Use This / Not This" Command Table With Reasons**
The file doesn't just list commands. For each task it pairs the Makefile target with the raw tool an agent would otherwise reach for, and explains why the raw tool behaves differently from CI.

> ```
> | Unit tests | `make test` | `go test ./...` — the target adds `-race -covermode atomic` and scopes to `./internal/... ./pkg/...` |
> | Format | `make format` | `gofmt` — the target runs `go fix`, `gofumpt`, and `gci` with the repo's import grouping |
> ```
> — `CLAUDE.md`, Commands

Below it, a "Three traps" list covers the cases where even the Makefile misleads: `make integration-test` always fails on the host, and `make migrate-create` prints a harmless error after it succeeds.

### 2. **Placement Decided by "What the Code Knows About"**
Instead of describing each layer in prose, the file gives a lookup table: code that knows about SQL or a driver error code goes in `internal/repo/persistent/<domain>/`, and code that knows about an HTTP status or gRPC code goes in a controller. Every row also gives the expected *shape* (method on `UseCase`, method on `Repo`, handler). The file is also honest about where the codebase breaks its own rules: `translation/` declares `package persistent`, and the file says "Follow `task/` and `user/`, not `translation/`."

### 3. **A Six-Step Handler Contract Across Four Transports**
Every controller method gets the caller, decodes into a transport-local DTO, validates, calls the use case, maps the error, and encodes the response. The file gives the transport-specific API for each step and flags subtle bugs:

> ```
> 4. **Call the use case** with the request context: `ctx.UserContext()` in Fiber (**not**
>    `ctx.Context()`, which drops the trace)
> ```
> — `CLAUDE.md`, The handler contract

### 4. **"Conventions That Will Bite You" With Symptoms**
Each convention comes with the confusing symptom you'll see if you break it. Adding a contract method without updating the `traced*` decorator "is a compile error that reads as an unrelated interface mismatch". The file names the specific linters (`wsl_v5`, `nlreturn`, `funlen`, `mnd`, `err113`, `dupl`) that reject code that otherwise looks fine, and gives each one's threshold.

### 5. **Ordered Recipes for Use Cases, Domains, and Multilingual Docs**
The file has an 11-step "Adding a whole domain" walkthrough that works outward from the entity, plus a table mapping each kind of change to the README sections it affects. That table matters because the English, Russian, and Chinese READMEs must mirror each other "section for section, table row for table row", which the file calls "the most common regression in this repo."

## Specific Techniques to Learn

### Pair Every Preferred Command With the Tempting Wrong One
```
| Task | Use this | Not this |
| Unit tests | make test | go test ./... — target adds -race and scopes packages |
```
Agents default to the raw tool. Naming the tool you *don't* want, and giving the reason, stops that default far better than listing only the right command.

### Key Placement Rules on Knowledge, Not Layer Names
```
| The code knows about… | It belongs in | Shape |
| SQL / a driver error  | repo/persistent/<domain>/ | method on Repo |
| an HTTP status        | controller/<transport>/v1/ | handler |
```
Layer names like "domain" or "infrastructure" leave room for interpretation. A question like "what does this code know about?" has one answer.

### Document Errors by Their Symptom
When a mistake shows up as a misleading error (an interface mismatch, `No rule to make target`), write down the message the agent will see so it can recognise the cause instead of chasing it.

## Key Takeaways

1. **Explain why the wrapper exists.** A command table that says *why* `make test` beats `go test` keeps agents from quietly using settings that differ from CI.
2. **Admit the codebase's own inconsistencies.** Pointing out the one package that breaks the pattern stops agents from copying the wrong example.
3. **One contract across many transports.** A numbered, transport-agnostic handler checklist keeps REST, gRPC, AMQP, and NATS handlers aligned.
4. **List the strict linters by name and threshold.** Saying "the linter is strict" is not enough. Name the rules and their limits so code passes on the first attempt.
5. **Treat translated docs as a synchronized set.** A change-to-section table makes multilingual README upkeep a mechanical step.

## Attribution

This analysis references the original CLAUDE.md from [evrone/go-clean-template](https://github.com/evrone/go-clean-template). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
