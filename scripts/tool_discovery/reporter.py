"""Main reporter class for tool discovery GitHub issue creation."""

import logging
from datetime import datetime
from typing import Any

from .reporters.issue_formatter import ToolIssueFormatter

logger = logging.getLogger(__name__)


class ToolIssueGenerator:
    """Handles GitHub issue creation and report generation for tool discovery."""

    def __init__(self, github_searcher):
        self.github_searcher = github_searcher
        self.issue_formatter = ToolIssueFormatter()

    def _get_issue_labels(self) -> list[str]:
        """Return labels to apply to the discovery issue."""
        return ["automation", "tool-discovery", "review-needed"]

    def create_discovery_issue(self, evaluations: list[dict[str, Any]]) -> None:
        """Create a GitHub issue with the tool discovery results."""
        if not evaluations:
            logger.info("No tool evaluations to report")
            return

        title = self.issue_formatter.create_issue_title(evaluations)
        body = self.issue_formatter.create_issue_body(evaluations)

        body = self._validate_and_truncate_body(body, evaluations)

        self._save_discovery_report(title, body)

        try:
            repo = self.github_searcher.github.get_repo("josix/awesome-claude-md")
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=self._get_issue_labels(),
            )
            logger.info(f"Created GitHub issue #{issue.number}: {title}")
            logger.info(f"Issue URL: {issue.html_url}")
        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {e}")
            logger.info(f"Issue title: {title}")
            logger.info(f"Issue body length: {len(body)} characters")

    def _validate_and_truncate_body(
        self, body: str, evaluations: list[dict[str, Any]]
    ) -> str:
        """Validate and truncate issue body if it exceeds GitHub's limit."""
        max_length = 65536  # GitHub's maximum issue body length

        if len(body) <= max_length:
            return body

        logger.warning(
            f"Issue body too long ({len(body)} chars), truncating to fit GitHub limit"
        )

        truncation_notice = (
            "\n\n---\n\n"
            "⚠️ **Content Truncated**: This issue was automatically truncated due to GitHub's "
            "65,536 character limit. The complete report has been saved to a local file for review.\n\n"
            f"**Total candidates found**: {len(evaluations)}\n"
            f"**Original content length**: {len(body):,} characters\n"
            f"**Truncated content length**: {max_length:,} characters"
        )

        available_space = max_length - len(truncation_notice)
        truncated_body = body[:available_space].rsplit("\n", 1)[0]
        return truncated_body + truncation_notice

    def _save_discovery_report(self, title: str, body: str) -> None:
        """Save tool discovery report to file for review."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tool_discovery_report_{timestamp}.md"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n")
                f.write(body)

            logger.info(f"Tool discovery report saved to {filename}")
        except OSError as e:
            logger.error(f"Error saving tool discovery report to file: {e}")
