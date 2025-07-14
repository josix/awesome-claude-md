# Awesome Claude.md

A curated collection of high-quality `claude.md` files from leading open-source projects. These examples demonstrate industry best practices for onboarding AI assistants to complex codebases.

## What is claude.md?

The `claude.md` file is a project documentation format designed to help AI assistants understand codebases quickly and effectively. It provides context about architecture, development workflows, testing strategies, and project-specific conventions.

## Categories

### 🏗️ Infrastructure Projects

Large-scale systems and runtime environments that power modern applications.

- **[Cloudflare workerd](scenarios/infrastructure-projects/cloudflare_workerd/analysis.md)** - JavaScript/WebAssembly runtime powering Cloudflare Workers (6,865 stars)
  - Dual build systems (Bazel + Just)
  - Comprehensive testing strategy across multiple environments
  - Production deployment guidance

### 🏢 Complex Projects

Multi-service applications with sophisticated architectures and enterprise-scale concerns.

- **[Microsoft Semantic Workbench](scenarios/complex-projects/microsoft_semanticworkbench/analysis.md)** - AI assistant prototyping platform (325 stars)
  - AI context generation system
  - Service orchestration patterns
  - Multi-language architecture

- **[Sentry](scenarios/complex-projects/getsentry_sentry/README.md)** - Error tracking and performance monitoring (40,000+ stars)
  - Microservices architecture
  - Real-time data processing
  - Enterprise deployment patterns

- **[TimeWarp Architecture](scenarios/complex-projects/TimeWarpEngineering_timewarp-architecture/README.md)** - .NET distributed application framework (100+ stars)
  - Event sourcing and CQRS patterns
  - Distributed system design
  - Modern .NET practices

- **[Platformatic](scenarios/complex-projects/platformatic_platformatic/README.md)** - Node.js application platform (1,000+ stars)
  - Multi-service coordination
  - API gateway patterns
  - Development environment setup

- **[Webhook Broker](scenarios/complex-projects/newscred_webhook-broker/README.md)** - High-throughput webhook delivery system (200+ stars)
  - Event-driven architecture
  - Message queuing patterns
  - Scalability considerations

### 🛠️ Developer Tooling

CLI tools, build systems, and developer productivity solutions.

- **[Cloudflare Workers SDK](scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md)** - Official SDK and CLI for Cloudflare Workers (3,271 stars)
  - Strict package management conventions
  - Monorepo architecture patterns
  - Advanced testing tiers

- **[PyTorch tlparse](scenarios/developer-tooling/pytorch_tlparse/analysis.md)** - Log parsing and analysis tool (46 stars)
  - Dual-language development (Rust/Python)
  - Extensible parser framework
  - Performance optimization techniques

- **[Lerna](scenarios/developer-tooling/lerna_lerna/README.md)** - Monorepo management tool (35,000+ stars)
  - Multi-package workflows
  - Release management
  - CI/CD integration

- **[Kubb](scenarios/developer-tooling/kubb-labs_kubb/README.md)** - API toolkit for code generation (2,000+ stars)
  - Plugin architecture
  - OpenAPI code generation
  - TypeScript integration

- **[mypy-boto3-builder](scenarios/developer-tooling/youtype_mypy-boto3-builder/README.md)** - Type generation for AWS SDK (2,000+ stars)
  - Sophisticated type generation
  - Multi-package publishing
  - Documentation automation

- **[HWP](scenarios/developer-tooling/mcollina_hwp/README.md)** - High-performance web platform (by Node.js TSC member)
  - Expert-level Node.js patterns
  - Performance optimization
  - Production deployment

- **[Kotlinter Gradle](scenarios/developer-tooling/jeremymailen_kotlinter-gradle/README.md)** - Kotlin code formatting plugin (500+ stars)
  - Gradle plugin development
  - Code quality automation
  - CI/CD integration

### 📚 Libraries & Frameworks

Reusable components, SDKs, and framework implementations.

- **[LangChain Redis](scenarios/libraries-frameworks/langchain-ai_langchain-redis/analysis.md)** - Redis integration for LangChain (34 stars)
  - Comprehensive testing architecture
  - Sophisticated configuration system
  - Production-ready workflows

- **[Composio](scenarios/libraries-frameworks/ComposioHQ_composio/README.md)** - AI agent integration platform (10,000+ stars)
  - Multi-platform SDK architecture
  - Comprehensive API coverage
  - Integration patterns

- **[Agentic](scenarios/libraries-frameworks/transitive-bullshit_agentic/README.md)** - LLM tool integration framework (2,000+ stars)
  - Innovative tool abstractions
  - Multi-model support
  - Type-safe implementations

- **[DataFog Python](scenarios/libraries-frameworks/DataFog_datafog-python/README.md)** - Data privacy and masking library (500+ stars)
  - Privacy-focused patterns
  - Data transformation pipelines
  - Compliance considerations

- **[GenSX](scenarios/libraries-frameworks/gensx-inc_gensx/README.md)** - Code generation framework (200+ stars)
  - Template-based generation
  - Multi-language support
  - Extensible architecture

### 🚀 Getting Started

Projects focused on developer onboarding and initial setup experiences.

- **[Ethereum.org Website](scenarios/getting-started/ethereum_ethereum-org-website/README.md)** - Official Ethereum community website (5,000+ stars)
  - Community-driven development
  - Multi-language support
  - Documentation workflows

### 🔄 Project Handoffs

Documentation focused on project state, blocking issues, and transition planning.

- **[Mattermost Test Management](scenarios/project-handoffs/mattermost_mattermost-test-management/README.md)** - Enterprise test management system
  - Current project state
  - Blocking issues documentation
  - Transition planning

## Quality Standards

All examples in this collection meet these criteria:

- **Industry Recognition**: From organizations with proven track records
- **Production Usage**: Actively maintained and used in production environments
- **Comprehensive Documentation**: Detailed architecture, setup, and workflow information
- **Best Practices**: Demonstrate advanced patterns and techniques
- **AI-Friendly**: Structured to maximize AI assistant effectiveness

## Contributing

When adding new examples:

1. **Focus on Quality**: Prioritize examples from established projects (1,000+ stars preferred)
2. **Preserve Originality**: Keep `claude.md` files exactly as they appear in source repositories
3. **Provide Analysis**: Create detailed `analysis.md` files explaining what makes each example exemplary
4. **Follow Structure**: Use the established directory structure and naming conventions

## Organizations Represented

- **Cloudflare**: Infrastructure runtime and developer tooling
- **Microsoft**: AI systems and enterprise tooling
- **PyTorch**: Machine learning infrastructure
- **LangChain**: AI application frameworks
- **Sentry**: Error tracking and monitoring
- **Ethereum Foundation**: Blockchain infrastructure
- **Mattermost**: Enterprise collaboration

## Search GitHub

To find more high-quality examples:

```bash
# Search for claude.md files in popular repositories
filename:claude.md stars:>1000

# Search within specific organizations
filename:claude.md org:microsoft
filename:claude.md org:cloudflare
filename:claude.md org:pytorch
```

## License

This collection is provided under MIT License. Original `claude.md` files retain their respective licenses from source repositories.
