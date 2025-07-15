# Curation Criteria for CLAUDE.md Examples

This document defines the standards and rubric used to evaluate `claude.md` files for inclusion in the awesome-claude-md collection.

## Overview

We curate examples that demonstrate **industry best practices** for onboarding AI assistants to complex codebases. Each example should provide concrete, learnable patterns that developers can apply to their own projects.

## Evaluation Rubric

### ⭐ Essential Criteria (Must Have)

All examples must meet these baseline requirements:

| Criterion | Requirements | Examples |
|-----------|-------------|----------|
| **Public Availability** | Publicly accessible repository with permissive license | MIT, Apache 2.0, BSD |
| **Industry Recognition** | From established organizations or 100+ GitHub stars | Microsoft, Cloudflare, 500+ stars |
| **AI-Friendly Structure** | Clear sections, consistent formatting, actionable content | Headers, bullet points, code blocks |
| **Production Usage** | Actively maintained project used in real environments | Recent commits, issues, releases |

### 🏆 Excellence Indicators (Scoring 1-5 each)

Rate each example on these dimensions:

#### 1. **Onboarding Clarity** (1-5)
- **5 (Exceptional)**: Complete setup guide, common workflows, troubleshooting
- **4 (Excellent)**: Clear setup and basic workflows documented
- **3 (Good)**: Basic setup instructions provided
- **2 (Fair)**: Minimal setup guidance
- **1 (Poor)**: No clear onboarding path

#### 2. **Architecture Communication** (1-5)
- **5 (Exceptional)**: Visual diagrams, component relationships, data flow
- **4 (Excellent)**: Clear component overview with relationships
- **3 (Good)**: Basic architecture description
- **2 (Fair)**: Some structural information
- **1 (Poor)**: No architectural context

#### 3. **Development Workflow** (1-5)
- **5 (Exceptional)**: Comprehensive commands, testing, debugging, deployment
- **4 (Excellent)**: Complete build/test/dev commands
- **3 (Good)**: Basic development commands
- **2 (Fair)**: Some workflow guidance
- **1 (Poor)**: No workflow information

#### 4. **AI Context & Instructions** (1-5)
- **5 (Exceptional)**: Specific AI guidance, examples, constraints, best practices
- **4 (Excellent)**: Clear AI instructions with context
- **3 (Good)**: Some AI-specific guidance
- **2 (Fair)**: Basic AI instructions
- **1 (Poor)**: Generic or no AI guidance

#### 5. **Technical Depth** (1-5)
- **5 (Exceptional)**: Advanced patterns, edge cases, performance considerations
- **4 (Excellent)**: Good technical detail with specific examples
- **3 (Good)**: Adequate technical information
- **2 (Fair)**: Basic technical coverage
- **1 (Poor)**: Superficial technical content

## Scoring & Selection

### Acceptance Thresholds
- **Essential Criteria**: Must meet ALL requirements
- **Excellence Score**: Minimum 15/25 points (average 3.0)
- **Standout Examples**: 20+ points qualify for "Top Picks"

### Scoring Examples

#### ⭐ **Exceptional (20-25 points)**
Examples like [Basic Memory](scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md):
- Complete MCP integration guide (5/5 Onboarding)
- Detailed architecture with diagrams (5/5 Architecture)  
- Full development workflow (5/5 Workflow)
- AI-specific collaboration patterns (5/5 AI Context)
- Advanced technical patterns (4/5 Technical)

#### ✅ **Excellent (15-19 points)**
Examples like [Cloudflare Workers SDK](scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md):
- Clear monorepo setup (4/5 Onboarding)
- Well-documented architecture (4/5 Architecture)
- Comprehensive commands (5/5 Workflow)
- Good AI guidance (3/5 AI Context)
- Solid technical depth (4/5 Technical)

## Category-Specific Considerations

### Complex Projects
- Multi-service coordination patterns
- Scalability and deployment considerations
- Inter-service communication documentation

### Libraries & Frameworks
- API design and usage patterns
- Integration examples and best practices
- Testing and validation strategies

### Developer Tooling
- Command-line interface documentation
- Configuration and customization options
- Integration with development workflows

### Getting Started
- Comprehensive onboarding sequences
- Common pitfalls and troubleshooting
- Progressive complexity introduction

### Infrastructure Projects
- Deployment and operational guidance
- Performance and monitoring considerations
- Production environment setup

## Quality Assurance Checklist

Before adding any example, verify:

- [ ] **License Compatibility**: Original repository uses permissive license
- [ ] **Attribution Complete**: Source links, license info, proper credit included
- [ ] **No Direct Copying**: We link to originals, never copy content
- [ ] **Educational Value**: Clear, specific techniques that others can learn
- [ ] **Maintenance Status**: Project actively maintained (commits within 6 months)
- [ ] **Community Value**: Demonstrates patterns applicable beyond the specific project

## Rejection Criteria

Examples will be rejected if they:

- Copy proprietary or restrictively licensed content
- Provide only generic advice without specific patterns
- Come from inactive or deprecated projects
- Lack sufficient technical depth or context
- Don't demonstrate clear AI assistant benefits

## Review Process

1. **Initial Screening**: Check essential criteria and licensing
2. **Technical Review**: Score on 5 excellence dimensions  
3. **Community Value**: Assess broader applicability and learning potential
4. **Documentation Quality**: Ensure analysis meets our standards
5. **Final Decision**: Accept (15+ points), feature (20+ points), or reject

## Examples by Score Range

### 🏆 Top Picks (20-25 points)
- [Basic Memory](scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md) - 23/25
- [CYRUP AI Kargo](scenarios/developer-tooling/cyrup-ai_kargo/analysis.md) - 22/25
- [Overreacted.io](scenarios/complex-projects/gaearon_overreacted.io/analysis.md) - 21/25

### ⭐ Excellent (18-19 points)  
- [Cloudflare Workers SDK](scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md) - 19/25
- [Anthropic Quickstarts](scenarios/getting-started/anthropics_anthropic-quickstarts/analysis.md) - 18/25

### ✅ Good (15-17 points)
- [Microsoft Semantic Workbench](scenarios/complex-projects/microsoft_semanticworkbench/analysis.md) - 16/25
- [PyTorch tlparse](scenarios/developer-tooling/pytorch_tlparse/analysis.md) - 15/25

---

**Note**: This rubric ensures consistency and quality while remaining flexible enough to accommodate diverse project types and innovative approaches to AI assistant onboarding.