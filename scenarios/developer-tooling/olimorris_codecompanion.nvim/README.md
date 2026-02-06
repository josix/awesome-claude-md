# Analysis: CodeCompanion.nvim - LLM-Powered Neovim Plugin

**Category: Developer Tooling**
**Source**: [olimorris/codecompanion.nvim](https://github.com/olimorris/codecompanion.nvim)
**CLAUDE.md**: [View Original](https://github.com/olimorris/codecompanion.nvim/blob/main/CLAUDE.md)
**License**: Apache-2.0
**Stars**: 6,092

## Why This Example

This CLAUDE.md is a masterclass in documenting a plugin architecture for AI-assisted development. It meticulously maps out the interaction modes, adapter system, tool execution pipeline, and slash command framework of a Neovim plugin that integrates multiple LLM providers. The document demonstrates how to communicate complex plugin architecture to an AI assistant with precision and clarity.

### Key Features That Make This Exemplary

### 1. Interaction Mode Architecture
The document clearly separates and describes four distinct interaction modes: Chat (buffer-based with tools and slash commands), Inline (direct code transformation), Cmd (lightweight query-response), and Workflow (multi-stage prompts with subscribers). This taxonomy gives an AI assistant a complete mental model of the plugin's capabilities.

### 2. Adapter System Documentation
The CLAUDE.md catalogs both HTTP adapters (Anthropic, OpenAI, Copilot, Ollama, Gemini, and many more) and ACP adapters (Claude Code, Auggie CLI, Codex, Gemini CLI) in a structured format. This makes it straightforward for an AI assistant to add new provider integrations following the established patterns.

### 3. Message Flow and Tool Execution Pipeline
A clear data flow diagram shows the path from user input through interactions and adapters to the LLM, and back through parsers and tools to the chat buffer. The tool execution pipeline is documented step-by-step: LLM returns tool calls, orchestrator extracts and validates, tools execute, results sent back. This enables AI assistants to debug issues at any point in the pipeline.

### 4. Lua Development Standards with Function Parameter Patterns
The document specifies a preferred function parameter style using table arguments rather than positional parameters, with concrete before/after examples. This opinionated guidance ensures consistent code generation across the entire codebase.

### 5. Comprehensive File Organization Map
Key files are enumerated with their purposes: plugin entry point, main module, configuration management, type definitions, HTTP client, and a full utilities breakdown. Combined with the naming conventions (snake_case for files/functions, PascalCase for classes, underscore prefix for private functions), this gives an AI assistant everything needed to navigate and extend the codebase.

### 6. Concise Behavioral Directive
The document closes with a clear behavioral instruction: "Do what has been asked; nothing more, nothing less" with explicit prohibitions against creating unnecessary files or documentation. This focused directive prevents AI assistants from overstepping their scope.

## Key Takeaways

1. **Document Plugin Architecture as Interaction Modes** - For plugin systems, organizing documentation around user-facing interaction modes (chat, inline, command, workflow) provides a more intuitive mental model than describing internal implementation details alone.
2. **Show Data Flow Diagrams in Text** - Simple text-based flow diagrams (User Input -> Interaction -> Adapter -> LLM) are highly effective at communicating architecture to AI assistants and cost almost nothing to maintain.
3. **Specify Code Style with Concrete Examples** - Showing preferred patterns (table parameters vs positional parameters) with actual code snippets eliminates ambiguity and produces more consistent AI-generated code.

## Attribution

- **Repository**: [olimorris/codecompanion.nvim](https://github.com/olimorris/codecompanion.nvim)
- **Original CLAUDE.md**: [Direct Link](https://github.com/olimorris/codecompanion.nvim/blob/main/CLAUDE.md)
- **License**: Apache-2.0
- **Creator**: Oli Morris
