"""Repository evaluator for scoring and assessing repository candidates."""

import logging
from datetime import datetime

import requests.exceptions
from github.GithubException import GithubException, UnknownObjectException

from .utils import retry_with_backoff

logger = logging.getLogger(__name__)


class RepositoryEvaluator:
    """Handles evaluation and scoring of repository candidates using content-first approach."""

    def __init__(self, github_searcher):
        self.github_searcher = github_searcher
        # Content-first scoring weights
        self.content_depth_weight = 30
        self.educational_value_weight = 25
        self.ai_effectiveness_weight = 15
        self.project_maturity_weight = 20
        self.community_recognition_weight = 10

    def _validate_candidate(self, candidate: dict) -> bool:
        """Validate that a candidate dictionary has the required structure."""
        required_fields = [
            "full_name",
            "name",
            "owner",
            "stars",
            "html_url",
            "claude_file_path",
        ]

        if not isinstance(candidate, dict):
            return False

        for field in required_fields:
            if field not in candidate:
                logger.warning(f"Candidate missing required field '{field}'")
                return False

        # Validate data types
        if not isinstance(candidate["stars"], int) or candidate["stars"] < 0:
            logger.warning(
                f"Invalid stars value for {candidate.get('full_name', 'unknown')}"
            )
            return False

        # Validate URLs
        if not (
            candidate["html_url"].startswith("https://github.com/")
            or candidate["html_url"].startswith("http://github.com/")
        ):
            logger.warning(
                f"Invalid GitHub URL for {candidate.get('full_name', 'unknown')}"
            )
            return False

        return True

    @retry_with_backoff(
        max_retries=3,
        exceptions=(
            UnknownObjectException,
            GithubException,
            requests.exceptions.RequestException,
            UnicodeDecodeError,
        ),
    )
    def evaluate_candidate(self, candidate: dict) -> dict | None:
        """Evaluate a repository candidate and return a scored assessment."""

        if not self._validate_candidate(candidate):
            return None

        try:
            # Get repository object and fetch CLAUDE.md content
            repo = self.github_searcher.github.get_repo(candidate["full_name"])
            claude_content = self._fetch_claude_content(repo, candidate)

            # Calculate scores
            score = 0
            reasons = []

            # Calculate content-first scoring components (0-100 scale)
            (
                content_depth_score,
                content_depth_reasons,
            ) = self._calculate_content_depth_score(claude_content)
            (
                educational_score,
                educational_reasons,
            ) = self._calculate_educational_value_score(claude_content, candidate)
            (
                ai_effectiveness_score,
                ai_effectiveness_reasons,
            ) = self._calculate_ai_effectiveness_score(claude_content)
            maturity_score, maturity_reasons = self._calculate_project_maturity_score(
                candidate
            )
            (
                recognition_score,
                recognition_reasons,
            ) = self._calculate_community_recognition_score(candidate)

            # Combine scores with weights
            score = (
                content_depth_score
                + educational_score
                + ai_effectiveness_score
                + maturity_score
                + recognition_score
            )
            reasons.extend(
                content_depth_reasons
                + educational_reasons
                + ai_effectiveness_reasons
                + maturity_reasons
                + recognition_reasons
            )

            # Suggest appropriate category
            suggested_category = self._suggest_category(candidate, claude_content)

            evaluation = {
                "candidate": candidate,
                "score": score,
                "reasons": reasons,
                "suggested_category": suggested_category,
                "claude_content_length": len(claude_content) if claude_content else 0,
                "last_updated_days": self._calculate_days_since_update(candidate),
            }

            logger.info(f"Evaluated {candidate['full_name']}: score {score}/100")
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
            claude_file = repo.get_contents(candidate["claude_file_path"])
            return claude_file.decoded_content.decode("utf-8")
        except (UnknownObjectException, GithubException, UnicodeDecodeError) as e:
            logger.warning(
                f"Could not fetch CLAUDE.md content from {candidate['full_name']}: {e}"
            )
            return ""

    def _calculate_content_depth_score(
        self, claude_content: str
    ) -> tuple[int, list[str]]:
        """Calculate score based on content depth and structure (0-30 points)."""
        if not claude_content:
            return 0, []

        content_lower = claude_content.lower()
        score = 0
        reasons = []

        # Architecture documentation (0-8 points)
        architecture_keywords = [
            "## architecture",
            "## overview",
            "## design",
            "## system",
            "## structure",
        ]
        if any(keyword in content_lower for keyword in architecture_keywords):
            score += 8
            reasons.append("Contains comprehensive architecture documentation")

        # Development workflows (0-8 points)
        dev_keywords = [
            "## development",
            "## building",
            "## commands",
            "## setup",
            "## workflow",
        ]
        if any(keyword in content_lower for keyword in dev_keywords):
            score += 8
            reasons.append("Contains clear development workflows")

        # Testing and deployment (0-6 points)
        test_deploy_keywords = [
            "## testing",
            "## tests",
            "## deployment",
            "## production",
        ]
        if any(keyword in content_lower for keyword in test_deploy_keywords):
            score += 6
            reasons.append("Contains testing and deployment guidance")

        # File organization and context (0-4 points)
        if len(claude_content) > 3000:
            score += 4
            reasons.append("Comprehensive and detailed documentation")
        elif len(claude_content) > 1500:
            score += 2
            reasons.append("Substantial documentation")

        # Troubleshooting information (0-4 points)
        troubleshoot_keywords = [
            "## troubleshooting",
            "## debugging",
            "## known issues",
            "## faq",
        ]
        if any(keyword in content_lower for keyword in troubleshoot_keywords):
            score += 4
            reasons.append("Contains troubleshooting information")

        return min(score, self.content_depth_weight), reasons

    def _calculate_educational_value_score(
        self, claude_content: str, candidate: dict
    ) -> tuple[int, list[str]]:
        """Calculate score based on educational value (0-25 points)."""
        if not claude_content:
            return 0, []

        content_lower = claude_content.lower()
        score = 0
        reasons = []

        # Advanced patterns and techniques (0-10 points)
        advanced_keywords = [
            "pattern",
            "best practice",
            "architecture",
            "design principle",
            "methodology",
        ]
        advanced_count = sum(
            1 for keyword in advanced_keywords if keyword in content_lower
        )
        if advanced_count >= 3:
            score += 10
            reasons.append("Demonstrates advanced patterns and techniques")
        elif advanced_count >= 1:
            score += 5
            reasons.append("Shows some advanced patterns")

        # Concrete examples and code snippets (0-8 points)
        if "```" in claude_content or "example" in content_lower:
            score += 8
            reasons.append("Includes concrete examples and code snippets")

        # Actionable guidance (0-7 points)
        actionable_keywords = ["step", "how to", "guide", "tutorial", "instruction"]
        if any(keyword in content_lower for keyword in actionable_keywords):
            score += 7
            reasons.append("Provides actionable, specific guidance")

        return min(score, self.educational_value_weight), reasons

    def _calculate_ai_effectiveness_score(
        self, claude_content: str
    ) -> tuple[int, list[str]]:
        """Calculate score based on AI assistant effectiveness (0-15 points)."""
        if not claude_content:
            return 0, []

        score = 0
        reasons = []

        # Well-structured sections (0-6 points)
        section_count = claude_content.count("##")
        if section_count >= 8:
            score += 6
            reasons.append("Well-organized with clear section headers")
        elif section_count >= 4:
            score += 3
            reasons.append("Good section organization")

        # Specific commands and workflows (0-5 points)
        if (
            "npm" in claude_content
            or "yarn" in claude_content
            or "pip" in claude_content
            or "cargo" in claude_content
        ):
            score += 5
            reasons.append("Contains specific commands and workflows")

        # Context about goals and constraints (0-4 points)
        context_keywords = [
            "goal",
            "purpose",
            "constraint",
            "requirement",
            "limitation",
        ]
        if any(keyword in claude_content.lower() for keyword in context_keywords):
            score += 4
            reasons.append("Provides project context and constraints")

        return min(score, self.ai_effectiveness_weight), reasons

    def _calculate_project_maturity_score(
        self, candidate: dict
    ) -> tuple[int, list[str]]:
        """Calculate score based on project maturity (0-20 points)."""
        score = 0
        reasons = []

        # Recent activity (0-8 points)
        days_since_update = self._calculate_days_since_update(candidate)
        if days_since_update <= 30:
            score += 8
            reasons.append("Recently updated (last 30 days)")
        elif days_since_update <= 90:
            score += 4
            reasons.append("Recently updated (last 90 days)")

        # Community engagement (0-6 points)
        stars = candidate["stars"]
        if stars >= 100:
            score += 6
            reasons.append(f"Good community engagement ({stars} stars)")
        elif stars >= 10:
            score += 3
            reasons.append(f"Some community engagement ({stars} stars)")

        # Production indicators (0-6 points)
        if candidate.get("description"):
            desc_lower = candidate["description"].lower()
            prod_keywords = ["production", "enterprise", "scale", "deployed", "used by"]
            if any(keyword in desc_lower for keyword in prod_keywords):
                score += 6
                reasons.append("Evidence of production usage")

        return min(score, self.project_maturity_weight), reasons

    def _calculate_community_recognition_score(
        self, candidate: dict
    ) -> tuple[int, list[str]]:
        """Calculate score based on community recognition (0-10 points)."""
        score = 0
        reasons = []

        # Notable organizations (0-5 points) - reduced impact
        recognized_orgs = {
            "anthropic",
            "openai",
            "microsoft",
            "google",
            "meta",
            "facebook",
            "apple",
            "amazon",
            "netflix",
            "uber",
            "airbnb",
            "spotify",
            "github",
            "gitlab",
            "atlassian",
            "docker",
            "kubernetes",
            "pytorch",
            "tensorflow",
            "huggingface",
            "langchain",
            "cloudflare",
            "vercel",
            "netlify",
            "elastic",
            "mongodb",
            "redis",
            "postgresql",
            "mysql",
            "sentry",
            "datadog",
            "stripe",
            "twilio",
            "shopify",
            "square",
            "paypal",
            "ethereum",
            "bitcoin",
            "polygon",
            "chainlink",
        }

        owner_lower = candidate["owner"].lower()
        if owner_lower in recognized_orgs:
            score += 5
            reasons.append(f"From recognized organization ({candidate['owner']})")
        elif (
            candidate.get("organization")
            and candidate["organization"].lower() in recognized_orgs
        ):
            score += 5
            reasons.append(
                f"From recognized organization ({candidate['organization']})"
            )

        # High star count as validation (0-5 points) - reduced from primary factor
        stars = candidate["stars"]
        if stars >= 1000:
            score += 5
            reasons.append(f"High community validation ({stars} stars)")
        elif stars >= 500:
            score += 3
            reasons.append(f"Good community validation ({stars} stars)")

        return min(score, self.community_recognition_weight), reasons

    def _calculate_days_since_update(self, candidate: dict) -> int:
        """Calculate days since last repository update."""
        updated_date = datetime.fromisoformat(
            candidate["updated_at"].replace("Z", "+00:00")
        )
        return (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days

    def _suggest_category(self, candidate: dict, claude_content: str) -> str:
        """Suggest appropriate category based on repository characteristics."""

        # Keywords that suggest different categories
        categories = {
            "complex-projects": [
                "microservices",
                "architecture",
                "distributed",
                "enterprise",
                "platform",
                "system",
                "infrastructure",
                "scalable",
                "multi-service",
            ],
            "libraries-frameworks": [
                "library",
                "framework",
                "sdk",
                "api",
                "npm",
                "pypi",
                "package",
                "component",
                "widget",
                "utility",
                "helper",
            ],
            "developer-tooling": [
                "cli",
                "tool",
                "build",
                "deploy",
                "automation",
                "workflow",
                "pipeline",
                "ci/cd",
                "development",
                "debugging",
            ],
            "getting-started": [
                "tutorial",
                "example",
                "demo",
                "sample",
                "template",
                "boilerplate",
                "starter",
                "quickstart",
                "beginner",
                "learning",
            ],
        }

        # Analyze description and topics
        text_to_analyze = (
            candidate.get("description", "")
            + " "
            + " ".join(candidate.get("topics", []))
            + " "
            + claude_content
        ).lower()

        category_scores = {}

        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                category_scores[category] = score

        # Return the category with the highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)

        # Default fallback based on language or other factors
        language = candidate.get("language", "").lower()
        if language in [
            "javascript",
            "typescript",
            "python",
            "java",
            "go",
            "rust",
            "c++",
        ]:
            return "libraries-frameworks"

        return "complex-projects"  # Default category
