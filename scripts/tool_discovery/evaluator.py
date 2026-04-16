"""Tool evaluator for scoring and assessing CLAUDE.md tool candidates."""

import logging
import re
from datetime import datetime

import requests.exceptions
from github.GithubException import GithubException, UnknownObjectException

from scripts.discovery.utils import retry_with_backoff

logger = logging.getLogger(__name__)

# Permissive licenses that receive full license score
PERMISSIVE_LICENSES = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "isc",
    "0bsd",
    "unlicense",
}

# Known organizations that add credibility
RECOGNIZED_ORGS = {
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
    "stripe",
    "shopify",
}


class ToolEvaluator:
    """Handles evaluation and scoring of CLAUDE.md tool candidates."""

    def __init__(self, github_searcher=None):
        self.github_searcher = github_searcher
        # Scoring weights summing to 100
        self.tool_functionality_weight = 30
        self.documentation_quality_weight = 25
        self.license_quality_weight = 15
        self.project_maturity_weight = 20
        self.community_weight = 10

    def _validate_candidate(self, candidate: dict) -> bool:
        """Validate that a candidate dictionary has the required structure."""
        required_fields = ["full_name", "name", "owner", "stars", "html_url"]

        if not isinstance(candidate, dict):
            return False

        for field in required_fields:
            if field not in candidate:
                logger.warning(f"Candidate missing required field '{field}'")
                return False

        if not isinstance(candidate["stars"], int) or candidate["stars"] < 0:
            logger.warning(
                f"Invalid stars value for {candidate.get('full_name', 'unknown')}"
            )
            return False

        if not (
            candidate["html_url"].startswith("https://github.com/")
            or candidate["html_url"].startswith("http://github.com/")
        ):
            logger.warning(
                f"Invalid GitHub URL for {candidate.get('full_name', 'unknown')}"
            )
            return False

        return True

    def _get_readme_content(self, candidate: dict) -> str:
        """Get README content from candidate dict."""
        return candidate.get("readme_content", "")

    def _get_license_name(self, candidate: dict) -> str | None:
        """Extract normalized license name from candidate."""
        license_value = candidate.get("license") or candidate.get("license_name")
        if not license_value:
            return None
        return license_value.lower()

    @retry_with_backoff(
        max_retries=3,
        exceptions=(
            UnknownObjectException,
            GithubException,
            requests.exceptions.RequestException,
        ),
    )
    def evaluate_candidate(self, candidate: dict) -> dict | None:
        """Evaluate a tool candidate and return a scored assessment, or None if rejected."""
        if not self._validate_candidate(candidate):
            return None

        try:
            readme_content = self._get_readme_content(candidate)

            # Calculate scoring components
            (
                functionality_score,
                functionality_reasons,
            ) = self._calculate_tool_functionality_score(candidate, readme_content)
            documentation_score, documentation_reasons = self._score_readme_quality(
                readme_content
            )
            license_score, license_reasons = self._calculate_license_quality_score(
                candidate, readme_content
            )
            maturity_score, maturity_reasons = self._calculate_project_maturity_score(
                candidate, readme_content
            )
            community_score, community_reasons = self._calculate_community_score(
                candidate
            )

            score = (
                functionality_score
                + documentation_score
                + license_score
                + maturity_score
                + community_score
            )
            reasons = (
                functionality_reasons
                + documentation_reasons
                + license_reasons
                + maturity_reasons
                + community_reasons
            )

            tool_type = self._detect_tool_type(candidate, readme_content)

            evaluation = {
                "candidate": candidate,
                "score": min(score, 100),
                "reasons": reasons,
                "tool_type": tool_type,
                "readme_content_length": len(readme_content),
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

    def _calculate_tool_functionality_score(
        self, candidate: dict, readme_content: str
    ) -> tuple[int, list[str]]:
        """Calculate score based on tool functionality evidence (0-30 points)."""
        score = 0
        reasons: list[str] = []
        readme_lower = readme_content.lower()

        # CLI presence signals (0-12 points)
        cli_signals = [
            "bin/",
            '"bin"',
            '"scripts"',
            "[tool.",  # pyproject.toml [tool.scripts]
            "console_scripts",
            "entry_points",
            "#!/usr/bin/env",
            "#!/bin/sh",
            "#!/bin/bash",
        ]
        cli_count = sum(1 for sig in cli_signals if sig in readme_content)
        if cli_count >= 3:
            score += 12
            reasons.append("Strong CLI presence detected (multiple signals)")
        elif cli_count >= 1:
            score += 6
            reasons.append("CLI presence detected")

        # Installation instructions (0-8 points)
        install_patterns = [
            "npm install",
            "pip install",
            "cargo install",
            "brew install",
            "go install",
            "npx ",
        ]
        install_count = sum(1 for p in install_patterns if p in readme_lower)
        if install_count >= 2:
            score += 8
            reasons.append("Clear installation instructions provided")
        elif install_count >= 1:
            score += 4
            reasons.append("Installation instructions present")

        # CLAUDE.md-related keywords in README (0-10 points)
        claude_keywords = [
            "generate",
            "sync",
            "lint",
            "analyze",
            "manage",
            "claude.md",
            "agents.md",
            "claude code",
        ]
        keyword_count = sum(1 for kw in claude_keywords if kw in readme_lower)
        if keyword_count >= 4:
            score += 10
            reasons.append("Strongly CLAUDE.md-focused (multiple keywords)")
        elif keyword_count >= 2:
            score += 5
            reasons.append("CLAUDE.md-related functionality confirmed")
        elif keyword_count >= 1:
            score += 2
            reasons.append("Some CLAUDE.md-related keywords found")

        return min(score, self.tool_functionality_weight), reasons

    def _score_readme_quality(self, readme_content: str) -> tuple[int, list[str]]:
        """Calculate score based on README documentation quality (0-25 points)."""
        if not readme_content:
            return 0, []

        score = 0
        reasons: list[str] = []
        readme_lower = readme_content.lower()

        # README length (0-7 points)
        content_length = len(readme_content)
        if content_length >= 3000:
            score += 7
            reasons.append("Comprehensive README documentation")
        elif content_length >= 1500:
            score += 4
            reasons.append("Substantial README documentation")
        elif content_length >= 500:
            score += 2
            reasons.append("Basic README documentation present")

        # Usage examples / code blocks (0-8 points)
        code_block_count = readme_content.count("```")
        if code_block_count >= 6:
            score += 8
            reasons.append("Rich usage examples with code blocks")
        elif code_block_count >= 2:
            score += 4
            reasons.append("Usage examples present")

        # Installation section (0-5 points)
        install_section_keywords = [
            "## install",
            "## getting started",
            "## setup",
            "## usage",
            "## quick start",
        ]
        if any(kw in readme_lower for kw in install_section_keywords):
            score += 5
            reasons.append("Dedicated installation/setup section")

        # Feature list (0-5 points)
        feature_section_keywords = [
            "## features",
            "## what it does",
            "## capabilities",
            "## overview",
        ]
        if any(kw in readme_lower for kw in feature_section_keywords):
            score += 5
            reasons.append("Feature list documented")

        return min(score, self.documentation_quality_weight), reasons

    def _calculate_license_quality_score(
        self, candidate: dict, readme_content: str
    ) -> tuple[int, list[str]]:
        """Calculate score based on license quality (0-15 points)."""
        score = 0
        reasons: list[str] = []
        readme_lower = readme_content.lower()

        license_name = self._get_license_name(candidate)

        # Has license file (detected by API returning a license value)
        if license_name:
            score += 5
            reasons.append("Has a license file")

        # License quality: permissive gets full points, non-permissive gets partial
        if license_name in PERMISSIVE_LICENSES:
            score += 5
            reasons.append(f"Permissive license ({license_name})")
        elif license_name:
            score += 2
            reasons.append(f"Non-permissive license ({license_name})")

        # License mentioned in README
        license_readme_keywords = ["license", "mit", "apache", "bsd", "unlicense"]
        if any(kw in readme_lower for kw in license_readme_keywords):
            score += 5
            reasons.append("License referenced in README")

        return min(score, self.license_quality_weight), reasons

    def _score_star_count(self, candidate: dict) -> tuple[int, list[str]]:
        """Calculate score contribution from star count (0-5 points)."""
        score = 0
        reasons: list[str] = []
        stars = candidate.get("stars", 0)

        if stars >= 100:
            score += 5
            reasons.append(f"High community interest ({stars} stars)")
        elif stars >= 20:
            score += 3
            reasons.append(f"Growing community interest ({stars} stars)")

        return score, reasons

    def _calculate_project_maturity_score(
        self, candidate: dict, readme_content: str
    ) -> tuple[int, list[str]]:
        """Calculate score based on project maturity — excluding stars (0-20 points)."""
        score = 0
        reasons: list[str] = []
        readme_lower = readme_content.lower()

        # Recent activity (0-8 points)
        days_since_update = self._calculate_days_since_update(candidate)
        if days_since_update <= 30:
            score += 8
            reasons.append("Recently updated (last 30 days)")
        elif days_since_update <= 90:
            score += 4
            reasons.append("Updated in last 90 days")

        # Has releases (0-4 points) — look for release keywords in readme
        release_keywords = ["release", "changelog", "version", "v0.", "v1.", "v2."]
        if any(kw in readme_lower for kw in release_keywords):
            score += 4
            reasons.append("Has release history or versioning")

        # Project age > 3 months (0-3 points)
        created_at = candidate.get("created_at", "")
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                age_days = (
                    datetime.now().replace(tzinfo=created_date.tzinfo) - created_date
                ).days
                if age_days >= 90:
                    score += 3
                    reasons.append("Project older than 3 months")
            except (ValueError, TypeError) as e:
                logger.debug(f"Could not parse created_at date: {e}")

        return min(score, self.project_maturity_weight), reasons

    def _calculate_community_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Calculate score based on community signals (0-10 points)."""
        score = 0
        reasons: list[str] = []

        # Star count (0-5 points)
        stars = candidate.get("stars", 0)
        if stars >= 100:
            score += 5
            reasons.append(f"High community interest ({stars} stars)")
        elif stars >= 20:
            score += 3
            reasons.append(f"Growing community interest ({stars} stars)")

        # Known organizations (0-3 points)
        owner_lower = candidate["owner"].lower()
        if owner_lower in RECOGNIZED_ORGS:
            score += 3
            reasons.append(f"From recognized organization ({candidate['owner']})")

        # Contributors mentioned in README (0-2 points)
        readme_lower = candidate.get("readme_content", "").lower()
        contributor_keywords = [
            "contributors",
            "contributing",
            "## contributing",
            "pull request",
        ]
        if any(kw in readme_lower for kw in contributor_keywords):
            score += 2
            reasons.append("Community contribution guidelines present")

        return min(score, self.community_weight), reasons

    def _detect_tool_type(self, candidate: dict, readme_content: str) -> str:
        """Detect the type of CLAUDE.md tool from candidate metadata and README content."""
        readme_lower = readme_content.lower()
        desc_lower = candidate.get("description", "").lower()
        topics = [t.lower() for t in candidate.get("topics", [])]
        combined = f"{desc_lower} {readme_lower} {' '.join(topics)}"

        type_keywords: dict[str, list[str]] = {
            "cli": ["command-line", "command line", "cli", "terminal"],
            "plugin": ["plugin", "extension", "addon", "add-on"],
            "library": ["library", "sdk", "package", "module", "import this"],
            "service": ["api", "service", "saas", "platform", "deploy"],
            "generator": [
                "generat",
                "creat",
                "scaffold",
                "bootstrap",
                "init",
            ],
            "sync": ["sync", "synchron", "propagat"],
            "linter": ["lint", "validate", "check", "enforce", "verify", "audit"],
            "template": ["template", "boilerplate", "starter"],
        }

        scores: dict[str, int] = {}
        for tool_type, keywords in type_keywords.items():
            count = sum(1 for kw in keywords if re.search(kw, combined))
            if count > 0:
                scores[tool_type] = count

        if scores:
            return max(scores, key=scores.get)  # type: ignore[arg-type]

        return "other"

    def _calculate_days_since_update(self, candidate: dict) -> int:
        """Calculate days since last repository update."""
        updated_date = datetime.fromisoformat(
            candidate["updated_at"].replace("Z", "+00:00")
        )
        return (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days
