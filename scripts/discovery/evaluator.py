"""Repository evaluator for scoring and assessing repository candidates."""

import logging
from datetime import datetime

from github.GithubException import GithubException, UnknownObjectException
import requests.exceptions

from .utils import retry_with_backoff

logger = logging.getLogger(__name__)


class RepositoryEvaluator:
    """Handles evaluation and scoring of repository candidates."""

    def __init__(self, github_searcher):
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
    def evaluate_candidate(self, candidate: dict) -> dict | None:
        """Evaluate a repository candidate and return a scored assessment."""

        if not self._validate_candidate(candidate):
            return None

        try:
            # Get repository object and fetch CLAUDE.md content
            repo = self.github_searcher.github.get_repo(candidate['full_name'])
            claude_content = self._fetch_claude_content(repo, candidate)

            # Calculate scores
            score = 0
            reasons = []

            # Calculate different scoring components
            stars_score, stars_reasons = self._calculate_stars_score(candidate)
            content_score, content_reasons = self._calculate_content_score(claude_content)
            activity_score, activity_reasons = self._calculate_activity_score(candidate)
            org_score, org_reasons = self._calculate_organization_score(candidate)

            # Combine scores
            score = stars_score + content_score + activity_score + org_score
            reasons.extend(stars_reasons + content_reasons + activity_reasons + org_reasons)

            # Suggest appropriate category
            suggested_category = self._suggest_category(candidate, claude_content)

            evaluation = {
                'candidate': candidate,
                'score': score,
                'reasons': reasons,
                'suggested_category': suggested_category,
                'claude_content_length': len(claude_content) if claude_content else 0,
                'last_updated_days': self._calculate_days_since_update(candidate)
            }

            logger.info(f"Evaluated {candidate['full_name']}: score {score}/10")
            return evaluation

        except (UnknownObjectException, GithubException) as e:
            logger.warning(f"Could not evaluate {candidate['full_name']}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error evaluating {candidate['full_name']}: {e}")
            return None

    def _fetch_claude_content(self, repo, candidate: dict) -> str:
        """Fetch CLAUDE.md content from repository."""
        try:
            claude_file = repo.get_contents(candidate['claude_file_path'])
            return claude_file.decoded_content.decode('utf-8')
        except (UnknownObjectException, GithubException, UnicodeDecodeError) as e:
            logger.warning(f"Could not fetch CLAUDE.md content from {candidate['full_name']}: {e}")
            return ""

    def _calculate_stars_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Calculate score based on star count (0-3 points)."""
        stars = candidate['stars']
        if stars >= self.preferred_stars:
            return 3, [f"High star count ({stars})"]
        elif stars >= 500:
            return 2, [f"Good star count ({stars})"]
        elif stars >= 100:
            return 1, [f"Moderate star count ({stars})"]
        return 0, []

    def _calculate_content_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Calculate score based on content quality (0-3 points)."""
        if not claude_content:
            return 0, []

        content_lower = claude_content.lower()
        score = 0
        reasons = []

        # Look for key sections
        if any(section in content_lower for section in ['## architecture', '## overview', '## design']):
            score += 1
            reasons.append("Contains architecture documentation")

        if any(section in content_lower for section in ['## development', '## building', '## commands', '## setup']):
            score += 1
            reasons.append("Contains development instructions")

        if any(section in content_lower for section in ['## testing', '## tests', '## validation']):
            score += 1
            reasons.append("Contains testing information")

        # Length indicates thoroughness
        if len(claude_content) > 2000:
            score = min(score + 1, 3)
            reasons.append("Comprehensive documentation")

        return score, reasons

    def _calculate_activity_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Calculate score based on recent activity (0-2 points)."""
        days_since_update = self._calculate_days_since_update(candidate)

        if days_since_update <= 30:
            return 2, ["Recently updated (last 30 days)"]
        elif days_since_update <= 90:
            return 1, ["Recently updated (last 90 days)"]
        return 0, []

    def _calculate_organization_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Calculate score based on organization recognition (0-2 points)."""
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
            return 2, [f"From recognized organization ({candidate['owner']})"]
        elif candidate['organization'] and candidate['organization'].lower() in recognized_orgs:
            return 2, [f"From recognized organization ({candidate['organization']})"]
        return 0, []

    def _calculate_days_since_update(self, candidate: dict) -> int:
        """Calculate days since last repository update."""
        updated_date = datetime.fromisoformat(candidate['updated_at'].replace('Z', '+00:00'))
        return (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days

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