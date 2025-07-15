# Contributing to Awesome Claude.md

Thank you for your interest in contributing to this collection! This guide will help you add high-quality examples and maintain the repository's standards.

## 🚀 Quick Start

1. **Find a Great Example**: Look for `claude.md` files in repositories with 100+ stars
2. **Check Our Standards**: Review [CRITERIA.md](CRITERIA.md) for evaluation rubric
3. **Create Analysis**: Write detailed analysis explaining why it's exemplary
4. **Submit Pull Request**: Follow our template and conventions

## 📋 Step-by-Step Contribution Process

### Step 1: Identify Potential Examples

#### Search Strategies
Use these GitHub search queries to find quality examples:

```bash
# High-quality repositories with claude.md files
filename:claude.md stars:>100
filename:CLAUDE.md stars:>500

# Specific organizations
filename:claude.md org:microsoft
filename:claude.md org:cloudflare  
filename:claude.md org:anthropic

# By programming language
filename:claude.md language:TypeScript
filename:claude.md language:Python
filename:claude.md language:Rust

# By content patterns
"## Architecture" filename:claude.md
"## Development Commands" filename:claude.md
"## Getting Started" filename:claude.md
```

#### Target Organizations
Prioritize examples from these organizations:
- **Anthropic**: Official AI development practices
- **Basic Machines**: Knowledge management and AI collaboration  
- **Cloudflare**: Infrastructure runtime and developer tooling
- **Microsoft**: AI systems and enterprise tooling
- **PyTorch**: Machine learning infrastructure
- **LangChain**: AI application frameworks

### Step 2: Evaluate Against Criteria

Before proceeding, ensure the example meets our [evaluation rubric](CRITERIA.md):

#### ✅ Essential Requirements (All Must Be Met)
- [ ] **Public Repository**: Accessible with permissive license (MIT, Apache 2.0, BSD)
- [ ] **Industry Recognition**: 100+ GitHub stars OR established organization
- [ ] **Active Maintenance**: Commits within last 6 months
- [ ] **Production Usage**: Used in real environments (not just demos)
- [ ] **AI-Friendly Structure**: Clear sections, consistent formatting

#### 🏆 Excellence Score (Target 15+ / 25 points)
Rate 1-5 on each dimension:
- **Onboarding Clarity**: Setup guides, workflows, troubleshooting
- **Architecture Communication**: Component relationships, data flow  
- **Development Workflow**: Commands, testing, debugging
- **AI Context & Instructions**: Specific AI guidance and constraints
- **Technical Depth**: Advanced patterns, edge cases, performance

### Step 3: Determine Category

Choose the most appropriate category:

| Category | Purpose | Examples |
|----------|---------|----------|
| `complex-projects/` | Multi-service applications with sophisticated architectures | Microsoft Semantic Workbench, Sentry |
| `libraries-frameworks/` | Reusable components, SDKs, framework implementations | LangChain Redis, Composio |
| `developer-tooling/` | CLI tools, build systems, developer productivity | Cloudflare Workers SDK, Lerna |
| `infrastructure-projects/` | Large-scale systems and runtime environments | Cloudflare workerd |
| `getting-started/` | Projects focused on developer onboarding | Anthropic Quickstarts, Ethereum.org |
| `project-handoffs/` | Documentation focused on project state and transitions | Mattermost Test Management |

### Step 4: Create Directory Structure

Create the directory following our naming convention:

```bash
scenarios/[category]/[owner]_[repo]/
```

**Examples**:
- `scenarios/complex-projects/microsoft_semanticworkbench/`
- `scenarios/developer-tooling/cloudflare_workers-sdk/`
- `scenarios/libraries-frameworks/langchain-ai_langchain-redis/`

### Step 5: Write Analysis File

Create `analysis.md` in your new directory using this template:

```markdown
# Analysis: [Project Name]

**Category**: [Category Name]  
**Repository**: [GitHub Repository URL]  
**Original CLAUDE.md**: [Direct link to the claude.md file]  
**License**: [Repository License]  
**Stars**: [GitHub star count] ⭐  

## Why This Example is Exemplary

[2-3 sentences explaining what makes this claude.md file outstanding and worth learning from]

## Key Features That Make This Exemplary

### 1. **[Feature Name]**
- **[Specific Aspect]**: [Detailed description with examples]
- **[Implementation Detail]**: [How it's executed]
- **[Learning Value]**: [What developers can learn]

### 2. **[Feature Name]**
- **[Specific Aspect]**: [Detailed description with examples]

[Continue for 3-5 key features]

## Specific Techniques to Learn

### [Technique Name]
```[language]
[Code example or pattern from the original claude.md]
```
[Explanation of why this technique is effective]

### [Another Technique]
[Description and example]

## Notable Patterns and Innovations

- **[Pattern 1]**: [Description and why it's innovative]
- **[Pattern 2]**: [Description and impact]
- **[Pattern 3]**: [Description and applicability]

## Quality Metrics

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Onboarding Clarity | [score] | [brief justification] |
| Architecture Communication | [score] | [brief justification] |
| Development Workflow | [score] | [brief justification] |
| AI Context & Instructions | [score] | [brief justification] |
| Technical Depth | [score] | [brief justification] |
| **Total** | **[total]/25** | |

## Key Takeaways for Your Projects

1. **[Takeaway 1]**: [Specific lesson with actionable advice]
2. **[Takeaway 2]**: [Specific lesson with actionable advice]  
3. **[Takeaway 3]**: [Specific lesson with actionable advice]

## Related Examples

- [Link to similar example 1] - [Brief comparison]
- [Link to similar example 2] - [Brief comparison]

---

**Source**: [Repository Name](repository-url) | **License**: [License] | **Last Updated**: [Date]
```

