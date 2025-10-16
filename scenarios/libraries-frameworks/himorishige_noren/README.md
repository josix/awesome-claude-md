# noren - Edge-Native PII Redaction Library

## Category: Libraries & Frameworks

**Category Rationale**: This edge-native PII redaction library demonstrates unique patterns for privacy-focused applications using Web Standards (WHATWG Streams API). It showcases edge computing architecture, plugin-based extensibility for country-specific PII detection, and MCP (Model Context Protocol) integration. Fills a unique niche for developers building privacy-compliant applications on edge platforms.

## Source Information

- **Repository**: [himorishige/noren](https://github.com/himorishige/noren)
- **CLAUDE.md**: [View Original](https://github.com/himorishige/noren/blob/main/CLAUDE.md)
- **License**: MIT License
- **Language**: TypeScript
- **Topics**: mcp, pii, typescript
- **Discovery Score**: 63/100 points

## Why This Example is Exceptional

This sophisticated PII redaction library demonstrates edge-native architecture with advanced stream processing using Web Standards (WHATWG Streams). Named after the Japanese "noren" curtain, it embodies the principle of protecting without closing the door.

### 1. Stream-First Design
- Uses WHATWG Streams API for efficient processing
- Memory-conscious data handling for large texts
- Backpressure handling built-in
- Compatible across Node.js, Deno, and edge runtimes

### 2. Plugin Architecture
- Country-specific PII detection modules
  - US Social Security Numbers
  - Japan My Number system
  - Security credentials (AWS, API keys)
- Extensible detector interface
- Confidence scoring system per detector

### 3. Performance Optimization
- Pre-compiled regex patterns
- Bundle size reduced from 360KB to 124KB
- Zero external dependencies
- Tree-shakable module structure

### 4. Advanced Detection Features
- Confidence scoring with thresholds
- False positive reduction algorithms
- Contextual pattern matching
- Checksum validation for certain ID types

## Standout Patterns

### Web Standards Compliance
```typescript
// WHATWG Streams API for edge compatibility
const stream = new TransformStream({
  transform(chunk, controller) {
    const redacted = detectAndRedact(chunk);
    controller.enqueue(redacted);
  }
});
```

### Plugin-Based Detection
```typescript
interface PIIDetector {
  name: string;
  detect(text: string): Detection[];
  confidence: number;
}

// Pluggable country-specific detectors
const detectors = [
  new USSocialSecurityDetector(),
  new JapanMyNumberDetector(),
  new AWSCredentialDetector()
];
```

### Edge-Native Architecture
- WebCrypto API for hashing and tokenization
- No Node.js-specific dependencies
- Works on Cloudflare Workers, Deno Deploy, and Vercel Edge
- MCP (Model Context Protocol) integration ready

## Key Takeaways for Developers

1. **Edge-Native Libraries**: Learn how to design libraries using Web Standards for deployment on edge computing platforms, ensuring maximum portability across different JavaScript runtimes without platform-specific dependencies.

2. **Stream Processing**: Implement efficient data processing with WHATWG Streams API for large-scale text handling, enabling memory-efficient processing of documents and real-time data streams.

3. **Privacy Engineering**: Build modular PII detection systems with confidence scoring and false positive reduction, demonstrating how to balance security requirements with usability in production systems.

## Attribution

Original CLAUDE.md created by [himorishige](https://github.com/himorishige) for the noren project. This analysis references the original file under the terms of the MIT License.
