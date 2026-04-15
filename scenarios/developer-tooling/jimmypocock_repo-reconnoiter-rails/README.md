# repo-reconnoiter-rails: Cost-First Rails OSINT Dashboard with AI-Prompt-as-Code Pattern

## Category: Developer Tooling

**Source Repository:** [jimmypocock/repo-reconnoiter-rails](https://github.com/jimmypocock/repo-reconnoiter-rails)
**Original CLAUDE.md:** [View Source](https://github.com/jimmypocock/repo-reconnoiter-rails/blob/main/CLAUDE.md)
**License:** Not specified
**Language:** Ruby

## Overview

repo-reconnoiter-rails is a Rails 8.1 OSINT dashboard that analyzes GitHub trending repositories using AI, with multi-query parsing and three-tier AI analysis (gpt-5-mini for categorization, gpt-5 for deep analysis). Its CLAUDE.md stands out for putting "Cost Control" as the first and most prominent core principle—before architecture, before testing, before anything else. The document also introduces the "Doer" naming convention with explicit ✅/❌ examples and documents AI prompts stored as versioned ERB templates, treating prompt engineering as a first-class software engineering concern.

## Key Features That Make This Exemplary

### 1. **"Cost Control" as First Core Principle**
Most CLAUDE.md files open with architecture or tech stack. This one opens with money.

> ```
> ## Core Principles
> 1. **Cost Control**: Keep AI API costs under $10/month through automatic tracking, caching, and smart model selection
> 4. **Automatic Tracking**: The `OpenAi` service automatically tracks all API costs - never call OpenAI directly
> ```
> — `CLAUDE.md`, Core Principles section

Making cost a first-class constraint changes how AI assistants reason about implementation choices. Every new feature proposal is evaluated against the $10/month budget, not just technical correctness.

### 2. **"Doer" Service Naming Convention with ✅/❌ Examples**
The document specifies a naming convention for service objects and enforces it with concrete counterexamples.

> ```
> ## Service Naming Convention ("Doer" Pattern)
> - ✅ `Prompter` (renders AI prompts)
> - ❌ ~~`PromptService`~~ (too verbose)
> ```
> — `CLAUDE.md`, Service Naming Convention section

Using strikethrough for incorrect names is a small formatting choice that has outsized effect: the ❌ example with strikethrough is visually harder to copy by mistake than a simple "don't do this" paragraph.

### 3. **Prompt-as-Code: ERB Templates in `app/prompts/`**
AI prompts are versioned ERB templates in `app/prompts/`, not hardcoded strings in service methods. This is the "prompt as code" pattern applied in a Rails context.

> ```
> 5. **Prompt as Code**: AI prompts are versioned ERB templates in `app/prompts/`, not hardcoded strings
> ```
> — `CLAUDE.md`, Core Principles section

The implication: prompts are testable, diffable, and reviewable via standard code review. Changing a prompt is a code change, not a configuration change buried in a string literal.

### 4. **Two-Layer API Authentication Architecture**
The CLAUDE.md explains both the internal API auth (HTTP header for frontend-to-Rails communication) and the external AI API key management (secret management for OpenAI keys). Both layers are explicitly documented with their rationale.

### 5. **$10/Month Cost Target as an Engineering Constraint**
The cost target is not aspirational—it is described as "automatic tracking" via a service that intercepts all OpenAI calls. This makes the constraint implementable: the `OpenAi` service is the single enforcement point, and the CLAUDE.md tells contributors not to bypass it.

### 6. **Full CI Command Suite**
The document lists all commands needed for development, testing, and CI:
- `rails test` for unit/integration
- `rails test:system` for browser tests
- `rubocop` for linting
- `brakeman` for security scanning

Having security scanning (`brakeman`) in the standard CI command list reflects production-mindedness: security is not a one-time audit, it is part of the regular development loop.

## Specific Techniques to Learn

### Cost as Architecture Constraint
```
Core Principles:
1. Cost Control: <$10/month via caching, smart model selection, automatic tracking
Never call [AI provider] directly — always go through the cost-tracking service
```
Placing a financial constraint at the top of the core principles list changes how all subsequent decisions are evaluated. Especially useful for AI-powered applications where API costs can spiral quickly.

### "Doer" Naming Convention Pattern
In Rails (and similar service-oriented architectures), naming services after what they do (verbs → nouns: "Prompter", "Fetcher", "Analyzer") rather than using `*Service` suffixes reduces cognitive overhead. Document the convention with both the positive and negative example:
```
✅ Prompter
❌ ~~PromptService~~
```

### Prompt-as-ERB-Template Pattern
```
app/prompts/
  categorize_repo.html.erb
  deep_dive_analysis.html.erb
```
Storing AI prompts as versioned template files (not string literals) enables:
- Git history on prompt changes
- Code review for prompt edits
- Standard testing via template rendering tests
- Reuse across controllers without duplication

## Key Takeaways

1. **Lead with your most important constraint.** If cost is your first-class concern, make it Principle #1—not an afterthought in the infrastructure section.
2. **Use ✅/❌ formatting with strikethrough for naming conventions.** The visual contrast makes the incorrect pattern harder to accidentally copy than prose instructions.
3. **Treat AI prompts as code.** Storing prompts as versioned template files gives them the same benefits as source code: history, review, testing, and reuse.
4. **Create a single enforcement point for cross-cutting concerns.** A cost-tracking service that intercepts all AI API calls is more reliable than trusting contributors to track costs manually.
5. **Include security scanning in the standard CI suite.** `brakeman` (or equivalent) in the normal test command signals that security is not optional.

## Attribution

This analysis references the original CLAUDE.md from [jimmypocock/repo-reconnoiter-rails](https://github.com/jimmypocock/repo-reconnoiter-rails). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
