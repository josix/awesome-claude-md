# Pydantic GenAI Prices - Python Data Processing Pipeline

## Category: Libraries/Frameworks

**Source Repository:** [pydantic/genai-prices](https://github.com/pydantic/genai-prices)  
**Original CLAUDE.md:** [View Source](https://github.com/pydantic/genai-prices/blob/main/CLAUDE.md)  
**License:** MIT License  
**Domain Expert:** Pydantic Team (Industry-leading Python validation library)

## Overview

This example showcases a comprehensive data processing pipeline for LLM pricing information, demonstrating advanced Python architecture patterns and development workflows from the Pydantic team.

## Key Features That Make This Exemplary

### 1. **Multi-Component Architecture Documentation**
- Clear separation between data sources, processing pipeline, and published package
- Detailed explanation of YAML → JSON → Python package flow
- Explicit warnings about auto-generated files and proper update procedures

### 2. **Comprehensive Development Commands**
- Complete command coverage: setup, development, building, testing, data management
- External API integration commands (Helicone, OpenRouter, LiteLLM)
- Price discrepancy detection and management workflows

### 3. **Production-Ready Practices**
- Strict data integrity rules (`prices_checked` field requirements)
- Automated JSON generation with pre-commit hooks
- Multi-Python version testing (3.9-3.13)
- Comprehensive linting and type checking with basedpyright

### 4. **Domain-Specific Guidance**
- LLM pricing data management best practices
- External API price synchronization patterns
- Data validation and schema building workflows

## Standout Patterns

### Data Pipeline Documentation
```yaml
prices/providers/*.yml → build-prices → data.json → package-data → packages/python/
```

### Command Organization
- **Setup**: `make install`, `make sync`
- **Development**: `make format`, `make lint`, `make typecheck`, `make test`  
- **Data Management**: `make get-all-prices`, `make check-for-price-discrepancies`
- **Building**: `make build-prices`, `make package-data`

### Code Quality Standards
- Ruff formatting with specific style rules (single quotes, 120 char lines)
- Basedpyright type checking in strict mode
- Coverage reporting with HTML output
- UV dependency management (not pip/conda)

## Key Takeaways

1. **Architecture First**: Leading with clear component relationships and data flow before diving into commands
2. **Production Warnings**: Explicit "DO NOT EDIT" warnings for generated files with explanation of proper update procedures  
3. **Command Categorization**: Logical grouping of commands by purpose (setup, development, data management, building)
4. **Tool-Specific Guidance**: Clear preferences for specific tools (UV over pip, basedpyright over mypy) with reasoning

This example demonstrates how domain experts document complex data processing systems for AI assistant collaboration, emphasizing both technical architecture and operational procedures.