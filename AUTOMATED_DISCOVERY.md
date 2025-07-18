# Automated Discovery System

This repository includes an automated system for discovering new CLAUDE.md files across GitHub, helping keep the collection up-to-date without missing valuable examples.

## How It Works

### 🔄 Scheduled Discovery
- **Frequency**: Runs automatically every Monday at 9 AM UTC
- **Trigger**: GitHub Action workflow (`.github/workflows/discover-claude-files.yml`)
- **Manual Execution**: Can be triggered manually via GitHub Actions interface

### 🔍 Search Process

The discovery system searches GitHub for repositories containing:
- `claude.md` (lowercase)
- `CLAUDE.md` (uppercase) 
- `Claude.md` (title case)

### 📊 Quality Evaluation

Each candidate repository is scored against multiple criteria:

#### ⭐ Repository Metrics
- **Star Count**: Higher stars indicate community recognition
  - 1000+ stars: 3 points (preferred threshold)
  - 500+ stars: 2 points
  - 50+ stars: 1 point (minimum threshold)
- **Recent Activity**: Active maintenance is crucial
  - Updated within 30 days: 2 points
  - Updated within 90 days: 1 point

#### 📄 Content Quality
- **File Size**: Substantial CLAUDE.md files (500+ bytes): 1 point
- **Content Richness**: Presence of key sections: 1-2 points
  - Architecture documentation
  - Development commands
  - Setup instructions
  - Testing information
  - Deployment guidance
  - Workflow descriptions
  - Contributing guidelines

#### 🏢 Organization Recognition
- **Notable Organizations**: Extra weight for established entities: 2 points
  - Microsoft, Google, Cloudflare, Anthropic, etc.
  - PyTorch, LangChain, Ethereum Foundation, etc.

### 🎯 Automatic Categorization

The system suggests appropriate categories based on content analysis:
- **infrastructure-projects**: Runtime environments, platforms, servers
- **complex-projects**: Applications, enterprise systems, microservices
- **developer-tooling**: CLI tools, build systems, generators
- **libraries-frameworks**: SDKs, APIs, integrations
- **getting-started**: Tutorials, examples, starter templates

### 📋 Community Review Process

When candidates are found, the system:

1. **Creates GitHub Issue**: Automatically opens an issue with:
   - Ranked list of candidates by quality score
   - Detailed evaluation for each repository
   - Direct links to CLAUDE.md files
   - Suggested categories
   - Quality indicators and reasons

2. **Community Assessment**: Maintainers and contributors review:
   - Quality of CLAUDE.md content
   - Uniqueness of patterns demonstrated
   - Educational value for the community
   - Maintenance status of the repository

3. **Manual Addition**: Approved candidates are manually added:
   - Create analysis files in appropriate categories
   - Update main README.md table of contents
   - Follow established quality standards

## 🛠️ Technical Implementation

### GitHub Action Workflow
```yaml
# .github/workflows/discover-claude-files.yml
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Mondays
  workflow_dispatch:      # Manual trigger
```

### Python Discovery Script
```bash
# scripts/discover_claude_files.py
python scripts/discover_claude_files.py
```

**Dependencies**: `requests`, `PyGithub`

**Environment**: Requires `GITHUB_TOKEN` for API access

### Duplicate Prevention
- Scans existing `scenarios/` directory structure
- Extracts repository names from directory naming convention
- Skips repositories already in the collection

## 📈 Quality Thresholds

### Minimum Requirements
- **Stars**: 50+ (ensures basic community validation)
- **File Size**: 500+ bytes (substantial content)
- **Score**: 3+ points (combined quality indicators)
- **Status**: Not archived, not a fork

### Discovery Limits
- **Search Results**: 100 repositories per query (GitHub API limit)
- **Rate Limiting**: 2-second delays between API calls
- **Issue Size**: Top 10 candidates featured prominently

## 🔧 Maintenance

### Manual Triggers
For testing or immediate discovery:
1. Go to repository Actions tab
2. Select "Discover New CLAUDE.md Files" workflow
3. Click "Run workflow" button

### Issue Management
- Issues created with labels: `automation`, `discovery`, `review-needed`
- Close issues after reviewing and adding approved candidates
- Archive discovery reports for historical tracking

### Monitoring
- Check workflow runs for errors
- Review API rate limit usage
- Monitor issue creation and closure patterns

## 🚀 Future Enhancements

Potential improvements to the discovery system:
- **Trending Analysis**: Weight recently starred repositories higher
- **Language Detection**: Better categorization based on primary language
- **Content Parsing**: More sophisticated CLAUDE.md content analysis
- **PR Automation**: Auto-create pull requests for high-confidence candidates
- **Notification System**: Alert maintainers of high-priority discoveries

## 🤝 Contributing

To improve the discovery system:
1. **Adjust Criteria**: Modify scoring logic in `scripts/discover_claude_files.py`
2. **Enhance Search**: Add new search queries or filters
3. **Improve Categorization**: Update category suggestion algorithm
4. **Test Changes**: Use manual workflow triggers for validation

---

*The automated discovery system ensures the awesome-claude-md collection stays current while maintaining high quality standards through community review.*