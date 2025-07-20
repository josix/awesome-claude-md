# Evaluate Quality of New Examples

Perform rigorous quality analysis of newly discovered CLAUDE.md examples before adding them to the awesome-claude-md collection.

## Task

Ultra-analyze each new example against the repository's strict quality criteria using the 100-point scoring system. **Only examples scoring 60+ points qualify for inclusion.**

## Scoring Framework (100 Points Total)

### Primary Criteria (70% weight)

#### 1. Content Depth (25 points)
- **Excellent (20-25)**: Comprehensive architecture, workflows, detailed context
- **Good (15-19)**: Solid documentation with clear patterns
- **Fair (10-14)**: Basic documentation, some detail missing
- **Poor (0-9)**: Minimal or superficial content

#### 2. Educational Value (25 points)
- **Excellent (20-25)**: Demonstrates unique patterns, teaches best practices
- **Good (15-19)**: Shows useful patterns, some learning value
- **Fair (10-14)**: Limited educational content
- **Poor (0-9)**: Little to no educational value

#### 3. AI Effectiveness (20 points)
- **Excellent (16-20)**: Perfectly structured for AI assistant consumption
- **Good (12-15)**: Well-organized for AI understanding
- **Fair (8-11)**: Adequate AI assistant guidance
- **Poor (0-7)**: Poor structure for AI consumption

### Secondary Criteria (30% weight)

#### 4. Project Maturity (15 points)
- **Excellent (12-15)**: Active maintenance, production usage, regular commits
- **Good (9-11)**: Stable project with some activity
- **Fair (6-8)**: Limited activity or early stage
- **Poor (0-5)**: Abandoned or minimal activity

#### 5. Community Recognition (15 points)
- **Industry validation**: GitHub stars (maximum 10% of total score)
- **Expert endorsement**: Created by recognized practitioners
- **Community engagement**: Issues, PRs, discussions
- **Documentation quality**: README, contributing guidelines

## Evaluation Process

### Step 1: Initial Assessment
1. **Read the CLAUDE.md file thoroughly**
2. **Examine the repository structure and documentation**
3. **Check commit history and maintenance status**
4. **Review community engagement metrics**

### Step 2: Detailed Scoring
For each example, score against all 5 criteria and calculate total:

```
Example: [Repository Name]
- Content Depth: X/25 points
- Educational Value: X/25 points
- AI Effectiveness: X/20 points
- Project Maturity: X/15 points
- Community Recognition: X/15 points
TOTAL: X/100 points
```

### Step 3: Quality Decision
- **90-100 points**: Exceptional quality → Top Picks "Essential"
- **70-89 points**: High quality → Top Picks "Advanced Patterns"
- **60-69 points**: Meets threshold → Include in collection
- **Below 60 points**: **REJECT** → Does not meet standards

## Red Flags (Automatic Rejection)

- ❌ **Minimal content**: CLAUDE.md under 20 lines with no depth
- ❌ **Abandoned projects**: No commits in 12+ months
- ❌ **Poor documentation**: No README or setup instructions
- ❌ **Experimental/toy projects**: Not production-ready
- ❌ **Duplicate patterns**: Doesn't add unique value

## Common Pitfalls to Avoid

1. **Star-count bias**: Don't let popularity override content quality
2. **Authority bias**: Even expert authors must meet content standards
3. **Quantity over quality**: Better to reject than lower standards
4. **Recency bias**: Newer doesn't automatically mean better

## Analysis Template

```markdown
## Quality Analysis: [Repository Name]

### Repository Details
- **Owner**: [username/organization]
- **Stars**: [count]
- **Last Commit**: [date]
- **License**: [type]
- **CLAUDE.md Link**: [direct link]

### Scoring Breakdown
1. **Content Depth (X/25)**:
   - [Detailed assessment of documentation comprehensiveness]

2. **Educational Value (X/25)**:
   - [Analysis of unique patterns and learning opportunities]

3. **AI Effectiveness (X/20)**:
   - [Evaluation of AI assistant usability]

4. **Project Maturity (X/15)**:
   - [Assessment of maintenance and production readiness]

5. **Community Recognition (X/15)**:
   - [Review of industry validation and engagement]

### Final Score: X/100

### Decision: [ACCEPT/REJECT]
**Rationale**: [Brief explanation of decision]

### Category Assignment (if accepted):
- **Primary Category**: [complex-projects/developer-tooling/etc.]
- **Technology**: [Python/TypeScript/etc.]
- **Use Case**: [AI Development/Getting Started/etc.]
```

## Output Requirements

For each batch of examples evaluated:

1. **Provide individual scores** for each example
2. **Show decision rationale** for accepts/rejects
3. **Rank accepted examples** by quality score
4. **Suggest category assignments** for accepted examples
5. **Identify any that qualify for Top Picks**

Remember: **Quality over quantity always**. It's better to maintain high standards than dilute the collection with mediocre examples.
