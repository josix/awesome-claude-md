# noren - Edge-Native PII Redaction Library

**Score**: 63/100 (Good)

## Source Repository

- **Repository**: [himorishige/noren](https://github.com/himorishige/noren)
- **CLAUDE.md**: [View Original](https://github.com/himorishige/noren/blob/main/CLAUDE.md)
- **License**: MIT License
- **Language**: TypeScript
- **Topics**: mcp, pii, typescript

## Category Assignment

**Category**: `libraries-frameworks`

**Rationale**: This edge-native PII redaction library demonstrates unique patterns for privacy-focused applications using Web Standards (WHATWG Streams API). It showcases edge computing architecture, plugin-based extensibility for country-specific PII detection, and MCP (Model Context Protocol) integration. Fills a unique niche for developers building privacy-compliant applications on edge platforms.

## Why This Example Was Selected

This sophisticated PII redaction library demonstrates edge-native architecture with advanced stream processing using Web Standards (WHATWG Streams). Named after the Japanese "noren" curtain, it embodies the principle of protecting without closing the door.

### Unique Features

1. **Stream-First Design**: Uses WHATWG Streams API for efficient, memory-conscious data processing
2. **Plugin Architecture**: Country-specific PII detection modules (US SSN, Japan My Number, security credentials)
3. **Performance Optimization**: Pre-compiled regex patterns reduced bundle from 360KB to 124KB
4. **Confidence Scoring System**: Advanced false positive reduction with confidence thresholds

### What Makes It Stand Out

- **Web Standards Compliance**: Built on WHATWG Streams for maximum portability across Node.js, Deno, and edge runtimes
- **Modular Detector System**: Clean separation of detection logic by country/category with extensible plugin interface
- **WebCrypto Integration**: Uses native crypto APIs for hashing and tokenization
- **Zero Dependencies**: Lightweight implementation focused on edge deployment

## Key Takeaways for Developers

1. **Edge-Native Libraries**: Learn how to design libraries using Web Standards for deployment on edge computing platforms
2. **Stream Processing**: Implement efficient data processing with WHATWG Streams API for large-scale text handling
3. **Privacy Engineering**: Build modular PII detection systems with confidence scoring and false positive reduction

## Attribution

Original CLAUDE.md created by [himorishige](https://github.com/himorishige) for the noren project. This analysis references the original file under the terms of the MIT License.
