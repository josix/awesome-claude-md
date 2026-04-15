# Stata-MCP - MCP Server for Stata Statistical Analysis

## Category: Developer Tooling

**Category Rationale**: This is the first econometrics and academic computing example in the collection, showcasing how to integrate specialized statistical software with LLMs via the Model Context Protocol. It demonstrates security-conscious tool design with guard systems, RAM monitoring, and hierarchical configuration. Essential for developers building MCP servers, academic computing tools, or LLM integrations with existing software ecosystems.

## Source Information

- **Repository**: [SepineTam/stata-mcp](https://github.com/SepineTam/stata-mcp)
- **CLAUDE.md**: [View Original](https://github.com/SepineTam/stata-mcp/blob/main/CLAUDE.md)
- **License**: AGPL-3.0
- **Language**: Python
- **Stars**: 80
- **Topics**: mcp-server, stata, llm-integration, statistical-computing, fastmcp
- **Discovery Score**: 59/100 points (promoted above threshold for unique domain)

## Key Features That Make This Exemplary

This MCP server showcases how to safely integrate LLMs with specialized academic software. It demonstrates security patterns for command execution, resource monitoring, and cross-platform executable discovery. First example bridging econometrics/statistics with LLM agents.

### 1. Security Guard Pattern

- `GuardValidator`: Validates Stata dofiles against dangerous commands
- Blacklist of prohibited operations (`shell`, `rm`, `! del`)
- Prevents destructive operations before execution
- Configurable via `IS_GUARD` setting

### 2. RAM Monitor Pattern

- `RAMMonitor`: Tracks Stata process memory usage with psutil
- Automatic process termination when RAM exceeds limit
- Configurable via `IS_MONITOR` and `MAX_RAM_MB` settings
- Extensible `MonitorBase` for custom monitors

### 3. Hierarchical Configuration

- Priority: environment variables > config file > defaults
- TOML-based configuration (`~/.statamcp/config.toml`)
- Hot-reload support for configuration changes
- Environment variable prefix (`STATA_MCP_`)

### 4. Cross-Platform Path Resolution

- `StataFinder`: Locates Stata executable on macOS, Windows, Linux
- Platform-specific default paths
- Fallback to system PATH
- Clear error messages for unsupported platforms

## Standout Patterns

### Security Guard System

```python
# GuardValidator checks dofiles against blacklist
validator = GuardValidator()
is_safe = validator.validate(dofile_path)
# Prevents shell commands, file deletions, etc.
```

Proactive security before executing user-provided code.

### Configuration Hierarchy

```toml
# ~/.statamcp/config.toml
[SECURITY]
IS_GUARD = true

[MONITOR]
IS_MONITOR = false
MAX_RAM_MB = -1  # -1 means no limit
```

Environment variables override config file values.

### Cross-Platform Executable Discovery

```python
# StataFinder locates Stata across platforms
finder = StataFinder()
stata_path = finder.find()  # macOS: /Applications/Stata/, Windows: Program Files, Linux: PATH
```

Automatic discovery with clear platform documentation.

### File-Based Working Directory

```
<cwd>/stata-mcp-folder/
├── stata-mcp-log/      # Stata execution logs
├── stata-mcp-dofile/   # Generated do-files
├── stata-mcp-result/   # Analysis results
└── stata-mcp-tmp/      # Temporary files
```

Configurable via `STATA_MCP_CWD` environment variable.

## MCP Tools Provided

- `help`: Get Stata command documentation (macOS/Linux)
- `stata_do`: Execute Stata do-files with logging
- `write_dofile`: Create do-files from code snippets
- `append_dofile`: Append code to existing do-files
- `get_data_info`: Analyze CSV, DTA, XLSX files
- `ado_package_install`: Install Stata packages (SSC, GitHub, net)
- `load_figure`: Load Stata-generated graphs
- `mk_dir`: Create directories safely

## Key Takeaways for Developers

1. **Security Guards for Code Execution**: Implement blacklist-based validation before executing user-provided code. Use abstract base classes (`MonitorBase`) for extensible resource monitoring and automatic termination patterns.

2. **Hierarchical Configuration Systems**: Design configuration with clear precedence (env vars > config file > defaults). Use TOML for human-readable config, provide example files, and document all environment variables with prefixes.

3. **Cross-Platform Executable Discovery**: Build platform-aware finders with fallback chains. Document platform-specific paths clearly, provide graceful error messages, and support system PATH as final fallback.

## Attribution

Original CLAUDE.md created by [Sepine Tam](https://github.com/SepineTam) for the stata-mcp project. This analysis references the original file under the terms of the AGPL-3.0 License.
