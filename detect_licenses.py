#!/usr/bin/env python3
"""
License Detection Script for awesome-claude-md

This script automatically detects license information for all repositories
referenced in analysis files using the GitHub API.
"""

import os
import re
import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse


class LicenseDetector:
    def __init__(self, github_token: Optional[str] = None):
        """Initialize the license detector with optional GitHub token for higher rate limits."""
        self.github_token = github_token
        self.session = requests.Session()
        if github_token:
            self.session.headers.update({'Authorization': f'token {github_token}'})
        
        # Cache to avoid duplicate API calls
        self.license_cache: Dict[str, Optional[str]] = {}
    
    def extract_repository_url(self, analysis_content: str) -> Optional[str]:
        """Extract the GitHub repository URL from analysis file content."""
        # Look for patterns like:
        # **Repository**: https://github.com/owner/repo
        # **Repository:** https://github.com/owner/repo  
        # **Source**: [owner/repo](https://github.com/owner/repo)
        # [View Original](https://github.com/owner/repo/...)
        
        patterns = [
            r'\*\*Repository\*\*:\s*https://github\.com/([^/\s]+/[^/\s]+)',
            r'\*\*Repository:\*\*\s*https://github\.com/([^/\s]+/[^/\s]+)',  
            r'\*\*Source\*\*:\s*\[([^]]+)\]\(https://github\.com/([^/\s)]+/[^/\s)]+)',
            r'https://github\.com/([^/\s]+/[^/\s)]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, analysis_content)
            if match:
                if len(match.groups()) == 1:
                    # Extract owner/repo and clean it up
                    repo_path = match.group(1)
                    # Handle cases where there might be additional path components
                    parts = repo_path.split('/')
                    if len(parts) >= 2:
                        return f"https://github.com/{parts[0]}/{parts[1]}"
                elif len(match.groups()) == 2:
                    return f"https://github.com/{match.group(2)}"
        
        return None
    
    def parse_github_url(self, url: str) -> Optional[Tuple[str, str]]:
        """Parse a GitHub URL to extract owner and repository name."""
        parsed = urlparse(url)
        if parsed.netloc != 'github.com':
            return None
        
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return path_parts[0], path_parts[1]
        
        return None
    
    def get_repository_license(self, owner: str, repo: str) -> Optional[str]:
        """Get license information from GitHub API."""
        cache_key = f"{owner}/{repo}"
        if cache_key in self.license_cache:
            return self.license_cache[cache_key]
        
        try:
            # First try to get license from repository info
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                repo_data = response.json()
                license_info = repo_data.get('license')
                if license_info and license_info.get('spdx_id') != 'NOASSERTION':
                    license_name = license_info.get('name', license_info.get('spdx_id'))
                    self.license_cache[cache_key] = license_name
                    return license_name
            
            elif response.status_code == 403:
                # Rate limited, wait and try again
                print(f"Rate limited, waiting 60 seconds...")
                time.sleep(60)
                return self.get_repository_license(owner, repo)
            
            elif response.status_code == 404:
                print(f"Repository not found: {owner}/{repo}")
                self.license_cache[cache_key] = None
                return None
            
            # If no license in main API, try the license endpoint
            license_url = f"https://api.github.com/repos/{owner}/{repo}/license"
            license_response = self.session.get(license_url)
            
            if license_response.status_code == 200:
                license_data = license_response.json()
                license_info = license_data.get('license', {})
                license_name = license_info.get('name', license_info.get('spdx_id'))
                self.license_cache[cache_key] = license_name
                return license_name
            
        except Exception as e:
            print(f"Error fetching license for {owner}/{repo}: {e}")
        
        self.license_cache[cache_key] = None
        return None
    
    def process_analysis_file(self, file_path: Path) -> Optional[str]:
        """Process a single analysis file and return license information."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check if license is already present
            if '**License**:' in content:
                # Extract existing license info
                match = re.search(r'\*\*License\*\*:\s*([^\n]+)', content)
                if match:
                    return match.group(1).strip()
            
            # Extract repository URL
            repo_url = self.extract_repository_url(content)
            
            # If no URL found in content, try to infer from directory structure
            if not repo_url:
                # Directory structure is like: scenarios/category/owner_repo/analysis.md
                parts = file_path.parts
                if len(parts) >= 3 and parts[-1] == 'analysis.md':
                    directory_name = parts[-2]  # e.g., "gaearon_overreacted.io"
                    if '_' in directory_name:
                        owner_repo = directory_name.replace('_', '/', 1)  # "gaearon/overreacted.io"
                        repo_url = f"https://github.com/{owner_repo}"
                        print(f"Inferred repository URL from directory: {repo_url}")
            
            if not repo_url:
                print(f"No repository URL found in {file_path}")
                return None
            
            # Parse URL to get owner/repo
            parsed = self.parse_github_url(repo_url)
            if not parsed:
                print(f"Could not parse GitHub URL: {repo_url}")
                return None
            
            owner, repo = parsed
            print(f"Checking license for {owner}/{repo}...")
            
            # Get license information
            license_info = self.get_repository_license(owner, repo)
            return license_info
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def update_analysis_file_with_license(self, file_path: Path, license_info: str) -> bool:
        """Update an analysis file to include license information."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check if license is already present
            if '**License**:' in content:
                print(f"License already present in {file_path}")
                return False
            
            # Find the best place to insert license information
            # Look for the header section with Category, Source, etc.
            lines = content.split('\n')
            insert_index = None
            
            for i, line in enumerate(lines):
                if line.startswith('**CLAUDE.md**:') or line.startswith('**Why it\'s exemplary**:'):
                    insert_index = i + 1
                    break
                elif line.startswith('**Source**:') or line.startswith('**Repository**:'):
                    insert_index = i + 1
                    break
            
            if insert_index is None:
                # Fallback: insert after the first line that ends with a line containing only markdown
                for i, line in enumerate(lines[:10]):  # Check first 10 lines
                    if line.strip() and not line.startswith('#') and not line.startswith('**'):
                        insert_index = i
                        break
            
            if insert_index is None:
                insert_index = 3  # Default fallback
            
            # Insert the license line
            license_line = f"**License**: {license_info}"
            lines.insert(insert_index, license_line)
            
            # Write back to file
            file_path.write_text('\n'.join(lines), encoding='utf-8')
            print(f"Updated {file_path} with license: {license_info}")
            return True
            
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
            return False
    
    def run(self, scenarios_dir: Path, update_files: bool = False) -> Dict[str, Optional[str]]:
        """Run license detection on all analysis files."""
        results = {}
        analysis_files = list(scenarios_dir.rglob('analysis.md'))
        
        print(f"Found {len(analysis_files)} analysis files")
        
        for file_path in analysis_files:
            relative_path = str(file_path.relative_to(scenarios_dir))
            print(f"\nProcessing: {relative_path}")
            
            license_info = self.process_analysis_file(file_path)
            results[relative_path] = license_info
            
            if license_info and update_files:
                self.update_analysis_file_with_license(file_path, license_info)
            
            # Small delay to be respectful to GitHub API
            time.sleep(0.5)
        
        return results


def main():
    """Main function to run license detection."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Detect licenses for repositories in analysis files')
    parser.add_argument('--update', action='store_true', help='Update analysis files with license information')
    parser.add_argument('--scenarios-dir', default='scenarios', help='Path to scenarios directory')
    parser.add_argument('--output', help='Output results to JSON file')
    
    args = parser.parse_args()
    
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Warning: No GITHUB_TOKEN environment variable found. API rate limits will be lower.")
    
    # Create detector
    detector = LicenseDetector(github_token)
    
    # Run detection
    scenarios_dir = Path(args.scenarios_dir)
    if not scenarios_dir.exists():
        print(f"Scenarios directory not found: {scenarios_dir}")
        return 1
    
    results = detector.run(scenarios_dir, update_files=args.update)
    
    # Print summary
    print("\n" + "="*50)
    print("LICENSE DETECTION SUMMARY")
    print("="*50)
    
    found_licenses = {k: v for k, v in results.items() if v}
    missing_licenses = {k: v for k, v in results.items() if not v}
    
    print(f"Total files processed: {len(results)}")
    print(f"Licenses found: {len(found_licenses)}")
    print(f"No license found: {len(missing_licenses)}")
    
    if found_licenses:
        print("\nFound licenses:")
        for file_path, license_info in found_licenses.items():
            print(f"  {file_path}: {license_info}")
    
    if missing_licenses:
        print("\nNo license information:")
        for file_path in missing_licenses.keys():
            print(f"  {file_path}")
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    exit(main())