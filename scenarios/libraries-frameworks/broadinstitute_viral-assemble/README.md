# Analysis: viral-assemble - Viral Genome Assembly Toolkit

**Category: Libraries & Frameworks**
**Source**: [broadinstitute/viral-assemble](https://github.com/broadinstitute/viral-assemble)
**CLAUDE.md**: [View Original](https://github.com/broadinstitute/viral-assemble/blob/main/CLAUDE.md)
**License**: NOASSERTION
**Stars**: 10

## Why This Example

This CLAUDE.md documents a scientific computing toolkit for viral genome assembly from the Broad Institute, one of the world's leading genomics research institutions. It demonstrates how to onboard an AI assistant to a docker-centric bioinformatics pipeline with modular command registration, conda dependency management, and a layered testing strategy. The document is concise yet comprehensive, covering the full development lifecycle from container setup to CI/CD.

### Key Features That Make This Exemplary

### 1. Docker-Centric Development Paradigm
The document explicitly states that the "development paradigm is intentionally docker-centric" and provides the exact `docker run` command with volume mounts to develop locally inside the viral-core container. This upfront declaration prevents AI assistants from suggesting non-containerized workflows that would fail.

### 2. Command Registration Pattern Documentation
The architecture section explains the command registration system: commands are registered via `__commands__` tuples, each with a parser function and main function connected via `util.cmd.attach_main()`. This pattern documentation enables AI assistants to add new assembly subcommands correctly.

### 3. Assembly Pipeline Flow
The typical assembly workflow is documented as a five-step pipeline: trim_rmdup_subsamp (clean reads), assemble_spades (de novo assembly), order_and_orient (scaffold against reference), impute_from_reference (fill gaps), and refine_assembly (iterative improvement). This pipeline overview gives AI assistants the scientific context for understanding how individual commands fit together.

### 4. Testing Performance Constraints
The document includes a specific testing guideline: "New tests should add no more than ~20-30 seconds to testing time" with slow tests requiring a `@pytest.mark.slow` marker. This practical constraint prevents AI assistants from generating computationally expensive tests that slow down the development cycle.

### 5. Error Handling Taxonomy
Three distinct error types are documented: `DenovoAssemblyError` for assembly failures, `IncompleteAssemblyError` for quality threshold failures, and `PoorAssemblyError` for quality criteria failures. This error taxonomy helps AI assistants implement proper error handling in new assembly code.

### 6. Layered Dependency Architecture
The document maps the dependency relationship with viral-core, listing imported utilities (cmd, file, misc, read_utils) and tool wrappers (picard, samtools, gatk, novoalign, trimmomatic, minimap2). This dependency inventory prevents AI assistants from duplicating functionality already available in the core library.

## Key Takeaways

1. **Declare the Development Paradigm Early** - When a project uses a non-standard development approach (docker-centric, container-first), stating this upfront prevents AI assistants from suggesting incompatible workflows.
2. **Document Testing Performance Budgets** - Setting explicit time budgets for new tests ensures AI assistants generate efficient tests that maintain fast feedback loops, especially important in scientific computing where test data can be large.
3. **Map the Dependency Hierarchy** - For projects that layer on top of a core library, documenting which utilities and tools are inherited from the parent project prevents duplication and ensures consistent usage patterns.

## Attribution

- **Repository**: [broadinstitute/viral-assemble](https://github.com/broadinstitute/viral-assemble)
- **Original CLAUDE.md**: [Direct Link](https://github.com/broadinstitute/viral-assemble/blob/main/CLAUDE.md)
- **License**: NOASSERTION
- **Organization**: Broad Institute of MIT and Harvard
