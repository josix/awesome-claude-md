"""Main orchestrator for the CLAUDE.md tool discovery workflow."""

import logging
from typing import Any

from .evaluator import ToolEvaluator
from .loader import ToolLoader
from .reporter import ToolIssueGenerator
from .searcher import ToolSearcher

logger = logging.getLogger(__name__)


class ClaudeToolDiscovery:
    """Orchestrates the discovery and evaluation of CLAUDE.md-related tools on GitHub."""

    # Quality threshold for tool candidates (50-point scale)
    QUALITY_THRESHOLD = 50

    def __init__(self, github_token: str):
        self.tool_loader = ToolLoader()
        self.tool_searcher = ToolSearcher(github_token)
        self.evaluator = ToolEvaluator(self.tool_searcher)
        self.issue_generator = ToolIssueGenerator(self.tool_searcher)

        # Load existing tools to avoid duplicates
        self.existing_tools = self.tool_loader.load_existing_tools()

    def discover_new_tools(self) -> list[dict[str, Any]]:
        """Main discovery workflow: search, evaluate, and report on new tools."""
        logger.info("Starting automated discovery of CLAUDE.md-related tools")

        # Search for candidate tool repositories
        candidates = self.tool_searcher.search_github_repos(self.existing_tools)

        if not candidates:
            logger.info("No new tool candidates found")
            return []

        # Evaluate each candidate
        all_evaluations = []
        for candidate in candidates:
            evaluation = self.evaluator.evaluate_candidate(candidate)
            if evaluation:
                all_evaluations.append(evaluation)

        # Filter for quality threshold (50+ points)
        quality_evaluations = [
            e for e in all_evaluations if e["score"] >= self.QUALITY_THRESHOLD
        ]

        logger.info(
            f"Found {len(quality_evaluations)} tool candidates meeting quality threshold "
            f"({self.QUALITY_THRESHOLD}+ points)"
        )

        # Create discovery issue/report
        if quality_evaluations:
            self.issue_generator.create_discovery_issue(quality_evaluations)

        return quality_evaluations
