#!/usr/bin/env python3
"""
Automated discovery script for new CLAUDE.md files across GitHub.

This script searches GitHub for repositories containing CLAUDE.md files,
evaluates them against quality standards, and creates issues for community
review of promising candidates.
"""

import os
import re
import json
import time
import html
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional
from pathlib import Path

import requests
from github import Github
from github.GithubException import RateLimitExceededException, UnknownObjectException, GithubException


class ClaudeFileDiscovery:
    """Discovers and evaluates new CLAUDE.md files on GitHub."""
    
    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        
        # Quality criteria based on project standards
        self.min_stars = 50  # Lower threshold for discovery, higher for auto-inclusion
        self.preferred_stars = 1000
        self.min_file_size = 500  # Minimum CLAUDE.md file size in bytes
        
        # Load existing repositories to avoid duplicates
        self.existing_repos = self._load_existing_repos()
        
    def _load_existing_repos(self) -> Set[str]:
        """Load list of repositories already included in the collection."""
        existing = set()
        scenarios_dir = Path('scenarios')
        
        if scenarios_dir.exists():
            for category_dir in scenarios_dir.iterdir():
                if category_dir.is_dir():
                    for repo_dir in category_dir.iterdir():
                        if repo_dir.is_dir():
                            # Extract owner/repo from directory name format: owner_repo
                            dir_name = repo_dir.name
                            if '_' in dir_name:
                                # Parse analysis.md file to get the actual repository URL
                                analysis_file = repo_dir / 'analysis.md'
                                if analysis_file.exists():
                                    try:
                                        with open(analysis_file, 'r', encoding='utf-8') as f:
                                            content = f.read()
                                            # Look for repository URL in the analysis file
                                            repo_match = re.search(r'\*\*Repository\*\*:\s*(?:\[.*?\]\()?https://github\.com/([^/\)\s]+/[^/\)\s]+)', content)
                                            if repo_match:
                                                existing.add(repo_match.group(1))
                                                continue
                                    except (IOError, UnicodeDecodeError) as e:
                                        print(f"Warning: Could not read {analysis_file}: {e}")
                                
                                # Fallback: Use simple first_last split for owner_repo format
                                # This assumes the first underscore separates owner from repo
                                parts = dir_name.split('_', 1)
                                if len(parts) == 2:
                                    owner, repo = parts
                                    existing.add(f"{owner}/{repo}")
                                        
    def _validate_candidate(self, candidate: Dict) -> bool:
        """Validate that a candidate dictionary has the required structure."""
        required_fields = ['full_name', 'name', 'owner', 'stars', 'html_url', 'claude_file_path']
        
        if not isinstance(candidate, dict):
            return False
            
        for field in required_fields:
            if field not in candidate:
                print(f"Warning: Candidate missing required field '{field}'")
                return False
                
        # Validate data types
        if not isinstance(candidate['stars'], int) or candidate['stars'] < 0:
            print(f"Warning: Invalid stars value for {candidate.get('full_name', 'unknown')}")
            return False
            
        # Validate URLs
        if not (candidate['html_url'].startswith('https://github.com/') or 
                candidate['html_url'].startswith('http://github.com/')):
            print(f"Warning: Invalid GitHub URL for {candidate.get('full_name', 'unknown')}")
            return False
            
        return True

    def _sanitize_text(self, text: str) -> str:
        """Sanitize text content for safe inclusion in markdown/issues."""
        if not isinstance(text, str):
            return ""
            
        # HTML escape to prevent injection
        sanitized = html.escape(text)
        
        # Limit length to prevent excessively long content
        max_length = 500
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."
            
        return sanitized
        
    def _handle_rate_limiting(self, response: requests.Response) -> None:
        """Handle GitHub API rate limiting adaptively."""
        # Check rate limit headers
        remaining = response.headers.get('X-RateLimit-Remaining')
        reset_time = response.headers.get('X-RateLimit-Reset')
        
        if remaining and int(remaining) < 10:
            if reset_time:
                reset_timestamp = int(reset_time)
                current_time = int(time.time())
                sleep_time = min(reset_timestamp - current_time + 1, 300)  # Max 5 minutes
                if sleep_time > 0:
                    print(f"Rate limit low, sleeping for {sleep_time} seconds")
                    time.sleep(sleep_time)
            else:
                # Default sleep if no reset time available
                time.sleep(10)
        else:
            # Normal rate limiting
            time.sleep(2)

    def search_github_repos(self) -> List[Dict]:
        """Search GitHub for repositories containing CLAUDE.md files."""
        candidates = []
        
        # Search queries for different file name variants
        search_queries = [
            'filename:claude.md',
            'filename:CLAUDE.md', 
            'filename:Claude.md'
        ]
        
        for query in search_queries:
            print(f"Searching with query: {query}")
            
            try:
                # Use GitHub Search API with pagination
                url = f"https://api.github.com/search/code?q={query}&sort=indexed&order=desc&per_page=100"
                response = self.session.get(url)
                response.raise_for_status()
                
                data = response.json()
                
                for item in data.get('items', []):
                    repo_info = item['repository']
                    full_name = repo_info['full_name']
                    
                    # Skip if already in collection
                    if full_name in self.existing_repos:
                        continue
                        
                    # Basic quality filters
                    if (repo_info['stargazers_count'] >= self.min_stars and
                        not repo_info.get('archived', False) and
                        not repo_info.get('fork', False)):
                        
                        candidate = {
                            'full_name': full_name,
                            'name': repo_info['name'],
                            'owner': repo_info['owner']['login'],
                            'description': repo_info.get('description', ''),
                            'stars': repo_info['stargazers_count'],
                            'language': repo_info.get('language'),
                            'updated_at': repo_info['updated_at'],
                            'html_url': repo_info['html_url'],
                            'claude_file_path': item['path'],
                            'clone_url': repo_info['clone_url']
                        }
                        
                        # Validate candidate structure
                        if self._validate_candidate(candidate):
                            candidates.append(candidate)
                        
                # Adaptive rate limiting
                self._handle_rate_limiting(response)
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"Rate limited or forbidden for query '{query}': {e}")
                    # Try to wait and continue
                    time.sleep(60)
                else:
                    print(f"HTTP error searching with query '{query}': {e}")
                continue
            except requests.exceptions.RequestException as e:
                print(f"Network error searching with query '{query}': {e}")
                continue
            except ValueError as e:
                print(f"JSON parsing error for query '{query}': {e}")
                continue
            except Exception as e:
                print(f"Unexpected error searching with query '{query}': {e}")
                continue
                
        # Remove duplicates based on full_name
        seen = set()
        unique_candidates = []
        for candidate in candidates:
            if candidate['full_name'] not in seen:
                seen.add(candidate['full_name'])
                unique_candidates.append(candidate)
                
        print(f"Found {len(unique_candidates)} unique candidate repositories")
        return unique_candidates
        
    def evaluate_candidate(self, candidate: Dict) -> Dict:
        """Evaluate a candidate repository against quality standards."""
        if not self._validate_candidate(candidate):
            return None
            
        full_name = candidate['full_name']
        
        try:
            # Get repository details
            repo = self.github.get_repo(full_name)
            
        except UnknownObjectException:
            print(f"Repository {full_name} not found or not accessible")
            return None
        except RateLimitExceededException:
            print(f"Rate limit exceeded while accessing {full_name}")
            return None
        except GithubException as e:
            print(f"GitHub API error for {full_name}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error accessing repository {full_name}: {e}")
            return None
            
        try:
            # Get CLAUDE.md file content
            claude_file_content = None
            claude_file_size = 0
            
            try:
                claude_file = repo.get_contents(candidate['claude_file_path'])
                claude_file_content = claude_file.decoded_content.decode('utf-8')
                claude_file_size = claude_file.size
            except UnknownObjectException:
                print(f"CLAUDE.md file not found in {full_name} at path {candidate['claude_file_path']}")
                return None
            except UnicodeDecodeError:
                print(f"Could not decode CLAUDE.md from {full_name} (invalid UTF-8)")
                return None
            except GithubException as e:
                print(f"GitHub API error fetching CLAUDE.md from {full_name}: {e}")
                return None
                
            # Quality evaluation criteria
            score = 0
            reasons = []
            
            # Star count scoring
            stars = candidate['stars']
            if stars >= self.preferred_stars:
                score += 3
                reasons.append(f"High star count ({stars:,} stars)")
            elif stars >= 500:
                score += 2
                reasons.append(f"Good star count ({stars:,} stars)")
            elif stars >= self.min_stars:
                score += 1
                reasons.append(f"Decent star count ({stars:,} stars)")
                
            # File size and content quality
            if claude_file_size >= self.min_file_size:
                score += 1
                reasons.append(f"Substantial CLAUDE.md file ({claude_file_size} bytes)")
                
            # Content analysis - look for quality indicators
            content_lower = claude_file_content.lower()
            
            quality_indicators = [
                ('architecture', 'Contains architecture documentation'),
                ('commands', 'Includes development commands'),
                ('setup', 'Has setup instructions'),
                ('testing', 'Includes testing information'),
                ('deployment', 'Contains deployment guidance'),
                ('workflow', 'Describes development workflow'),
                ('contributing', 'Has contribution guidelines')
            ]
            
            found_indicators = []
            for indicator, description in quality_indicators:
                if indicator in content_lower:
                    found_indicators.append(description)
                    
            if len(found_indicators) >= 3:
                score += 2
                reasons.append(f"Rich content ({len(found_indicators)} key sections)")
            elif len(found_indicators) >= 1:
                score += 1
                reasons.append(f"Good content ({len(found_indicators)} key sections)")
                
            # Recent activity
            try:
                updated_at = datetime.fromisoformat(candidate['updated_at'].replace('Z', '+00:00'))
                days_since_update = (datetime.now().astimezone() - updated_at).days
                
                if days_since_update <= 30:
                    score += 2
                    reasons.append("Recently updated (within 30 days)")
                elif days_since_update <= 90:
                    score += 1
                    reasons.append("Recently updated (within 90 days)")
            except (ValueError, TypeError) as e:
                print(f"Warning: Could not parse update date for {full_name}: {e}")
                days_since_update = 999  # Default to old
                
            # Organization recognition
            notable_orgs = [
                'microsoft', 'google', 'facebook', 'meta', 'apple', 'amazon',
                'cloudflare', 'anthropic', 'openai', 'pytorch', 'tensorflow',
                'langchain-ai', 'ethereum', 'mattermost', 'sentry', 'stripe',
                'vercel', 'supabase', 'planetscale', 'railway', 'fly'
            ]
            
            if candidate['owner'].lower() in notable_orgs:
                score += 2
                reasons.append(f"Notable organization ({candidate['owner']})")
                
            # Suggest category based on repo characteristics
            suggested_category = self._suggest_category(candidate, claude_file_content)
            
            return {
                'candidate': candidate,
                'score': score,
                'reasons': reasons,
                'claude_file_size': claude_file_size,
                'content_indicators': found_indicators,
                'days_since_update': days_since_update,
                'suggested_category': suggested_category,
                'evaluation_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Unexpected error evaluating {full_name}: {e}")
            return None
            
    def _suggest_category(self, candidate: Dict, claude_content: str) -> str:
        """Suggest the most appropriate category for a repository."""
        content_lower = claude_content.lower()
        description_lower = candidate.get('description', '').lower()
        
        # Category keywords
        categories = {
            'infrastructure-projects': [
                'runtime', 'infrastructure', 'platform', 'engine', 'server',
                'proxy', 'gateway', 'orchestration', 'kubernetes', 'docker'
            ],
            'complex-projects': [
                'application', 'platform', 'system', 'enterprise', 'full-stack',
                'microservices', 'distributed', 'monitoring', 'analytics'
            ],
            'developer-tooling': [
                'cli', 'tool', 'build', 'generator', 'parser', 'formatter',
                'linter', 'compiler', 'bundler', 'packager', 'deployment'
            ],
            'libraries-frameworks': [
                'library', 'framework', 'sdk', 'api', 'client', 'wrapper',
                'integration', 'connector', 'driver', 'adapter'
            ],
            'getting-started': [
                'tutorial', 'example', 'demo', 'quickstart', 'starter',
                'template', 'boilerplate', 'scaffold'
            ]
        }
        
        combined_text = f"{description_lower} {content_lower}"
        
        category_scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                category_scores[category] = score
                
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return 'complex-projects'  # Default category
            
    def create_discovery_issue(self, evaluations: List[Dict]) -> None:
        """Create a GitHub issue with discovered candidate repositories."""
        if not evaluations:
            print("No candidates to create issue for")
            return
            
        # Sort by score (highest first)
        evaluations.sort(key=lambda x: x['score'], reverse=True)
        
        # Create issue content
        title = f"Automated Discovery: {len(evaluations)} New CLAUDE.md Candidates Found"
        
        body_parts = [
            "# 🤖 Automated CLAUDE.md Discovery Report",
            "",
            f"Found **{len(evaluations)}** new repositories with CLAUDE.md files that meet our quality criteria.",
            "",
            "## 📊 Summary",
            "",
            f"- **Discovery Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"- **Total Candidates**: {len(evaluations)}",
            f"- **High Quality** (score ≥ 6): {len([e for e in evaluations if e['score'] >= 6])}",
            f"- **Good Quality** (score ≥ 4): {len([e for e in evaluations if e['score'] >= 4])}",
            "",
            "## 🏆 Top Candidates",
            ""
        ]
        
        for i, eval_result in enumerate(evaluations[:10], 1):  # Top 10
            candidate = eval_result['candidate']
            
            # Sanitize user-generated content
            safe_description = self._sanitize_text(candidate.get('description', 'No description available'))
            safe_owner = self._sanitize_text(candidate['owner'])
            safe_name = self._sanitize_text(candidate['name'])
            safe_language = self._sanitize_text(candidate.get('language', 'Unknown'))
            
            body_parts.extend([
                f"### {i}. [{safe_owner}/{safe_name}]({candidate['html_url']}) ⭐ {candidate['stars']:,}",
                "",
                f"**Score**: {eval_result['score']}/10 | **Suggested Category**: `{eval_result['suggested_category']}`",
                "",
                f"**Description**: {safe_description}",
                "",
                f"**Language**: {safe_language} | **Last Updated**: {candidate['updated_at'][:10]}",
                "",
                "**Quality Indicators**:",
                ""
            ])
            
            for reason in eval_result['reasons']:
                # Sanitize reason text (though it should be safe since it's generated by us)
                safe_reason = self._sanitize_text(reason)
                body_parts.append(f"- {safe_reason}")
                
            if eval_result['content_indicators']:
                body_parts.append("")
                body_parts.append("**Content Features**:")
                for indicator in eval_result['content_indicators']:
                    safe_indicator = self._sanitize_text(indicator)
                    body_parts.append(f"- {safe_indicator}")
                    
            body_parts.extend([
                "",
                f"**CLAUDE.md**: [{candidate['claude_file_path']}]({candidate['html_url']}/blob/main/{candidate['claude_file_path']})",
                "",
                "---",
                ""
            ])
            
        body_parts.extend([
            "## 🎯 Review Guidelines",
            "",
            "For each candidate, please consider:",
            "",
            "- **Quality**: Does the CLAUDE.md file demonstrate best practices?",
            "- **Uniqueness**: Does it offer patterns not already covered?",
            "- **Maintenance**: Is the repository actively maintained?",
            "- **Educational Value**: Would it help others learn effective CLAUDE.md patterns?",
            "",
            "## 🚀 Next Steps",
            "",
            "1. Review the candidates above",
            "2. For approved candidates, create analysis files in appropriate categories",
            "3. Update the main README.md with new entries",
            "4. Close this issue when review is complete",
            "",
            "---",
            "*This issue was automatically created by the discovery system. See `.github/workflows/discover-claude-files.yml` for details.*"
        ])
        
        body = "\n".join(body_parts)
        
        try:
            repo = self.github.get_repo(os.environ.get('GITHUB_REPOSITORY', 'josix/awesome-claude-md'))
            
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=['automation', 'discovery', 'review-needed']
            )
            
            print(f"Created issue #{issue.number}: {title}")
            
        except GithubException as e:
            print(f"GitHub API error creating issue: {e}")
            # Fallback: save to file for manual review
            self._save_discovery_report(title, body)
        except Exception as e:
            print(f"Unexpected error creating issue: {e}")
            # Fallback: save to file for manual review
            self._save_discovery_report(title, body)
            
    def _save_discovery_report(self, title: str, body: str) -> None:
        """Save discovery report to file as fallback."""
        try:
            filename = f"discovery-report-{datetime.now().strftime('%Y%m%d')}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n{body}")
            print(f"Saved discovery report to {filename}")
        except IOError as e:
            print(f"Error saving discovery report to file: {e}")


def main():
    """Main execution function."""
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is required")
        return 1
        
    print("🔍 Starting automated CLAUDE.md discovery...")
    
    discovery = ClaudeFileDiscovery(github_token)
    
    # Search for candidates
    candidates = discovery.search_github_repos()
    
    if not candidates:
        print("No new candidates found")
        return 0
        
    print(f"Evaluating {len(candidates)} candidates...")
    
    # Evaluate each candidate
    evaluations = []
    for candidate in candidates:
        eval_result = discovery.evaluate_candidate(candidate)
        if eval_result and eval_result['score'] >= 3:  # Minimum threshold
            evaluations.append(eval_result)
            
    print(f"Found {len(evaluations)} candidates that meet quality thresholds")
    
    if evaluations:
        # Create issue with findings
        discovery.create_discovery_issue(evaluations)
    else:
        print("No candidates met the quality threshold for review")
        
    return 0


if __name__ == '__main__':
    exit(main())