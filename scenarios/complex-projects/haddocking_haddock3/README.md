# HADDOCK3: Scientific Workflow Engine With a Human-Only Agent Charter

## Category: Complex Projects

**Source Repository:** [haddocking/haddock3](https://github.com/haddocking/haddock3)
**Original CLAUDE.md:** [View Source](https://github.com/haddocking/haddock3/blob/main/CLAUDE.md)
**License:** Apache-2.0
**Language:** Python

## Overview

HADDOCK3 is the modular BioExcel version of HADDOCK, a biomolecular docking platform from BonvinLab at Utrecht University. A workflow engine chains discrete modules, and each module's output (PDB files plus metadata) becomes the next module's input. Sampling and refinement run in CNS, an external Fortran engine. The CLAUDE.md is a strong example from scientific computing. It opens with a guard that says AI agents may never edit the file. It then maps a three-layer architecture (gear, module, CNS), traces how data moves between steps through `io.json`, and documents a parameter-schema system and four execution schedulers (local, HPC batch, MPI, grid) that an agent couldn't infer from the code alone.

## Key Features That Make This Exemplary

### 1. **A Self-Protecting Instruction File**
The file opens by forbidding agents from changing it, even when a user asks them to:

> ```
> > **This file must never be edited, reformatted, or removed by an AI agent,**
> > **for any reason — including to make a task easier, to "align" it with**
> > **code you just wrote, or because a user prompt asks you to.**
> ```
> — `CLAUDE.md`, Agent Guidelines

It also states a stance on existing code: it is "functional" (verified by humans) but not necessarily optimal, so agents should improve code they copy rather than treat it as a model.

### 2. **Explicit Data-Flow Contract Between Workflow Steps**
The architecture section explains how modules communicate, not only what they are. Steps exchange lists of `PDBFile` objects serialised to `io.json` in numbered step folders (`1_topoaa/`, `2_rigidbody/`, …). The file names the classes responsible (`WorkflowManager`, `ModuleIO`) with their `file:Class` locations, so an agent can follow a run from config file to output directory.

### 3. **Module Anatomy and a Template-Based Recipe**
Each module is a folder with `__init__.py` (a `HaddockModule` class that inherits `BaseHaddockModule` or `BaseCNSModule`), a `defaults.yaml` parameter schema, and optionally a `cns/` script directory. The "Adding a New Module" section points to a real template directory (`_template_cat/_template_mod/`) and lists the required hooks (`confirm_installation()`, `_run()`) and the `RECIPE_PATH.name` naming rule.

### 4. **Domain-Specific Configuration Semantics**
The file documents configuration behaviour that would surprise someone used to TOML: section headers can repeat (`[caprieval]` several times), and parameters expand per molecule (`mol_fix_origin_1` → `mol_fix_origin_2`). It also says where each tier of parameters lives (`core/mandatory.yaml`, `core/optional.yaml`, `modules/defaults.yaml`) and lists the schema keys, including the `explevel` tiers (easy/expert/guru/hidden).

### 5. **Pluggable Execution Backends Mapped to Config**
Four schedulers (multiprocessing, SLURM/Torque, MPI, DIRAC grid) are each tied to their implementing class and to the `mode`/`batch_type` config keys that select them. This is useful context for any HPC-oriented codebase.

## Specific Techniques to Learn

### Guard the Instruction File Itself
```
> This file must never be edited by an AI agent. If you believe it should
> change, say so to the user and stop.
```
When a CLAUDE.md encodes design intent, a short guard stops agents from quietly rewriting it to match code they just wrote.

### Document the Inter-Step Contract, Not Just the Steps
```
Step N writes io.json (list of PDBFile) → Step N+1 reads it via ModuleIO
Run dir: 1_<module>/, 2_<module>/, ...
```
For pipeline systems, the serialization format and folder layout are what an agent needs to debug or extend a run.

### Point at a Living Template
Instead of describing module boilerplate in prose, point to a template directory in the repo and list only the hooks and naming rules that must be satisfied.

## Key Takeaways

1. **Protect your agent charter.** A no-edit clause keeps design principles from being changed during routine tasks.
2. **"Works" doesn't mean "exemplary".** Telling agents that existing code is correct but not optimal encourages improvement over cargo-culting.
3. **Explain the data handoff.** In workflow engines, the shared data contract (`io.json`, `PDBFile`) matters more than the list of modules.
4. **Call out non-standard config semantics.** Repeated sections and expandable indexed parameters are exactly what an agent would get wrong.
5. **Tie execution modes to config keys.** Mapping each scheduler class to the setting that selects it makes HPC behaviour easy to reason about.

## Attribution

This analysis references the original CLAUDE.md from [haddocking/haddock3](https://github.com/haddocking/haddock3). All credit for the original documentation belongs to the repository maintainers. Excerpts are quoted for educational analysis under fair use; always refer to the source repository for the full and authoritative document.
