"""Main reporter class for GitHub issue creation and report generation."""

import logging
from datetime import datetime
from typing import List, Dict, Any

from .reporters.issue_formatter import IssueFormatter

logger = logging.getLogger(__name__)


class IssueGenerator:
    """Handles GitHub issue creation and report generation."""

    def __init__(self, github_searcher):
        self.github_searcher = github_searcher
        self.issue_formatter = IssueFormatter()

    def create_discovery_issue(self, evaluations: List[Dict[str, Any]]) -> None:
        """Create a GitHub issue with the discovery results."""
        if not evaluations:
            logger.info("No evaluations to report")
            return

        # Create issue title and body
        title = self.issue_formatter.create_issue_title(evaluations)
        body = self.issue_formatter.create_issue_body(evaluations)

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