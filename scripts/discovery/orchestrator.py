"""Main orchestrator for the discovery workflow."""

import logging
from typing import List, Dict, Any

from .loader import RepositoryLoader
from .searcher import GitHubSearcher
from .evaluator import RepositoryEvaluator
from .reporter import IssueGenerator

logger = logging.getLogger(__name__)


class ClaudeFileDiscovery:
    """Orchestrates the discovery and evaluation of new CLAUDE.md files on GitHub."""

    def __init__(self, github_token: str):
        self.repo_loader = RepositoryLoader()
        self.github_searcher = GitHubSearcher(github_token)
        self.evaluator = RepositoryEvaluator(self.github_searcher)
        self.issue_generator = IssueGenerator(self.github_searcher)

        # Load existing repositories to avoid duplicates
        self.existing_repos = self.repo_loader.load_existing_repos()

    def discover_new_repositories(self) -> List[Dict[str, Any]]:
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