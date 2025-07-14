# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Building
- `cargo build` - Build the Rust binary
- `cargo build --release` - Build optimized release version

### Testing
- `cargo test` - Run all tests
- `cargo test --verbose` - Run tests with detailed output
- `cargo test tests/integration_test.rs` - Run specific test file

### Development
- `cargo run -- <input_dir> -o <output_dir>` - Run tlparse with arguments
- `cargo run -- --help` - Show command help
- `cargo check` - Fast compile check without generating binary

### Python Package (via maturin)
- `pip install maturin` - Install build system for Python bindings
- `maturin develop` - Install development version in current Python environment
- `maturin build` - Build Python wheel

### Release Process
1. Update version in `Cargo.toml`
2. Run `cargo update` to update `Cargo.lock`
3. Create release commit and tag (triggers PyPI release)
4. Run `cargo publish` to publish to crates.io

## Code Architecture

### Core Components
**Main Library (`src/lib.rs`)**
- `parse_path()` - Primary entry point that processes TORCH_LOG files
- Handles glog parsing, JSON deserialization, and coordinates all parsers
- Returns `ParseOutput` (vector of file paths and contents to write)
- Supports both regular analysis mode and export mode

**Type System (`src/types.rs`)**
- `Envelope` - Main structured log entry container with all possible metadata fields
- `CompileId` - Unique identifier for compilation attempts
- Various metadata types for different log entry types

**Parser Framework (`src/parsers.rs`)**
- `StructuredLogParser` trait - Implement to create custom analysis parsers
- `get_metadata()` - Filter which log entries a parser processes
- `parse()` - Transform log data into output files or links

**CLI Interface (`src/cli.rs`)**
- Built with `clap` for command-line argument parsing
- Supports input directory, output directory, and export mode options
- Handles file filtering and directory traversal logic

### Analysis Parsers
**Graph Analysis (`src/graph.rs`)**
- Parses compilation graph structure and dependencies
- Generates visualization files and dependency reports
- Tracks module relationships and compilation order

**Compilation Event Parser (`src/compile_event.rs`)**
- Processes compilation timeline events
- Extracts performance metrics and bottlenecks
- Generates compilation timing reports

**Operator Timeline Parser (`src/op_timeline.rs`)**
- Analyzes operator execution timelines
- Tracks GPU/CPU utilization patterns
- Generates performance profiling data

## Development Workflow

### Setting Up Development Environment
1. Install Rust toolchain (rustup recommended)
2. Install Python 3.8+ for Python bindings
3. Install maturin: `pip install maturin`
4. Clone repository and run `cargo build`

### Testing Strategy
- Unit tests for individual parser components
- Integration tests with sample TORCH_LOG files
- Python binding tests via maturin
- Performance benchmarks for large log files

### Code Organization
- `src/` - Main Rust source code
- `tests/` - Integration tests and test data
- `examples/` - Example usage and sample log files
- `python/` - Python binding implementation
- `docs/` - Documentation and user guides

## Key Concepts

### TORCH_LOG Format
- Uses Google's glog format with JSON payloads
- Each log entry has metadata and structured content
- Entries are filtered by compilation ID for analysis

### Parser Extension
- Implement `StructuredLogParser` trait for new analysis types
- Use `get_metadata()` to specify which log entries to process
- Return `ParseOutput` with file paths and contents to write

### Performance Considerations
- Streaming JSON parsing for large log files
- Parallel processing of independent log entries
- Memory-efficient data structures for large datasets

## Common Issues & Solutions

### Build Issues
- Ensure Rust toolchain is up to date
- Check that Python headers are available for maturin
- Verify glog-rs dependency compilation

### Runtime Issues
- Validate TORCH_LOG file format and structure
- Check for sufficient memory when processing large files
- Ensure output directory permissions are correct

### Python Integration
- Use `maturin develop` for local development
- Test Python bindings after Rust changes
- Verify Python package structure matches expectations