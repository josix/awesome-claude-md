# OAuth2 Passkey - Modern Authentication Library

## Source Repository
- **Repository**: [ktaka-ccmp/oauth2-passkey](https://github.com/ktaka-ccmp/oauth2-passkey)
- **CLAUDE.md**: [Link to original file](https://github.com/ktaka-ccmp/oauth2-passkey/blob/main/CLAUDE.md)
- **Language**: Rust
- **Stars**: 5
- **License**: To be verified

## Category Assignment
**Category**: `libraries-frameworks`

**Rationale**: This repository demonstrates advanced authentication library design patterns in Rust, with comprehensive documentation of layered architecture, security-first design principles, and modern authentication protocols that serve as excellent educational material for library development.

## Key Educational Features

### 1. Layered Library Architecture
- Clear separation between core authentication logic (`oauth2_passkey/`) and web framework integration (`oauth2_passkey_axum/`)
- Coordination layer orchestrating all authentication flows with centralized control
- Flexible storage abstraction supporting both development (SQLite, in-memory) and production (PostgreSQL, Redis) configurations

### 2. Security-First Design Principles
- Built-in CSRF protection, secure sessions, and page session tokens
- Comprehensive error handling using `thiserror` crate (appropriate for library design)
- Minimal dependency approach reducing attack surface and maintenance burden

### 3. Publication-Ready Development Standards
- Code designed for crates.io publication with comprehensive documentation
- Strict code quality standards: "fix ALL warnings before committing code"
- Comprehensive testing strategy with unit, integration, and functional tests

## Key Takeaways for Developers

1. **Modern Authentication Patterns**: Demonstrates how to implement OAuth2 and WebAuthn/Passkey authentication with proper security practices and flexible configuration options.

2. **Library Design Excellence**: Shows how to structure Rust libraries with clear API boundaries, minimal public interfaces, and comprehensive documentation for publication.

3. **Security-Focused Development**: Provides excellent examples of security-first design thinking, from architecture decisions to development workflow practices.

## Distinctive Patterns

- **Coordination Layer Pattern**: Central orchestration of complex authentication flows with clear separation of concerns
- **Dual Storage Strategy**: Flexible configuration supporting both development simplicity and production scalability
- **Security by Design**: Comprehensive security implementation including CSRF protection and secure session management
- **Publication-Ready Standards**: Development practices specifically designed for open source library distribution
