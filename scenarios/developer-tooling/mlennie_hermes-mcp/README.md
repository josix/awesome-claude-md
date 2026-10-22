# hermes-mcp: Security Invariants With Their Reasons for an OAuth-Gated MCP Bridge

## Category: Developer Tooling

**Source Repository:** [mlennie/hermes-mcp](https://github.com/mlennie/hermes-mcp)
**Original CLAUDE.md:** [View Source](https://github.com/mlennie/hermes-mcp/blob/main/CLAUDE.md)
**License:** Apache-2.0
**Language:** Python

## Overview

hermes-mcp is an MCP server that lets clients such as Claude Desktop delegate tasks to a locally running Hermes Agent gateway over an HTTPS tunnel, gated by OAuth 2.1 or a static bearer token. Its CLAUDE.md is a compact (~90 lines) model of how to document a security-sensitive service: each module gets a one-paragraph contract, and each hard constraint comes with the reason behind it — including a past regression that was reverted. It also documents deliberate limitations (in-memory tokens, cancellation that cannot kill a thread) so an assistant does not "fix" them naively, and closes with a precise release and deployment-hardening procedure.

## Key Features That Make This Exemplary

### 1. **Constraints Backed by Incident History**
The file doesn't just forbid a change — it explains the exploit and notes that it already happened once:

> **Do not make the static client public (`client_secret=None` / `token_endpoint_auth_method="none"`)**: `/authorize` auto-approves, so that lets anyone with the tunnel URL and the non-secret `client_id` mint tokens — an unreleased build did exactly this and it was reverted.
> — `CLAUDE.md`, Architecture

Recording "we tried this and it was wrong" is one of the most effective ways to stop an AI assistant from repeating a plausible-looking mistake.

### 2. **One-Paragraph Contracts per Module**
Each of the six modules in `src/hermes_mcp/` gets a dense paragraph covering validation rules, TTLs, caps, and invariants — e.g. `jobs.py` is "in-memory only by design," `mark_completed`/`mark_failed` are terminal-state-aware "so a late-finishing worker cannot overwrite a cancellation," and gateway error bodies "are NOT echoed in user-visible errors."

### 3. **Documented Limitations, With the Path Forward**
Instead of hiding a weakness, the file explains why it exists and what fixing it would cost:

> **Cancellation is a tombstone, not a kill switch.** `hermes_cancel` updates this server's bookkeeping; the worker thread keeps running ... If we ever want real cancellation, the path is to rewrite `HermesClient` against `httpx.AsyncClient` ... large refactor, scoped for a future major version.
> — `CLAUDE.md`, Architecture

### 4. **Privacy and Error-Handling Invariants as Rules**
The "Key constraints" section reads like a checklist of invariants: prompt content logged only at DEBUG; async jobs store only `prompt_chars`; unexpected worker exceptions surface as `unexpected error: <ExceptionType>` and never `str(exc)`; refresh-token rotation is "atomic-pop-then-mint." It even gives a regression signal: "Test count is 160 ... a sudden drop is a regression smell."

### 5. **Protect Deployment Hardening from Casual Removal**
The systemd unit's hardening flags (`ProtectSystem=strict`, `MemoryDenyWriteExecute=true`, `SystemCallFilter=@system-service`, …) are listed with an explicit instruction: "do not strip them without intent," and if a dependency needs more, "narrow the rule rather than removing it." The release section similarly explains that the version must match in two files because the release workflow checks it against the tag.

## Specific Techniques to Learn

### Pair every "don't" with the attack or failure it prevents
```
Do not <change>: <mechanism> means <concrete consequence>. A previous build did this and it was reverted.
```

### Document intentional limitations so they aren't "fixed" blindly
```
<Feature> is <limitation> by design. Reason: <constraint>.
Real fix: <approach> — <cost>, scoped for <milestone>.
```

### Give the assistant cheap regression signals
A known test count, a pinned dependency with the reason (`mcp` pinned `<2` because 2.x renamed `FastMCP`), or a "both files must match" rule are easy for an assistant to check before declaring work done.

## Key Takeaways

1. **Explain the threat, not just the rule.** Security constraints stick when the exploit path is spelled out.
2. **Write down reverted mistakes.** Institutional memory of "we tried this" prevents an assistant from re-proposing it.
3. **Separate "by design" from "bug."** Documenting deliberate limitations and their future fix avoids risky drive-by refactors.
4. **Treat ops hardening as code under review.** Tell the assistant to narrow, not remove, security flags.

## Attribution

This analysis references the original CLAUDE.md from [mlennie/hermes-mcp](https://github.com/mlennie/hermes-mcp). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
