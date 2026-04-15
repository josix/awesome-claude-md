# ada - WHATWG-Compliant C++ URL Parser

## Category: Libraries & Frameworks

**Category Rationale**: This is the first C++ library example in the collection, showcasing industry-leading performance optimization patterns and CMake development workflow practices. It demonstrates C++ best practices for building high-performance parsers with comprehensive testing and benchmarking infrastructure. Essential for developers working on performance-critical C++ libraries and learning rigorous development methodology.

## Source Information

- **Repository**: [ada-url/ada](https://github.com/ada-url/ada)
- **CLAUDE.md**: [View Original](https://github.com/ada-url/ada/blob/main/CLAUDE.md)
- **License**: Apache-2.0
- **Language**: C++
- **Stars**: 1689
- **Topics**: url-parser, c++, whatwg, performance, cmake
- **Discovery Score**: 60/100 points

## Key Features That Make This Exemplary

This C++ URL parser library showcases production-grade development practices for high-performance systems. Used by Node.js, Cloudflare Workers, Telegram, and Datadog, it demonstrates how to structure C++ projects for both correctness and extreme performance.

### 1. Development Checks Concept

- Clear distinction between debug assertions and release builds
- Automatic enabling/disabling based on build configuration
- Explicit guidance on when development checks should be active
- Prevents common pitfalls (benchmarking with checks enabled)

### 2. CMake Development Workflow

- Comprehensive CMake option documentation in table format
- Separate build configurations for testing vs benchmarking
- Clear commands for common development tasks
- Platform-specific notes (Windows config handling)

### 3. Benchmark Methodology

- Explicit warnings about performance measurement correctness
- Multiple benchmark targets for different scenarios (BBC URLs, WPT, percent encoding)
- Required flags documented (`-DCMAKE_BUILD_TYPE=Release`)
- Ninja build system recommendation for faster iteration

### 4. Summary Task-to-Command Table

- Quick reference at the end showing task -> command -> state
- Reduces cognitive load for common operations
- Shows tradeoffs clearly (testing vs benchmarking modes)

## Standout Patterns

### Development vs Production Build Modes

```bash
# Testing (development checks ENABLED)
cmake -B build -DADA_TESTING=ON && cmake --build build

# Benchmarking (development checks DISABLED for accurate performance)
cmake -B build -DADA_BENCHMARKS=ON -DCMAKE_BUILD_TYPE=Release && cmake --build build
```

Clear documentation of when assertions should be active vs disabled.

### CMake Build Options Table

| Option | Default | Description |
|--------|---------|-------------|
| `ADA_TESTING` | OFF | Enable building tests |
| `ADA_BENCHMARKS` | OFF | Enable building benchmarks |
| `CMAKE_BUILD_TYPE` | - | Release for optimized builds |

Comprehensive reference for all configuration options.

### Clang-Tidy Integration

```bash
# During build with proper compiler selection
cmake -B build -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_CLANG_TIDY=clang-tidy
```

Documents why clang++ is required (GCC-specific flags incompatibility).

### Platform-Specific Notes

- Windows: Explicit config flag during build
- Ninja: Recommended for faster builds across platforms
- Cross-platform testing infrastructure

## Key Takeaways for Developers

1. **Performance Measurement Discipline**: Document exactly how to disable debug checks for accurate benchmarks. Prevent common mistake of measuring debug builds and drawing wrong conclusions about performance.

2. **CMake Best Practices**: Use clear option flags, provide table-based documentation of all build options, separate concerns (testing vs benchmarking configurations), and explain the "why" behind configuration choices.

3. **Development Workflow Documentation**: Provide complete workflow examples from initial setup through development cycle to performance validation. Show concrete commands for every common task with explanation of what each flag does.

## Attribution

Original CLAUDE.md created by the [ada-url](https://github.com/ada-url) team for the ada project. This analysis references the original file under the terms of the Apache-2.0 License.
