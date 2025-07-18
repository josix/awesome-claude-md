#!/usr/bin/env python3
"""
Automated discovery script for new CLAUDE.md files across GitHub.

This script searches GitHub for repositories containing CLAUDE.md files,
evaluates them against quality standards, and creates issues for community
review of promising candidates.

Refactored into separate classes following single responsibility principle.
"""

import functools
import html
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path

import requests
from github import Github
from github.GithubException import (
    GithubException,
    RateLimitExceededException,
    UnknownObjectException,
)


def retry_with_backoff(max_retries=3, backoff_factor=2, exceptions=(Exception,)):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor to multiply delay between retries
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = 1  # Start with 1 second delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        # Last attempt, re-raise the exception
                        raise e

                    # Log the retry attempt
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= backoff_factor

        return wrapper
    return decorator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


class RepositoryLoader:
    """Handles loading existing repositories from the collection."""

    def __init__(self):
        pass

    def load_existing_repos(self) -> set[str]:
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
                                analysis_file = repo_dir / 'README.md'
                                if analysis_file.exists():
                                    try:
                                        with open(analysis_file, encoding='utf-8') as f:
                                            content = f.read()
                                            # Look for repository URL in the analysis file
                                            repo_match = re.search(r'\*\*Repository\*\*:\s*(?:\[.*?\]\()?https://github\.com/([^/\)\s]+/[^/\)\s]+)', content)
                                            if repo_match:
                                                repo_name = repo_match.group(1)
                                                # Validate extracted repository name format
                                                if self._validate_repo_name(repo_name):
                                                    existing.add(repo_name)
                                                    continue
                                                else:
                                                    logger.warning(f"Invalid repository name format extracted: {repo_name}")
                                    except (OSError, UnicodeDecodeError) as e:
                                        logger.warning(f"Could not read {analysis_file}: {e}")
                                    except (re.error, AttributeError) as e:
                                        logger.warning(f"Regex parsing error for {analysis_file}: {e}")

                                # Fallback: Use simple first underscore split for owner_repo format
                                # This assumes the first underscore separates owner from repo
                                parts = dir_name.split('_', 1)
                                if len(parts) == 2:
                                    owner, repo = parts
                                    existing.add(f"{owner}/{repo}")

        logger.info(f"Loaded {len(existing)} existing repositories")
        return existing

    def _validate_repo_name(self, repo_name: str) -> bool:
        """Validate GitHub repository name format (owner/repo)."""
        if not isinstance(repo_name, str) or '/' not in repo_name:
            return False

        parts = repo_name.split('/')
        if len(parts) != 2:
            return False

        owner, repo = parts
        # Basic validation for GitHub username/org and repo name rules
        # GitHub usernames: 1-39 chars, alphanumeric or hyphens, can't start/end with hyphen
        # Repo names: similar rules but can contain dots, underscores
        if not (1 <= len(owner) <= 39 and re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', owner)):
            return False
        if not (1 <= len(repo) <= 100 and re.match(r'^[a-zA-Z0-9._-]+$', repo)):
            return False

        return True


class GitHubSearcher:
    """Handles GitHub API interactions and repository searching."""

    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.min_stars = 50
        self.min_file_size = 500

    def _handle_rate_limiting(self, response: requests.Response) -> None:
        """Handle GitHub API rate limiting adaptively."""
        # Check rate limit headers
        remaining = response.headers.get('X-RateLimit-Remaining')
        reset_time = response.headers.get('X-RateLimit-Reset')

        if remaining and int(remaining) < 10:
            if reset_time:
                try:
                    reset_timestamp = int(reset_time)
                    current_time = time.time()
                    # Cap sleep time at 60 seconds to avoid workflow timeout
                    sleep_time = min(reset_timestamp - current_time + 1, 60)
                    if sleep_time > 0:
                        logger.warning(f"Rate limit low, sleeping for {sleep_time} seconds")
                        time.sleep(sleep_time)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not parse rate limit headers: {e}")
                    time.sleep(1)  # Default 1 second delay

    @retry_with_backoff(max_retries=3, exceptions=(requests.exceptions.RequestException, GithubException))
    def search_github_repos(self, existing_repos: set[str]) -> list[dict]:
        """Search GitHub for repositories with CLAUDE.md files."""
        logger.info("Starting GitHub repository search...")

        search_queries = [
            'filename:claude.md',
            'filename:CLAUDE.md',
            'filename:Claude.md'
        ]

        all_candidates = []

        for query in search_queries:
            logger.info(f"Searching with query: {query}")

            try:
                # Search for repositories using the GitHub API
                # Use pagination to get more results (up to 3 pages = 300 results)
                for page in range(1, 4):  # Pages 1, 2, 3
                    search_results = self.github.search_repositories(
                        query=query,
                        sort='stars',
                        order='desc'
                    )

                    # Get specific page results
                    page_results = search_results.get_page(page - 1)  # get_page is 0-indexed

                    for repo in page_results:
                        # Skip repos we already have
                        if repo.full_name in existing_repos:
                            logger.debug(f"Skipping existing repository: {repo.full_name}")
                            continue

                        # Skip archived or forked repositories
                        if repo.archived or repo.fork:
                            logger.debug(f"Skipping archived/forked repository: {repo.full_name}")
                            continue

                        # Apply minimum quality filters
                        if repo.stargazers_count < self.min_stars:
                            logger.debug(f"Skipping low-star repository: {repo.full_name} ({repo.stargazers_count} stars)")
                            continue

                        # Try to fetch the CLAUDE.md file
                        claude_file_path = self._find_claude_file(repo)
                        if not claude_file_path:
                            logger.debug(f"No CLAUDE.md file found in {repo.full_name}")
                            continue

                        candidate = {
                            'full_name': repo.full_name,
                            'name': repo.name,
                            'owner': repo.owner.login,
                            'description': repo.description or '',
                            'stars': repo.stargazers_count,
                            'forks': repo.forks_count,
                            'language': repo.language,
                            'topics': repo.get_topics(),
                            'html_url': repo.html_url,
                            'created_at': repo.created_at.isoformat(),
                            'updated_at': repo.updated_at.isoformat(),
                            'claude_file_path': claude_file_path,
                            'organization': repo.organization.login if repo.organization else None
                        }

                        all_candidates.append(candidate)
                        logger.info(f"Found candidate: {repo.full_name} ({repo.stargazers_count} stars)")

                    # Add a small delay between page requests to be respectful
                    time.sleep(1)

            except RateLimitExceededException:
                logger.warning(f"Rate limit exceeded for query: {query}")
                time.sleep(60)  # Wait a minute before continuing
                continue
            except Exception as e:
                logger.error(f"Error searching with query '{query}': {e}")
                continue

        logger.info(f"Found {len(all_candidates)} candidate repositories")
        return all_candidates

    @retry_with_backoff(max_retries=3, exceptions=(UnknownObjectException, GithubException, requests.exceptions.HTTPError))
    def _find_claude_file(self, repo) -> str | None:
        """Find CLAUDE.md file in repository and validate its size."""
        possible_paths = ['claude.md', 'CLAUDE.md', 'Claude.md']

        for path in possible_paths:
            try:
                file_contents = repo.get_contents(path)

                # Check file size
                if file_contents.size < self.min_file_size:
                    logger.debug(f"CLAUDE.md file too small in {repo.full_name}: {file_contents.size} bytes")
                    continue

                return path

            except UnknownObjectException:
                # File doesn't exist at this path
                continue
            except (GithubException, requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
                logger.warning(f"Could not fetch CLAUDE.md from {repo.full_name}: {e}")
                continue

        return None


class RepositoryEvaluator:
    """Handles evaluation and scoring of repository candidates."""

    def __init__(self, github_searcher: GitHubSearcher):
        self.github_searcher = github_searcher
        self.preferred_stars = 1000

    def _validate_candidate(self, candidate: dict) -> bool:
        """Validate that a candidate dictionary has the required structure."""
        required_fields = ['full_name', 'name', 'owner', 'stars', 'html_url', 'claude_file_path']

        if not isinstance(candidate, dict):
            return False

        for field in required_fields:
            if field not in candidate:
                logger.warning(f"Candidate missing required field '{field}'")
                return False

        # Validate data types
        if not isinstance(candidate['stars'], int) or candidate['stars'] < 0:
            logger.warning(f"Invalid stars value for {candidate.get('full_name', 'unknown')}")
            return False

        # Validate URLs
        if not (candidate['html_url'].startswith('https://github.com/') or
                candidate['html_url'].startswith('http://github.com/')):
            logger.warning(f"Invalid GitHub URL for {candidate.get('full_name', 'unknown')}")
            return False

        return True

    @retry_with_backoff(max_retries=3, exceptions=(UnknownObjectException, GithubException, requests.exceptions.RequestException, UnicodeDecodeError))
    def evaluate_candidate(self, candidate: dict) -> dict:
        """Evaluate a repository candidate and return a scored assessment."""

        if not self._validate_candidate(candidate):
            return None

        try:
            # Get repository object
            repo = self.github_searcher.github.get_repo(candidate['full_name'])

            # Fetch CLAUDE.md content for analysis
            claude_content = ""
            try:
                claude_file = repo.get_contents(candidate['claude_file_path'])
                claude_content = claude_file.decoded_content.decode('utf-8')
            except (UnknownObjectException, GithubException, UnicodeDecodeError) as e:
                logger.warning(f"Could not fetch CLAUDE.md content from {candidate['full_name']}: {e}")

            # Score the candidate (0-10 scale)
            score = 0
            reasons = []

            # Stars scoring (0-3 points)
            if candidate['stars'] >= self.preferred_stars:
                score += 3
                reasons.append(f"High star count ({candidate['stars']})")
            elif candidate['stars'] >= 500:
                score += 2
                reasons.append(f"Good star count ({candidate['stars']})")
            elif candidate['stars'] >= 100:
                score += 1
                reasons.append(f"Moderate star count ({candidate['stars']})")

            # Content quality analysis (0-3 points)
            content_score = 0
            if claude_content:
                content_lower = claude_content.lower()

                # Look for key sections
                if any(section in content_lower for section in ['## architecture', '## overview', '## design']):
                    content_score += 1
                    reasons.append("Contains architecture documentation")

                if any(section in content_lower for section in ['## development', '## building', '## commands', '## setup']):
                    content_score += 1
                    reasons.append("Contains development instructions")

                if any(section in content_lower for section in ['## testing', '## tests', '## validation']):
                    content_score += 1
                    reasons.append("Contains testing information")

                # Length indicates thoroughness
                if len(claude_content) > 2000:
                    content_score = min(content_score + 1, 3)
                    reasons.append("Comprehensive documentation")

            score += content_score

            # Recent activity (0-2 points)
            updated_date = datetime.fromisoformat(candidate['updated_at'].replace('Z', '+00:00'))
            days_since_update = (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days

            if days_since_update <= 30:
                score += 2
                reasons.append("Recently updated (last 30 days)")
            elif days_since_update <= 90:
                score += 1
                reasons.append("Recently updated (last 90 days)")

            # Organization/user recognition (0-2 points)
            recognized_orgs = {
                'anthropic', 'openai', 'microsoft', 'google', 'meta', 'facebook',
                'apple', 'amazon', 'netflix', 'uber', 'airbnb', 'spotify',
                'github', 'gitlab', 'atlassian', 'docker', 'kubernetes',
                'pytorch', 'tensorflow', 'huggingface', 'langchain',
                'cloudflare', 'vercel', 'netlify', 'elastic', 'mongodb',
                'redis', 'postgresql', 'mysql', 'sentry', 'datadog',
                'stripe', 'twilio', 'shopify', 'square', 'paypal',
                'ethereum', 'bitcoin', 'polygon', 'chainlink'
            }

            owner_lower = candidate['owner'].lower()
            if owner_lower in recognized_orgs:
                score += 2
                reasons.append(f"From recognized organization ({candidate['owner']})")
            elif candidate['organization'] and candidate['organization'].lower() in recognized_orgs:
                score += 2
                reasons.append(f"From recognized organization ({candidate['organization']})")

            # Suggest appropriate category
            suggested_category = self._suggest_category(candidate, claude_content)

            evaluation = {
                'candidate': candidate,
                'score': score,
                'reasons': reasons,
                'suggested_category': suggested_category,
                'claude_content_length': len(claude_content) if claude_content else 0,
                'last_updated_days': days_since_update
            }

            logger.info(f"Evaluated {candidate['full_name']}: score {score}/10")
            return evaluation

        except (UnknownObjectException, GithubException) as e:
            logger.warning(f"Could not evaluate {candidate['full_name']}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error evaluating {candidate['full_name']}: {e}")
            return None

    def _suggest_category(self, candidate: dict, claude_content: str) -> str:
        """Suggest appropriate category based on repository characteristics."""

        # Keywords that suggest different categories
        categories = {
            'complex-projects': [
                'microservices', 'architecture', 'distributed', 'enterprise',
                'platform', 'system', 'infrastructure', 'scalable', 'multi-service'
            ],
            'libraries-frameworks': [
                'library', 'framework', 'sdk', 'api', 'npm', 'pypi', 'package',
                'component', 'widget', 'utility', 'helper'
            ],
            'developer-tooling': [
                'cli', 'tool', 'build', 'deploy', 'automation', 'workflow',
                'pipeline', 'ci/cd', 'development', 'debugging'
            ],
            'getting-started': [
                'tutorial', 'example', 'demo', 'sample', 'template', 'boilerplate',
                'starter', 'quickstart', 'beginner', 'learning'
            ]
        }

        # Analyze description and topics
        text_to_analyze = (
            (candidate.get('description', '') + ' ' +
             ' '.join(candidate.get('topics', [])) + ' ' +
             claude_content).lower()
        )

        category_scores = {}

        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                category_scores[category] = score

        # Return the category with the highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)

        # Default fallback based on language or other factors
        language = candidate.get('language', '').lower()
        if language in ['javascript', 'typescript', 'python', 'java', 'go', 'rust', 'c++']:
            return 'libraries-frameworks'

        return 'complex-projects'  # Default category


class IssueGenerator:
    """Handles GitHub issue creation and report generation."""

    def __init__(self, github_searcher: GitHubSearcher):
        self.github_searcher = github_searcher

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

    def create_discovery_issue(self, evaluations: list[dict]) -> None:
        """Create a GitHub issue with the discovery results."""
        if not evaluations:
            logger.info("No evaluations to report")
            return

        # Sort evaluations by score (highest first)
        sorted_evaluations = sorted(evaluations, key=lambda x: x['score'], reverse=True)

        # Create issue title
        high_score_count = len([e for e in evaluations if e['score'] >= 7])
        title = f"🤖 Weekly Discovery: {len(evaluations)} New CLAUDE.md Candidates Found"
        if high_score_count > 0:
            title += f" ({high_score_count} High Priority)"

        # Create issue body
        body_parts = []
        body_parts.append("## 🎯 Discovery Summary")
        body_parts.append(f"- **Total Candidates**: {len(evaluations)}")
        body_parts.append(f"- **High Priority** (≥7 points): {len([e for e in evaluations if e['score'] >= 7])}")
        body_parts.append(f"- **Medium Priority** (4-6 points): {len([e for e in evaluations if 4 <= e['score'] < 7])}")
        body_parts.append(f"- **Low Priority** (<4 points): {len([e for e in evaluations if e['score'] < 4])}")
        body_parts.append("")

        # Group by priority
        high_priority = [e for e in sorted_evaluations if e['score'] >= 7]
        medium_priority = [e for e in sorted_evaluations if 4 <= e['score'] < 7]
        low_priority = [e for e in sorted_evaluations if e['score'] < 4]

        for priority_group, title_suffix in [
            (high_priority, "High Priority (≥7 points)"),
            (medium_priority, "Medium Priority (4-6 points)"),
            (low_priority, "Low Priority (<4 points)")
        ]:
            if priority_group:
                body_parts.append(f"## 🔥 {title_suffix}")
                body_parts.append("")

                for eval_data in priority_group:
                    candidate = eval_data['candidate']
                    safe_name = self._sanitize_text(candidate['full_name'])
                    safe_description = self._sanitize_text(candidate.get('description', 'No description'))

                    # Create candidate section
                    body_parts.append(f"### [{safe_name}]({candidate['html_url']}) - **{eval_data['score']}/10 points**")
                    body_parts.append(f"**Description**: {safe_description}")
                    body_parts.append(f"**Stars**: {candidate['stars']} | **Language**: {candidate.get('language', 'Unknown')} | **Suggested Category**: {eval_data['suggested_category']}")

                    if candidate.get('topics'):
                        topics_str = ', '.join(candidate['topics'][:5])  # Limit to first 5 topics
                        body_parts.append(f"**Topics**: {topics_str}")

                    body_parts.append(f"**CLAUDE.md**: [{candidate['claude_file_path']}]({candidate['html_url']}/blob/main/{candidate['claude_file_path']})")
                    body_parts.append(f"**Content Size**: {eval_data['claude_content_length']:,} bytes | **Last Updated**: {eval_data['last_updated_days']} days ago")

                    # Add scoring reasons
                    if eval_data['reasons']:
                        body_parts.append("**Scoring Reasons**:")
                        for reason in eval_data['reasons']:
                            body_parts.append(f"- {reason}")

                    body_parts.append("")

        # Add review guidelines
        body_parts.append("## 📋 Review Guidelines")
        body_parts.append("When reviewing candidates, please consider:")
        body_parts.append("- **Quality**: Is the CLAUDE.md comprehensive and well-structured?")
        body_parts.append("- **Uniqueness**: Does it demonstrate patterns not already in our collection?")
        body_parts.append("- **Maintainability**: Is the repository actively maintained?")
        body_parts.append("- **Licensing**: Does it have an appropriate open source license?")
        body_parts.append("- **Category Fit**: Is the suggested category appropriate?")
        body_parts.append("")
        body_parts.append("**Next Steps**: Review the candidates and create PRs for those that should be added to the collection.")

        body = "\n".join(body_parts)

        # Save to file for review (useful for testing/debugging)
        self._save_discovery_report(title, body)

        logger.info(f"Would create issue: {title}")
        logger.info(f"Issue body length: {len(body)} characters")

    def _save_discovery_report(self, title: str, body: str) -> None:
        """Save discovery report to file for review."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"discovery_report_{timestamp}.md"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(body)

            logger.info(f"Discovery report saved to {filename}")
        except OSError as e:
            logger.error(f"Error saving discovery report to file: {e}")


class ClaudeFileDiscovery:
    """Orchestrates the discovery and evaluation of new CLAUDE.md files on GitHub."""

    def __init__(self, github_token: str):
        self.repo_loader = RepositoryLoader()
        self.github_searcher = GitHubSearcher(github_token)
        self.evaluator = RepositoryEvaluator(self.github_searcher)
        self.issue_generator = IssueGenerator(self.github_searcher)

        # Load existing repositories to avoid duplicates
        self.existing_repos = self.repo_loader.load_existing_repos()

    def discover_new_repositories(self) -> list[dict]:
        """Main discovery workflow: search, evaluate, and report on new repositories."""
        logger.info("Starting automated discovery of new CLAUDE.md repositories")

        # Search for candidate repositories
        candidates = self.github_searcher.search_github_repos(self.existing_repos)

        if not candidates:
            logger.info("No new candidates found")
            return []

        # Evaluate each candidate
        evaluations = []
        for candidate in candidates:
            evaluation = self.evaluator.evaluate_candidate(candidate)
            if evaluation:
                evaluations.append(evaluation)

        # Create discovery issue/report
        if evaluations:
            self.issue_generator.create_discovery_issue(evaluations)

        return evaluations


def main():
    """Main execution function."""
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        logger.error("Error: GITHUB_TOKEN environment variable is required")
        return 1

    logger.info("🔍 Starting automated CLAUDE.md discovery...")

    discovery = ClaudeFileDiscovery(github_token)

    # Run the discovery workflow
    evaluations = discovery.discover_new_repositories()

    # Filter for quality threshold
    quality_evaluations = [e for e in evaluations if e['score'] >= 3]

    logger.info(f"Found {len(quality_evaluations)} candidates that meet quality thresholds")

    if not quality_evaluations:
        logger.info("No candidates met the quality threshold for review")

    return 0


if __name__ == '__main__':
    exit(main())
