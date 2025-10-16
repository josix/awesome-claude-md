# claude-code-mastra - Claude Code SDK Integration for Mastra Framework

## Category: Developer Tooling

**Category Rationale**: This integration library demonstrates clean adapter patterns for AI SDK interoperability, specifically bridging Claude Code SDK with Mastra (an AI agent framework). It showcases essential patterns for tool conflict resolution, protocol translation, and session lifecycle management. Valuable for developers building integrations between different AI frameworks and SDKs.

## Source Information

- **Repository**: [t3ta/claude-code-mastra](https://github.com/t3ta/claude-code-mastra)
- **CLAUDE.md**: [View Original](https://github.com/t3ta/claude-code-mastra/blob/main/CLAUDE.md)
- **License**: MIT License
- **Language**: TypeScript
- **Stars**: 9
- **Discovery Score**: 66/100 points

## Why This Example is Exceptional

This focused integration library demonstrates clean adapter patterns for bridging Claude Code SDK with the Mastra framework (an AI agent development framework), showing excellent session management and tool conflict resolution. Mastra provides infrastructure for building AI agents, and this adapter enables seamless integration with Claude Code tooling.

### 1. Tool Bridge Architecture
- Automatic conflict resolution between different SDK tools
- Intelligent tool merging with deduplication
- Priority-based tool selection
- Unified tool interface across frameworks

### 2. Message Conversion
- Multi-layer message format translation
- Protocol mapping between Claude Code and Mastra
- Bidirectional communication handling
- Type-safe message transformations

### 3. Session Lifecycle Management
- Automatic 30-second cleanup using WeakMap
- Ephemeral connection patterns
- Memory leak prevention
- Graceful session termination

### 4. JSON Tool Processing
- Intelligent tool call detection in messages
- JSON parsing with error recovery
- Tool invocation result handling
- Proper error propagation

## Standout Patterns

### Adapter Pattern Implementation
```typescript
class ClaudeCodeMastraAdapter {
  constructor(
    private claudeSDK: ClaudeCodeSDK,
    private mastraFramework: Mastra
  ) {}

  // Bridge tool definitions
  private mergeTools(
    claudeTools: Tool[],
    mastraTools: Tool[]
  ): Tool[] {
    // Intelligent deduplication and conflict resolution
  }
}
```

### Session Management
```typescript
// WeakMap for automatic cleanup
private sessions = new WeakMap<Session, Timer>();

createSession(config: SessionConfig): Session {
  const session = new Session(config);

  // Auto-cleanup after 30 seconds
  const timer = setTimeout(() => {
    this.cleanupSession(session);
  }, 30000);

  this.sessions.set(session, timer);
  return session;
}
```

### Tool Conflict Resolution
```typescript
// Priority-based tool selection
function resolveToolConflict(
  tool1: Tool,
  tool2: Tool
): Tool {
  // Claude Code tools take precedence
  if (tool1.source === 'claude-code') return tool1;
  // Mastra-specific tools for framework operations
  if (tool2.category === 'framework') return tool2;
  // Merge capabilities if compatible
  return mergeTools(tool1, tool2);
}
```

### Protocol Translation
```typescript
// Message format conversion
function translateMessage(
  claudeMessage: ClaudeMessage
): MastraMessage {
  return {
    role: mapRole(claudeMessage.role),
    content: convertContent(claudeMessage.content),
    toolCalls: extractToolCalls(claudeMessage),
    metadata: preserveMetadata(claudeMessage)
  };
}
```

## Key Takeaways for Developers

1. **Framework Adapters**: Learn how to create clean adapters between different AI framework SDKs, demonstrating proper separation of concerns, protocol translation, and unified interfaces for seamless interoperability.

2. **Session Management**: Implement ephemeral connection patterns with automatic cleanup and resource management, using modern JavaScript features like WeakMap to prevent memory leaks in long-running applications.

3. **Tool Integration**: Handle tool registration conflicts and build unified tool interfaces across frameworks, showing patterns for tool deduplication, priority resolution, and capability merging.

## Attribution

Original CLAUDE.md created by [t3ta](https://github.com/t3ta) for the claude-code-mastra project. This analysis references the original file under the terms of the MIT License.
