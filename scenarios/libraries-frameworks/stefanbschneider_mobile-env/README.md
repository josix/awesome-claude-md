# mobile-env: Honest Gotchas and Extension Seams for a Gymnasium RL Environment

## Category: Libraries & Frameworks

**Source Repository:** [stefanbschneider/mobile-env](https://github.com/stefanbschneider/mobile-env)
**Original CLAUDE.md:** [View Source](https://github.com/stefanbschneider/mobile-env/blob/main/CLAUDE.md)
**License:** MIT
**Language:** Python

## Overview

mobile-env is a minimalist Gymnasium environment for reinforcement learning on autonomous coordination in wireless mobile networks (base stations, user equipment, scheduling, mobility). Its CLAUDE.md is compact (~115 lines) but unusually dense: instead of restating the README, it explains *how the library is wired* — import-time environment registration, a strategy-pattern config made of classes, and the handler layer that forms the Gym seam — and then closes with a "Gotchas" section that candidly documents real bugs and documentation errors in the codebase. It reads like notes from a maintainer who has actually traced the code, which is exactly what an AI assistant needs.

## Key Features That Make This Exemplary

### 1. **Commands That Mirror CI Exactly**
Every test and lint command is tied to the CI workflow, including how to run a single parametrized case and the fact that notebooks are tested too.

> ```
> pytest tests/test_env_stepping.py -k "small and central"     # single parametrized case
> pytest --nbmake examples/test.ipynb                          # notebooks are part of CI
> ruff check .                                                  # lint, exact CI invocation
> ```
> — `CLAUDE.md`, Commands

It also flags environment traps, e.g. that `docs/requirements.txt` pins old Sphinx versions and RTD builds on Python 3.8, so a local docs build "may need its own virtualenv."

### 2. **Explains Import-Side-Effect Registration**
The file traces the exact import chain that registers the `mobile-{scenario}-{handler}-v0` environments and explains a puzzling code pattern as a consequence:

> Registration is a pure import side effect, which is why tests import `mobile_env` with `# noqa: F401`.
> — `CLAUDE.md`, Architecture → Environment registration

Explaining *why* odd-looking code exists prevents an assistant from "cleaning up" an unused import and silently breaking registration.

### 3. **Documents the Extension Recipe for a Strategy-Pattern Config**
`default_config()` returns classes paired with `<name>_params` dicts, merged via `deep_dict_merge`, with deterministic per-component seeds. The CLAUDE.md turns this into an actionable rule: subclass the base in `mobile_env/core/`, then set both `config['<name>']` and `config['<name>_params']` — "no source changes needed." It similarly spells out the three places that must change to add an observation feature: `features()`, `feature_sizes`, and the handler's `features` list.

### 4. **`step()` Semantics Worth Knowing**
A short list captures non-obvious runtime behaviour that would otherwise take a debugger session to discover:

> - `terminated` is always `False`; `truncated` is `time_is_up`, ...
> - `if not self.active and not self.time_is_up: return self.step({})` — a single `env.step()` call can
>   advance several simulation time steps when no UE is requesting service.
> — `CLAUDE.md`, Architecture → `step()` semantics worth knowing

### 5. **A Candid "Gotchas" Section Listing Known Bugs**
Rather than describing the code as it should be, the file records where it is wrong: `MComCentralHandler.check()` asserts a (always-truthy) list comprehension so a constraint is not enforced; `RateFair` is broken as a drop-in scheduler (returns a scalar, divides by zero); and the README's import path `mobile_env.core.channel` is wrong — "The README snippet fails verbatim." This keeps an assistant from trusting stale docs or building on broken components.

## Specific Techniques to Learn

### Explain the "why" behind suspicious-looking code
```
Registration is a pure import side effect, which is why tests import `pkg` with `# noqa: F401`.
```
One sentence prevents an entire class of well-intentioned but destructive "cleanups."

### Write "touch N places" checklists for cross-cutting changes
```
Adding an observation feature requires touching three places: features(), feature_sizes,
and the handler's features list.
```

### Keep a gotchas list of known-broken code and wrong docs
Name the exact class/function, describe the failure mode, and say what to use instead. Treat the CLAUDE.md as the most honest document in the repo.

## Key Takeaways

1. **Tie commands to CI.** Saying "exact CI invocation" removes guesswork about which lint/test flags actually gate merges.
2. **Document the extension seams, not just the modules.** Tell the assistant how to add a component without editing core code.
3. **Capture runtime semantics that surprise people.** Recursion in `step()` or always-`False` flags are what cause subtle RL bugs.
4. **Be candid about known bugs and doc errors.** A gotchas section that says "this is broken" is more useful than a polished architecture overview.

## Attribution

This analysis references the original CLAUDE.md from [stefanbschneider/mobile-env](https://github.com/stefanbschneider/mobile-env). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
