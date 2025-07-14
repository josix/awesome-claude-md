# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Instructions for Claude Code

- Look for high-level overview in `docs/` directory
- Check README.md files for package/directory level information
- Check source file comments for more detailed info
- Suggest updates to CLAUDE.md when you find new high-level information

## Project Overview

**workerd** is Cloudflare's JavaScript/WebAssembly server runtime that powers Cloudflare Workers. It's an open-source implementation of the same technology used in production at Cloudflare, designed for self-hosting applications, local development, and programmable HTTP proxy functionality.

## Build System & Commands

### Primary Build System: Bazel

- Main build command: `bazel build //src/workerd/server:workerd`
- Binary output: `bazel-bin/src/workerd/server/workerd`

### Just Commands (recommended for development)

- `just build` or `just b` - Build the project
- `just test` or `just t` - Run all tests
- `just format` or `just f` - Format code (uses clang-format + Python formatter)
- `just stream-test <target>` - Stream test output for debugging
- `just node-test <name>` - Run specific Node.js compatibility tests
- `just wpt-test <name>` - Run Web Platform Tests
- `just generate-types` - Generate TypeScript definitions
- `just compile-commands` - Generate compile_commands.json for clangd support
- `just build-asan` - Build with AddressSanitizer
- `just test-asan` - Run tests with AddressSanitizer

## Testing

### Test Types & Commands

- **Unit Tests**: `.wd-test` files use Cap'n Proto config format
- **C++ Tests**: Traditional C++ unit tests
- **Node.js Compatibility**: `just node-test <test_name>`
- **Web Platform Tests**: `just wpt-test <test_name>`
- **Benchmarks**: `just bench <path>`

## Architecture

- **Cap'n Proto**: Core schemas and configuration format
- **V8 Engine**: JavaScript runtime integration
- **Workers**: Event-driven request/response model
- **Modules**: ES module support with imports
- **Streams**: Web Streams API implementation
- **WebAssembly**: WASM module support

## Key Directories

- `src/workerd/` - Main source code
- `src/workerd/server/` - Server implementation
- `src/workerd/api/` - Web API implementations
- `src/workerd/jsg/` - JavaScript/TypeScript bindings
- `src/workerd/io/` - I/O system
- `src/workerd/util/` - Utility functions
- `samples/` - Example configurations and applications

## Configuration

- Uses `.capnp` files for configuration schemas
- Runtime configuration via `workerd.capnp` format
- Development configs in `samples/` directory

## Development Environment

- **Supported Platforms**: Linux, macOS, Windows (WSL2)
- **Dependencies**: Bazel, Node.js, Python, C++ compiler
- **IDE Support**: VS Code with C++ and Bazel extensions recommended
- **Debugging**: GDB/LLDB supported, Chrome DevTools for JavaScript

## Testing Infrastructure

- **Test Framework**: Custom test runner with `.wd-test` files
- **Coverage**: Built-in code coverage reporting
- **CI/CD**: GitHub Actions for automated testing
- **Performance**: Benchmarking suite for runtime performance

## Deployment

- **Self-hosting**: Can run as standalone server
- **Local development**: Full Workers environment simulation
- **Production**: Same runtime as Cloudflare Workers production