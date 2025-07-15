# Contributing to Awesome Claude.md

Thank you for your interest in contributing to the awesome-claude-md collection! This guide will help you understand how to suggest new examples and contribute to the project.

## Quick Start

1. **Review our [Curation Criteria](CRITERIA.md)** to understand what makes an example "awesome"
2. **Check existing examples** to avoid duplicates and understand our standards
3. **Open an issue** using our submission template to propose a new example
4. **Follow the evaluation process** outlined below

## Submission Process

### 1. Find a Quality Example

Look for CLAUDE.md files that demonstrate exceptional patterns:

```bash
# Search GitHub for examples
filename:claude.md stars:>100
filename:CLAUDE.md org:microsoft
filename:claude.md "## Architecture"
```

**Pre-submission checklist:**
- [ ] Repository has 100+ stars OR is from a recognized organization
- [ ] CLAUDE.md file is comprehensive and well-structured
- [ ] Repository is actively maintained (commits within 12 months)
- [ ] Project is used in production environments
- [ ] No similar example already exists in our collection

### 2. Evaluate Against Criteria

Use our [detailed scoring rubric](CRITERIA.md#evaluation-rubric) to assess:

- **Repository Quality & Recognition** (25 points)
- **CLAUDE.md Content Quality** (30 points)
- **AI Assistant Effectiveness** (25 points)
- **Educational Value** (20 points)

**Evaluation tools:**
- Use our [evaluation template](.github/EVALUATION_TEMPLATE.md) for systematic assessment
- Refer to the [complete criteria](CRITERIA.md) for detailed scoring guidelines

**Minimum thresholds:**
- Examples need 55+ points total to be considered
- Strong candidates should score 70+ points
- Exceptional examples (85+ points) are prioritized

### 3. Submit Your Proposal

Open a new issue using the "New Example Submission" template. Include:

- Link to the repository and original CLAUDE.md file
- Category placement (complex-projects, developer-tooling, etc.)
- Your evaluation score with brief justification
- 2-3 key techniques the example demonstrates
- Why it adds unique value to our collection

### 4. Community Review

Your submission will be reviewed by maintainers and community members:

- Initial screening for basic requirements
- Detailed evaluation using our scoring rubric
- Community feedback and discussion
- Final decision with documented rationale

## Creating Analysis Files

If your submission is accepted, you'll be invited to create the analysis file:

### Directory Structure
```
scenarios/[category]/[owner]_[repo]/
└── analysis.md
```

### Analysis Template
```markdown
# Analysis: [Project Name]

**Category**: [Category Name]
**Repository**: [GitHub URL]
**CLAUDE.md**: [Direct link to original file]
**License**: [License type]
**Why it's exemplary**: [Brief explanation]

## Key Features That Make This Exemplary

### 1. **[Feature Name]**
- **[Aspect]**: [Description]
- **[Examples]**: [Specific examples]

## Specific Techniques to Learn

### [Technique Name]
```[language]
[Code example]
```
[Explanation of why this is effective]

## Key Takeaways

1. **[Takeaway 1]**: [Actionable insight]
2. **[Takeaway 2]**: [Practical application]
3. **[Takeaway 3]**: [Best practice learned]
```

### Writing Guidelines

- **Focus on specific, learnable patterns** rather than general praise
- **Include concrete examples** with code snippets where relevant
- **Explain why techniques are effective** for AI assistant onboarding
- **Highlight unique approaches** that differentiate this example
- **Keep educational value paramount** - what will developers learn?

## Categories and Placement

### Category Definitions

- **complex-projects/**: Multi-service applications with sophisticated architectures
- **libraries-frameworks/**: Reusable components, SDKs, and framework implementations
- **developer-tooling/**: CLI tools, build systems, and developer productivity solutions
- **infrastructure-projects/**: Large-scale systems and runtime environments
- **getting-started/**: Projects focused on developer onboarding experiences
- **project-handoffs/**: Documentation for project transitions and current state

### Placement Guidelines

Choose the category that best represents the **primary value** of the CLAUDE.md file:
- What is the main thing developers will learn from this example?
- What problem does this approach solve most effectively?
- Which community would benefit most from this pattern?

## Quality Standards

### Ethical Requirements

- **Never copy** CLAUDE.md files directly into this repository
- **Always link** to original source repositories with proper attribution
- **Respect licensing** - only reference files under permissive licenses
- **Credit original authors** in analysis files and documentation

### Technical Standards

- **Accuracy**: All technical information must be verified and correct
- **Currency**: Examples should reflect current best practices
- **Clarity**: Analysis must be clear and accessible to developers
- **Completeness**: Cover all significant techniques demonstrated

### Editorial Standards

- Use consistent formatting and style across analysis files
- Follow established naming conventions for directories and files
- Include all required metadata (license, source links, etc.)
- Proofread for grammar, spelling, and technical accuracy

## Maintenance and Updates

### Monitoring Changes

We monitor source repositories for significant changes:
- Major updates to CLAUDE.md files may require analysis updates
- Deprecated or archived repositories may be removed
- Security issues or licensing changes are addressed promptly

### Community Updates

Contributors can help maintain quality by:
- Reporting broken links or outdated information
- Suggesting improvements to existing analysis files
- Identifying new patterns in evolving examples
- Helping with periodic reviews of criteria and processes

## Recognition

Contributors are recognized in multiple ways:
- Attribution in analysis files they create
- Mention in repository contributors list
- Special recognition for exceptional contributions
- Invitation to help with repository maintenance

## Getting Help

### Before Contributing

- Read through existing analysis files to understand our style
- Review the [curation criteria](CRITERIA.md) thoroughly
- Browse issues to see what types of examples we're looking for

### During Contribution

- Ask questions in your submission issue for clarification
- Request feedback on draft analysis files before finalizing
- Collaborate with maintainers on category placement decisions

### Community Resources

- **GitHub Issues**: For questions, suggestions, and discussions
- **Discussions**: For broader conversations about direction and standards
- **Email**: Contact maintainers for sensitive issues or private feedback

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and constructive in all interactions
- Focus on the technical merits of contributions
- Help create a learning-friendly environment
- Respect the time and effort of volunteers

Report any issues with community behavior to the maintainers.

---

Thank you for helping make awesome-claude-md a valuable resource for the developer community!