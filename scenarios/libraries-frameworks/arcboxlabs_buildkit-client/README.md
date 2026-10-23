# buildkit-client: Protocol-Level Debugging Guide for a Rust BuildKit Session Implementation

## Category: Libraries & Frameworks

**Source Repository:** [arcboxlabs/buildkit-client](https://github.com/arcboxlabs/buildkit-client)
**Original CLAUDE.md:** [View Source](https://github.com/arcboxlabs/buildkit-client/blob/master/CLAUDE.md)
**License:** Apache-2.0
**Language:** Rust

## Overview

buildkit-client is a Rust library and CLI that talks to moby/buildkit over gRPC and implements the BuildKit session protocol: bidirectional streaming, fsutil DiffCopy file sync, and an HTTP/2 server tunneled inside a gRPC stream. Its CLAUDE.md is a strong example of documenting an undocumented wire protocol for an AI assistant. It walks through a build step by step, specifies packet ordering and ID rules for DiffCopy, shows a nested-loop bug pattern in code, and maps each cryptic BuildKit error message ("no active session", "changes out of order") to its root cause. Anyone building a client for a complex third-party protocol can borrow this structure.

## Key Features That Make This Exemplary

### 1. **Numbered End-to-End Data Flow**
A ten-step flow goes from `BuildKitClient.build(config)` through session creation, the HTTP/2 tunnel, `control.solve`, BuildKit's callbacks (DiffCopy, Credentials, Health), and the STAT/REQ/DATA/FIN packet exchange, ending with the returned digest. An assistant can find where any bug sits in the sequence.

### 2. **Protocol Invariants Stated as Hard Rules**
The DiffCopy section lists rules that are easy to get wrong and hard to debug:

> - IDs are assigned to ALL entries (files + directories), not just files
> - Root directory itself gets NO STAT packet, only its children
> - Mode bits must be in **Go FileMode format** - use the `filemode` crate for conversion
> - Empty packets signal EOF, not FIN (FIN is for entire transfer)
> — `CLAUDE.md`, DiffCopy File Sync

### 3. **A Bug Pattern Shown as Annotated Code**
The "Nested Loop Exit Pattern" shows a Rust loop where `break` exits only the inner `while`. Comments (`⚠️ Only exits inner while loop!`, `✅ MUST check flag and break outer loop`) mark the problem, followed by the symptom: "Without the flag check, outer loop continues waiting → timeout."

### 4. **Error Message → Root Cause Troubleshooting**
"Common Issues" is organized by the exact error string a developer will see, with likely causes under each:

> ### "changes out of order" error
> - fsutil/validator requires files in depth-first traversal order
> - Use depth-first recursive sending, NOT collect-and-sort approach
> — `CLAUDE.md`, Common Issues

### 5. **What the Client Should *Not* Do**
The `.dockerignore` section says the client sends all files and BuildKit filters them on the server, and cites the BuildKit PR that introduced this. That stops an assistant from adding plausible-looking but wrong client-side filtering.

## Specific Techniques to Learn

### Scoped Trace Logging Recipes
```bash
RUST_LOG=info,my_crate::session::tunnel=trace cargo run -- <cmd>
```
Give the assistant copy-pasteable logging commands scoped to the module you are debugging, so it gets frame-level detail without noise from the rest of the program.

### Key Troubleshooting Sections by Literal Error Strings
```markdown
### "invalid file request N" error
- File ID mismatch between STAT packets and file_map
- IDs must increment for ALL entries (files + dirs)
```
When an assistant sees an error, it can search CLAUDE.md for the string and land on the cause.

### Point to the Reference Implementation Precisely
The file directs readers to specific files in the upstream reference (`fsutil`'s `send.go` and `receive.go`) for protocol behavior. Precise pointers keep an agent from guessing about third-party semantics.

## Key Takeaways

1. **Spell out wire-protocol invariants.** Packet ordering, ID assignment and EOF-vs-FIN rules are exactly what an assistant cannot infer from types alone.
2. **Show bugs as annotated code.** A five-line loop with ⚠️/✅ comments teaches more than a paragraph about control flow.
3. **Index troubleshooting by the exact error message.** It is the fastest path from symptom to cause for both humans and agents.
4. **Document what the client must not do.** Stating that responsibility sits on the server (as with `.dockerignore`) prevents well-meant but wrong code.

## Attribution

This analysis references the original CLAUDE.md from [arcboxlabs/buildkit-client](https://github.com/arcboxlabs/buildkit-client). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
