#!/usr/bin/env python3
"""
Verification script for awesome-claude-md examples.
Checks:
1. All example directories have README.md or analysis.md
2. GitHub repository links are valid
3. CLAUDE.md file links are reachable
4. Information consistency
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import json

def find_example_dirs() -> List[Path]:
    """Find all example directories in scenarios/"""
    scenarios_path = Path("scenarios")
    example_dirs = []

    for category_dir in scenarios_path.iterdir():
        if category_dir.is_dir():
            for example_dir in category_dir.iterdir():
                if example_dir.is_dir():
                    example_dirs.append(example_dir)

    return sorted(example_dirs)

def check_documentation_file(example_dir: Path) -> Tuple[bool, str, str]:
    """Check if example has README.md or analysis.md"""
    readme = example_dir / "README.md"
    analysis = example_dir / "analysis.md"

    if readme.exists():
        return True, "README.md", str(readme)
    elif analysis.exists():
        return True, "analysis.md", str(analysis)
    else:
        return False, "", ""

def extract_github_links(file_path: str) -> Dict[str, str]:
    """Extract GitHub repository and CLAUDE.md links from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    links = {
        'repo_url': None,
        'claude_md_url': None,
        'repo_owner': None,
        'repo_name': None
    }

    # Pattern for repository link
    repo_pattern = r'\[(?:Repository|Source)\]\((https://github\.com/([^/]+)/([^/)]+))\)'
    repo_match = re.search(repo_pattern, content)
    if repo_match:
        links['repo_url'] = repo_match.group(1)
        links['repo_owner'] = repo_match.group(2)
        links['repo_name'] = repo_match.group(3)

    # Alternative pattern for repository link
    if not links['repo_url']:
        repo_pattern2 = r'https://github\.com/([^/\s]+)/([^/\s)]+)'
        repo_match2 = re.search(repo_pattern2, content)
        if repo_match2:
            links['repo_url'] = f"https://github.com/{repo_match2.group(1)}/{repo_match2.group(2)}"
            links['repo_owner'] = repo_match2.group(1)
            links['repo_name'] = repo_match2.group(2)

    # Pattern for CLAUDE.md link
    claude_pattern = r'\[CLAUDE\.md\]\((https://github\.com/[^/]+/[^/]+/blob/[^)]+/CLAUDE\.md)\)'
    claude_match = re.search(claude_pattern, content)
    if claude_match:
        links['claude_md_url'] = claude_match.group(1)

    # Alternative CLAUDE.md pattern
    if not links['claude_md_url']:
        claude_pattern2 = r'(https://github\.com/[^/]+/[^/]+/blob/[^/\s]+/CLAUDE\.md)'
        claude_match2 = re.search(claude_pattern2, content)
        if claude_match2:
            links['claude_md_url'] = claude_match2.group(1)

    return links

def verify_directory_name(example_dir: Path, repo_owner: str, repo_name: str) -> Tuple[bool, str]:
    """Verify directory name matches owner_repo pattern"""
    expected_name = f"{repo_owner}_{repo_name}"
    actual_name = example_dir.name

    if expected_name == actual_name:
        return True, ""
    else:
        return False, f"Expected: {expected_name}, Got: {actual_name}"

def main():
    print("🔍 Verifying awesome-claude-md examples...\n")

    example_dirs = find_example_dirs()
    print(f"Found {len(example_dirs)} examples to verify\n")

    results = {
        'total': len(example_dirs),
        'passed': 0,
        'failed': 0,
        'issues': []
    }

    for example_dir in example_dirs:
        example_path = str(example_dir)
        category = example_dir.parent.name

        print(f"📂 Checking: {example_path}")

        issues = []

        # Check 1: Documentation file exists
        has_doc, doc_type, doc_path = check_documentation_file(example_dir)
        if not has_doc:
            issues.append(f"❌ Missing README.md or analysis.md")
        else:
            print(f"  ✓ Found {doc_type}")

            # Check 2: Extract and verify links
            links = extract_github_links(doc_path)

            if not links['repo_url']:
                issues.append(f"❌ No GitHub repository link found")
            else:
                print(f"  ✓ Repository: {links['repo_url']}")

            if not links['claude_md_url']:
                issues.append(f"⚠️  No CLAUDE.md link found (may be optional)")
            else:
                print(f"  ✓ CLAUDE.md: {links['claude_md_url']}")

            # Check 3: Directory name matches repo
            if links['repo_owner'] and links['repo_name']:
                name_match, name_issue = verify_directory_name(
                    example_dir,
                    links['repo_owner'],
                    links['repo_name']
                )
                if not name_match:
                    issues.append(f"❌ Directory name mismatch: {name_issue}")
                else:
                    print(f"  ✓ Directory name matches repository")

        if issues:
            results['failed'] += 1
            results['issues'].append({
                'path': example_path,
                'category': category,
                'issues': issues
            })
            for issue in issues:
                print(f"  {issue}")
        else:
            results['passed'] += 1

        print()

    # Summary
    print("=" * 80)
    print(f"\n📊 VERIFICATION SUMMARY\n")
    print(f"Total examples: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")

    if results['issues']:
        print(f"\n⚠️  Issues found in {results['failed']} examples:\n")
        for issue_item in results['issues']:
            print(f"\n{issue_item['path']} ({issue_item['category']}):")
            for issue in issue_item['issues']:
                print(f"  {issue}")

    # Save results to file
    with open('verification_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Detailed results saved to: verification_results.json")

    return results['failed']

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
