# Contributing to Awesome Claude.md

Thank you for your interest in contributing to this curated collection of high-quality `claude.md` files! This guide will help you add valuable examples while maintaining our quality standards.

## 🚀 Quick Start

1. **Found a great `claude.md` file?** [Submit a suggestion using our issue template](#suggesting-new-examples)
2. **Want to improve an existing analysis?** [Use our improvement template](#improving-existing-analyses)
3. **Found a bug or issue?** [Report it using our bug template](#reporting-issues)

## 📋 Types of Contributions

### 🎯 Suggesting New Examples

The most valuable contributions are high-quality `claude.md` files from established projects. Before suggesting:

**Quality Criteria:**
- From repositories with **1,000+ stars** (preferred) or recognized organizations
- Actively maintained and used in production
- Demonstrates advanced patterns or techniques
- Well-structured to maximize AI assistant effectiveness

**Search for Examples:**
```bash
# GitHub search patterns
filename:claude.md stars:>1000
filename:CLAUDE.md org:microsoft
filename:claude.md "## Architecture"
```

### 📝 Improving Existing Analyses

Help make our analyses more valuable by:
- Adding missing technical details
- Improving explanations of key patterns
- Updating outdated information
- Enhancing code examples or takeaways

### 🐛 Reporting Issues

Found broken links, typos, or incorrect information? Please report it!

## 🛠️ Step-by-Step Contribution Process

### 1. **Discover and Evaluate**

**Find Examples:**
- Search GitHub using patterns above
- Look for projects in our [target organizations](#target-organizations)
- Check recent repositories from industry leaders

**Evaluate Quality:**
- ✅ Does it demonstrate best practices?
- ✅ Is the documentation comprehensive?
- ✅ Would it help developers learn effective patterns?
- ✅ Is it from a reputable source?

### 2. **Create an Issue First**

Before creating a PR, **always create an issue** using our templates:
- 🆕 [New Example Suggestion](.github/ISSUE_TEMPLATE/new-example.md)
- 📈 [Analysis Improvement](.github/ISSUE_TEMPLATE/improvement.md)
- 🐛 [Bug Report](.github/ISSUE_TEMPLATE/bug-report.md)

This allows maintainers to provide early feedback and avoid duplicate work.

### 3. **Fork and Clone**

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/awesome-claude-md.git
cd awesome-claude-md
```

### 4. **Create Your Branch**

```bash
git checkout -b add-example-project-name
# or
git checkout -b improve-analysis-project-name
```

### 5. **Add Your Contribution**

#### For New Examples:

**A. Create Directory Structure:**
```bash
mkdir -p scenarios/[category]/[owner]_[repo]
```

**Categories:**
- `complex-projects/` - Multi-service projects with detailed architecture
- `libraries-frameworks/` - Core concepts, APIs, and usage patterns
- `developer-tooling/` - CLI tools with commands and configuration
- `project-handoffs/` - Current state with blocking issues and next steps
- `getting-started/` - Development environment setup focused
- `infrastructure-projects/` - Large-scale systems and runtime environments

**B. Create Analysis File:**

Create `scenarios/[category]/[owner]_[repo]/analysis.md` using this template:

```markdown
# Analysis: [Project Name]

**Category**: [Category Name]  
**Repository**: [GitHub Repository URL]  
**Original CLAUDE.md**: [Direct link to the claude.md file]  
**License**: [Repository License] - [Link to License]  
**Why it's exemplary**: [Brief explanation of what makes this special]

## Key Features That Make This Exemplary

### 1. **[Feature Name]**
- **[Aspect]**: [Detailed description]
- **[Implementation]**: [How it's implemented]
- **[Example]**: [Specific code or command examples]

### 2. **[Feature Name]**
- **[Aspect]**: [Detailed description]
- **[Commands/Examples]**: [Specific examples]

## Specific Techniques to Learn

### [Technique Name]
```[language]
[Code example from the original]
```
[Explanation of why this technique is effective]

### [Another Technique]
[Description and examples]

## Key Takeaways

1. **[Takeaway 1]**: [Concrete lesson developers can apply]
2. **[Takeaway 2]**: [Another actionable insight]
3. **[Takeaway 3]**: [Third key learning point]

## Additional Resources

- [Link to project documentation]
- [Link to related blog posts or articles]
- [Link to community discussions]
```

**C. Update README.md:**

Add your example to the appropriate sections:
- Add to the category section
- Include star count if available
- List 2-3 key features
- Link to your analysis file

### 6. **Quality Checklist**

Before submitting, verify:

**Content Quality:**
- [ ] Analysis explains what makes the example exemplary
- [ ] Key takeaways are actionable for developers
- [ ] All links work correctly
- [ ] Proper attribution and licensing information included

**Ethical Guidelines:**
- [ ] **NO copying** of original `claude.md` files into this repository
- [ ] All links point to original sources
- [ ] Proper attribution with source links and license info
- [ ] Respects copyright of publicly available files

**Structure:**
- [ ] Follows directory naming conventions
- [ ] Uses consistent markdown formatting
- [ ] README.md updated appropriately
- [ ] No typos or grammar errors

### 7. **Submit Your Pull Request**

```bash
git add .
git commit -m "Add analysis for [project-name]"
git push origin your-branch-name
```

**PR Description Should Include:**
- Link to the issue you created
- Brief description of the example
- Why it's valuable for the collection
- Any special considerations

## 🎯 Target Organizations

Prioritize examples from these organizations known for quality:

- **Anthropic**: Official AI development best practices
- **Basic Machines**: Knowledge management and AI collaboration  
- **Cloudflare**: Infrastructure runtime and developer tooling
- **CYRUP AI**: Advanced AI development methodologies
- **Microsoft**: AI systems and enterprise tooling
- **PyTorch**: Machine learning infrastructure
- **LangChain**: AI application frameworks
- **Sentry**: Error tracking and monitoring
- **Ethereum Foundation**: Blockchain infrastructure
- **Mattermost**: Enterprise collaboration

## 🚫 What Not to Contribute

- Examples from repositories with < 100 stars (unless exceptional circumstances)
- Outdated or unmaintained projects
- Projects without clear licensing
- Direct copies of `claude.md` files
- Low-quality or incomplete documentation
- Examples that don't demonstrate clear best practices

## 📖 Style Guide

### Markdown Formatting:
- Use consistent heading levels (## for main sections, ### for subsections)
- Include code blocks with language specification
- Use **bold** for emphasis on key terms
- Include links to repositories and documentation

### Analysis Structure:
- Start with clear categorization and attribution
- Focus on what makes the example unique or exemplary
- Include specific, actionable takeaways
- Provide concrete examples and code snippets where relevant

## 🤝 Community Guidelines

- Be respectful in all interactions
- Provide constructive feedback
- Credit original authors appropriately
- Follow ethical guidelines for content usage
- Help newcomers understand our standards

## 📞 Getting Help

- **Questions about contributing?** Create an issue with the "question" label
- **Not sure if an example qualifies?** Create a suggestion issue for discussion
- **Need clarification on guidelines?** Tag maintainers in an issue

## 🏆 Recognition

Contributors who add high-quality examples will be:
- Credited in commit messages
- Mentioned in release notes for significant additions
- Added to a future contributors section

Thank you for helping make this collection a valuable resource for the developer community!