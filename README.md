# Awesome Claude.md

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Examples: 25+](https://img.shields.io/badge/Examples-25%2B-blue.svg)](#-all-categories)
[![Auto Discovery](https://img.shields.io/badge/Auto-Discovery-enabled-green.svg)](.github/workflows/discover-claude-files.yml)

A curated collection of high-quality `claude.md` files from leading open-source projects. These examples demonstrate industry best practices for onboarding AI assistants to complex codebases.

> **🚀 Quick Start**: New here? Jump to [Top Picks](#-top-picks) or browse by [Technology](#-browse-by-technology) | [Use Case](#-browse-by-use-case)  
> **📖 Learn More**: [Curation Criteria](CRITERIA.md) | [Best Practices](BEST_PRACTICES.md) | [Contributing Guide](CONTRIBUTING.md)

## 📋 Table of Contents

- [🎯 Top Picks](#-top-picks) - Start here for the best examples
- [🔍 Browse by Technology](#-browse-by-technology) - Find examples by tech stack
- [🎨 Browse by Use Case](#-browse-by-use-case) - Find examples by purpose
- [📂 All Categories](#-all-categories) - Complete categorized list
- [🏆 Quality Standards](#-quality-standards) - Our selection criteria
- [📚 Resources](#-resources) - Documentation and guides
- [🤝 Contributing](#-contributing) - How to add examples
- [🔎 Search GitHub](#-search-github) - Find more examples

## 🎯 Top Picks

**Start with these exceptional examples** - hand-picked for learning effective `claude.md` patterns:

### 🥇 **Essential (Must Read)**
| Example | Why It's Great | Tech Stack |
|---------|---------------|------------|
| **[Basic Memory](scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md)** | Cutting-edge MCP integration & AI collaboration | Python, FastAPI, SQLAlchemy |
| **[CYRUP AI Kargo](scenarios/developer-tooling/cyrup-ai_kargo/analysis.md)** | State machine workflows & research methodology | Rust, MCP Tools |
| **[Overreacted.io](scenarios/complex-projects/gaearon_overreacted.io/analysis.md)** | Technical depth with personality | Next.js, React, MDX |

### 🥈 **Advanced Patterns**
| Example | Why It's Great | Tech Stack |
|---------|---------------|------------|
| **[Cloudflare Workers SDK](scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md)** | Monorepo & testing excellence | TypeScript, Monorepo |
| **[Anthropic Quickstarts](scenarios/getting-started/anthropics_anthropic-quickstarts/analysis.md)** | Multi-project organization | Python, TypeScript, React |

## 🔍 Browse by Technology

<details>
<summary><strong>🟦 TypeScript/JavaScript</strong></summary>

- **[Overreacted.io](scenarios/complex-projects/gaearon_overreacted.io/analysis.md)** - Next.js with MDX
- **[Cloudflare Workers SDK](scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md)** - Monorepo patterns
- **[Claude Crew](scenarios/developer-tooling/d-kimuson_claude-crew/analysis.md)** - Strict TypeScript standards
- **[Anthropic Quickstarts](scenarios/getting-started/anthropics_anthropic-quickstarts/analysis.md)** - Multi-project setup

</details>

<details>
<summary><strong>🟧 Python</strong></summary>

- **[Basic Memory](scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md)** - MCP integration
- **[PyTorch tlparse](scenarios/developer-tooling/pytorch_tlparse/analysis.md)** - Dual-language (Rust/Python)
- **[Anthropic Quickstarts](scenarios/getting-started/anthropics_anthropic-quickstarts/analysis.md)** - Computer-use demo

</details>

<details>
<summary><strong>🟫 Rust</strong></summary>

- **[CYRUP AI Kargo](scenarios/developer-tooling/cyrup-ai_kargo/analysis.md)** - State machine workflows
- **[PyTorch tlparse](scenarios/developer-tooling/pytorch_tlparse/analysis.md)** - Performance optimization

</details>

<details>
<summary><strong>🟪 Other Languages</strong></summary>

- **[Kent Beck's BPlusTree3](scenarios/project-handoffs/KentBeck_BPlusTree3/analysis.md)** - TDD methodology
- **[Cloudflare workerd](scenarios/infrastructure-projects/cloudflare_workerd/analysis.md)** - C++/WebAssembly runtime

</details>

## 🎨 Browse by Use Case

<details>
<summary><strong>🏗️ Monorepo & Build Systems</strong></summary>

- **[Cloudflare Workers SDK](scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md)** - Advanced monorepo patterns
- **[Lerna](scenarios/developer-tooling/lerna_lerna/analysis.md)** - Multi-package management

</details>

<details>
<summary><strong>🤖 AI & Machine Learning</strong></summary>

- **[Basic Memory](scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md)** - AI collaboration workflows
- **[Microsoft Semantic Workbench](scenarios/complex-projects/microsoft_semanticworkbench/analysis.md)** - AI assistant platform

</details>

<details>
<summary><strong>🧪 Testing & Quality</strong></summary>

- **[Kent Beck's BPlusTree3](scenarios/project-handoffs/KentBeck_BPlusTree3/analysis.md)** - TDD methodology
- **[Claude Crew](scenarios/developer-tooling/d-kimuson_claude-crew/analysis.md)** - Strict TypeScript standards

</details>

<details>
<summary><strong>🚀 Getting Started</strong></summary>

- **[Anthropic Quickstarts](scenarios/getting-started/anthropics_anthropic-quickstarts/analysis.md)** - Multi-project documentation
- **[Ethereum.org Website](scenarios/getting-started/ethereum_ethereum-org-website/analysis.md)** - Community-driven development

</details>

## 📂 All Categories

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

- **[Sentry](scenarios/complex-projects/getsentry_sentry/analysis.md)** - Error tracking and performance monitoring (40,000+ stars)
  - Microservices architecture
  - Real-time data processing
  - Enterprise deployment patterns

- **[TimeWarp Architecture](scenarios/complex-projects/TimeWarpEngineering_timewarp-architecture/analysis.md)** - .NET distributed application framework (100+ stars)
  - Event sourcing and CQRS patterns
  - Distributed system design
  - Modern .NET practices

- **[Platformatic](scenarios/complex-projects/platformatic_platformatic/analysis.md)** - Node.js application platform (1,000+ stars)
  - Multi-service coordination
  - API gateway patterns
  - Development environment setup

- **[Webhook Broker](scenarios/complex-projects/newscred_webhook-broker/analysis.md)** - High-throughput webhook delivery system (200+ stars)
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

- **[Lerna](scenarios/developer-tooling/lerna_lerna/analysis.md)** - Monorepo management tool (35,000+ stars)
  - Multi-package workflows
  - Release management
  - CI/CD integration

- **[Kubb](scenarios/developer-tooling/kubb-labs_kubb/analysis.md)** - API toolkit for code generation (2,000+ stars)
  - Plugin architecture
  - OpenAPI code generation
  - TypeScript integration

- **[mypy-boto3-builder](scenarios/developer-tooling/youtype_mypy-boto3-builder/analysis.md)** - Type generation for AWS SDK (2,000+ stars)
  - Sophisticated type generation
  - Multi-package publishing
  - Documentation automation

- **[HWP](scenarios/developer-tooling/mcollina_hwp/analysis.md)** - High-performance web platform (by Node.js TSC member)
  - Expert-level Node.js patterns
  - Performance optimization
  - Production deployment

- **[Kotlinter Gradle](scenarios/developer-tooling/jeremymailen_kotlinter-gradle/analysis.md)** - Kotlin code formatting plugin (500+ stars)
  - Gradle plugin development
  - Code quality automation
  - CI/CD integration

### 📚 Libraries & Frameworks

Reusable components, SDKs, and framework implementations.

- **[LangChain Redis](scenarios/libraries-frameworks/langchain-ai_langchain-redis/analysis.md)** - Redis integration for LangChain (34 stars)
  - Comprehensive testing architecture
  - Sophisticated configuration system
  - Production-ready workflows

- **[Composio](scenarios/libraries-frameworks/ComposioHQ_composio/analysis.md)** - AI agent integration platform (10,000+ stars)
  - Multi-platform SDK architecture
  - Comprehensive API coverage
  - Integration patterns

- **[Agentic](scenarios/libraries-frameworks/transitive-bullshit_agentic/analysis.md)** - LLM tool integration framework (2,000+ stars)
  - Innovative tool abstractions
  - Multi-model support
  - Type-safe implementations

- **[DataFog Python](scenarios/libraries-frameworks/DataFog_datafog-python/analysis.md)** - Data privacy and masking library (500+ stars)
  - Privacy-focused patterns
  - Data transformation pipelines
  - Compliance considerations

- **[GenSX](scenarios/libraries-frameworks/gensx-inc_gensx/analysis.md)** - Code generation framework (200+ stars)
  - Template-based generation
  - Multi-language support
  - Extensible architecture

### 🚀 Getting Started

Projects focused on developer onboarding and initial setup experiences.

- **[Ethereum.org Website](scenarios/getting-started/ethereum_ethereum-org-website/analysis.md)** - Official Ethereum community website (5,000+ stars)
  - Community-driven development
  - Multi-language support
  - Documentation workflows

### 🔄 Project Handoffs

Documentation focused on project state, blocking issues, and transition planning.

- **[Mattermost Test Management](scenarios/project-handoffs/mattermost_mattermost-test-management/analysis.md)** - Enterprise test management system
  - Current project state
  - Blocking issues documentation
  - Transition planning

## 🏆 Quality Standards

All examples in this collection meet rigorous criteria designed to ensure educational value and industry relevance.

### Essential Requirements
- **Industry Recognition**: 100+ GitHub stars OR established organization backing
- **Production Usage**: Actively maintained and used in production environments  
- **Comprehensive Documentation**: Detailed architecture, setup, and workflow information
- **Best Practices**: Demonstrate advanced patterns and techniques
- **AI-Friendly**: Structured to maximize AI assistant effectiveness

### Excellence Scoring (25-point scale)
Our [detailed rubric](CRITERIA.md) evaluates examples across 5 dimensions:
- **Onboarding Clarity** (1-5): Setup guides, workflows, troubleshooting
- **Architecture Communication** (1-5): Component relationships, data flow
- **Development Workflow** (1-5): Commands, testing, debugging  
- **AI Context & Instructions** (1-5): Specific AI guidance and constraints
- **Technical Depth** (1-5): Advanced patterns, edge cases, performance

**Acceptance Threshold**: 15+ points | **Top Picks**: 20+ points

📊 **[View Full Criteria](CRITERIA.md)** | 📈 **[See Scoring Examples](CRITERIA.md#examples-by-score-range)**

## 📚 Resources

### For Contributors
- **[📋 Contributing Guide](CONTRIBUTING.md)** - Step-by-step process for adding examples
- **[📝 Analysis Template](ANALYSIS_TEMPLATE.md)** - Standardized template for consistent analysis
- **[🔍 Curation Criteria](CRITERIA.md)** - Detailed evaluation rubric and quality standards

### For Learning
- **[📖 Best Practices Summary](BEST_PRACTICES.md)** - Top patterns and techniques across all examples
- **[🎯 Top Picks Analysis](#-top-picks)** - Deep dive into our highest-rated examples
- **[🚀 Implementation Roadmap](BEST_PRACTICES.md#-implementation-roadmap)** - How to improve your own claude.md files

### Community Tools
- **[🤖 Automated Discovery](.github/workflows/discover-claude-files.yml)** - Weekly search for new quality examples
- **[📝 Issue Templates](.github/ISSUE_TEMPLATE/)** - Streamlined contribution and feedback process

## 🤝 Contributing

We welcome high-quality contributions that help the community learn effective `claude.md` patterns!

### Quick Start
1. **[📝 Suggest New Example](https://github.com/josix/awesome-claude-md/issues/new?template=suggest-new-example.yml)** - Found a great claude.md file?
2. **[✨ Improve Analysis](https://github.com/josix/awesome-claude-md/issues/new?template=improve-analysis.yml)** - Help enhance existing analyses
3. **[🐛 Report Problem](https://github.com/josix/awesome-claude-md/issues/new?template=report-problem.yml)** - Broken links or incorrect information?

### Detailed Process
📋 **[Complete Contributing Guide](CONTRIBUTING.md)** includes:
- Search strategies for finding quality examples
- Step-by-step evaluation process using our rubric
- Template for creating analysis files
- Requirements and review process

### Quality Standards
- Minimum 15/25 points on our [evaluation rubric](CRITERIA.md)
- Focus on examples with 100+ stars or established organizations
- Comprehensive analysis following our [template](ANALYSIS_TEMPLATE.md)
- Proper attribution and licensing compliance

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