### Step 6: Update Main README

Add your example to the main `README.md` in the appropriate category section:

```markdown
- **[Project Name](scenarios/[category]/[owner]_[repo]/analysis.md)** - [Brief description] ([star count] stars)
  - [Key feature 1]
  - [Key feature 2]  
  - [Key feature 3]
```

### Step 7: Submit Pull Request

1. **Create descriptive PR title**: `Add [Project Name] - [Brief description of why it's valuable]`

2. **Use this PR template**:
```markdown
## New Example Addition

**Project**: [Project Name]
**Category**: [Category]
**Repository**: [GitHub URL]
**Why it's exemplary**: [Brief explanation]

### Checklist
- [ ] Meets all essential criteria from CRITERIA.md
- [ ] Scored 15+ points on excellence rubric
- [ ] Analysis follows template structure
- [ ] README.md updated with new entry
- [ ] Proper attribution and licensing included
- [ ] No direct copying of original content

### Quality Score: [X]/25
- Onboarding Clarity: [score]/5
- Architecture Communication: [score]/5  
- Development Workflow: [score]/5
- AI Context & Instructions: [score]/5
- Technical Depth: [score]/5

### Key Learning Value
[2-3 sentences about what developers will learn from this example]
```

## 🎯 Quality Standards

### Ethical Guidelines

- **Never copy** `claude.md` files directly into this repository
- **Always link** to the original source repository
- **Include proper attribution** with source links and licensing information
- **Respect copyright** and only reference publicly available files under permissive licenses

### Analysis Quality

Your analysis should:
- **Focus on specifics**: Highlight concrete, learnable patterns over generic advice
- **Explain the "why"**: Don't just describe what they do, explain why it's effective
- **Provide actionable insights**: Include takeaways developers can apply to their own projects
- **Use examples**: Quote specific sections or patterns from the original file
- **Maintain objectivity**: Be honest about both strengths and potential limitations

### Writing Style

- Use clear, concise language
- Include code examples where relevant
- Structure content with headers and bullet points
- Link to relevant documentation and resources
- Keep technical accuracy as the top priority

## 🔍 Review Process

### Automated Checks
- License compatibility verification
- Link validation
- Template structure compliance

### Manual Review
1. **Criteria Verification**: Ensure example meets all essential requirements
2. **Quality Assessment**: Score against excellence rubric  
3. **Educational Value**: Verify analysis provides concrete learning value
4. **Writing Quality**: Check clarity, accuracy, and completeness
5. **Community Fit**: Assess alignment with collection goals

### Review Timeline
- **Initial Response**: Within 48 hours
- **Review Completion**: Within 1 week for straightforward additions
- **Complex Cases**: May require additional discussion for borderline examples

## 🚫 Common Rejection Reasons

- **Insufficient stars/recognition**: Under 100 stars without established organization backing
- **Inactive maintenance**: No commits in 6+ months
- **Poor documentation quality**: Minimal or unclear claude.md content  
- **License restrictions**: Non-permissive licensing that limits reference/analysis
- **Low educational value**: Generic advice without specific, learnable patterns
- **Duplicate coverage**: Similar examples already well-represented

## 💡 Tips for Success

1. **Start with our top picks**: Study examples like [Basic Memory](scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md) to understand our standards

2. **Focus on unique value**: What makes this example different from others we already have?

3. **Be specific in analysis**: Instead of "good documentation," explain "provides Mermaid diagrams showing data flow between services"

4. **Consider the audience**: Write for developers who want to improve their own claude.md files

5. **Test your links**: Ensure all repository and file links work correctly

## 🤝 Getting Help

- **Questions about criteria**: Review [CRITERIA.md](CRITERIA.md) or open an issue
- **Unsure about quality**: Create a draft PR for early feedback
- **Technical issues**: Open an issue with the "help wanted" label
- **General discussion**: Use GitHub Discussions for broader conversations

## 📊 Contribution Recognition

Contributors are recognized in several ways:
- Attribution in analysis files
- Contributor listing in README
- Priority review for future high-quality submissions
- Invitation to help review other contributions

---

**Thank you for helping make this collection a valuable resource for the developer community!**