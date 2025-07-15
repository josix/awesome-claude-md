# License Detection Documentation

This document explains the automated license detection system for the awesome-claude-md repository.

## Overview

The repository includes automated tools to detect and display license information for all referenced repositories, ensuring compliance with open source licenses and informing users about usage rights.

## How It Works

### 1. License Detection Script

The `detect_licenses.py` script automatically:

- Scans all `analysis.md` files in the `scenarios/` directory
- Extracts GitHub repository URLs using multiple patterns:
  - `**Repository**: https://github.com/owner/repo`
  - `**Source**: [owner/repo](https://github.com/owner/repo)`
  - Any other `https://github.com/owner/repo` URLs in the content
- Falls back to inferring repository from directory structure (`owner_repo` format)
- Uses the GitHub API to fetch license information
- Updates analysis files with license information if missing

### 2. GitHub Actions Workflow

The `.github/workflows/update-licenses.yml` workflow:

- Runs weekly on Mondays
- Can be triggered manually from the GitHub Actions tab
- Uses the repository's `GITHUB_TOKEN` for API access
- Automatically commits and pushes license updates

## Usage

### Manual License Detection

Run the script locally to check license information:

```bash
# Check licenses without updating files
python detect_licenses.py --output license_results.json

# Update analysis files with license information
python detect_licenses.py --update

# Specify custom scenarios directory
python detect_licenses.py --scenarios-dir path/to/scenarios --update
```

### Requirements

- Python 3.7+
- `requests` library (`pip install requests`)
- Optional: `GITHUB_TOKEN` environment variable for higher API rate limits

### GitHub Actions

The workflow runs automatically but can also be triggered manually:

1. Go to the Actions tab in the GitHub repository
2. Select "Update License Information" workflow
3. Click "Run workflow"

## Analysis File Format

All analysis files should include license information in the header:

```markdown
# Analysis: Project Name

**Category**: Category Name  
**Repository**: https://github.com/owner/repo  
**CLAUDE.md**: [View Original](https://github.com/owner/repo/blob/main/CLAUDE.md)  
**License**: License Name  

Project description...
```

### Header Fields

- **Category**: The category classification (required)
- **Repository**: Direct link to the GitHub repository (required)
- **CLAUDE.md**: Link to the original CLAUDE.md file (recommended)
- **License**: License information, automatically detected (required)

## Adding New Examples

When adding new analysis files:

1. **Create the directory structure**: `scenarios/[category]/[owner]_[repo]/`
2. **Write the analysis.md file** with the standard header format
3. **Run license detection**: Either manually or wait for the weekly workflow
4. **Verify license information**: Check that the detected license is correct

## Troubleshooting

### Repository Not Found

If the script reports "Repository not found":
- Verify the repository URL is correct and publicly accessible
- Check if the repository has been moved or renamed
- Ensure the directory name follows the `owner_repo` format

### No License Detected

If no license is found:
- The repository may not have a LICENSE file
- The repository may use a non-standard license format
- Consider manual verification and documentation

### Rate Limiting

Without a GitHub token, the API is limited to 60 requests per hour:
- Use `GITHUB_TOKEN` environment variable for authenticated requests (5,000/hour)
- The script includes automatic retry logic for rate limits

## License Information Display

License information helps users understand:
- **Usage Rights**: What they can do with the referenced code
- **Compliance Requirements**: Attribution and other obligations  
- **Commercial Use**: Whether commercial use is permitted
- **Distribution**: How code can be shared or modified

## Quality Standards

- **Accuracy**: All license information is automatically detected from authoritative sources
- **Consistency**: Standardized format across all analysis files
- **Maintenance**: Regular updates ensure license information stays current
- **Compliance**: Helps ensure the awesome-claude-md collection respects all referenced projects' licenses

## Contributing

When contributing new examples or updating existing ones:

1. Follow the standardized analysis file format
2. Ensure repository URLs are accurate and accessible
3. Run the license detection script to verify automation works
4. Include license information in your analysis

The automation handles license detection, but contributors should verify that detected licenses are accurate and current.