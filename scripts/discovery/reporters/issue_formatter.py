"""Issue formatter for creating GitHub issues from discovery results."""

from typing import Any

from .priority_grouper import PriorityGrouper
from .summary_generator import SummaryGenerator


class IssueFormatter:
    """Formats discovery results into GitHub issue content."""

    def __init__(self):
        self.priority_grouper = PriorityGrouper()
        self.summary_generator = SummaryGenerator()

    def create_issue_title(self, evaluations: list[dict[str, Any]]) -> str:
        """Create issue title based on evaluation results."""
        counts = self.priority_grouper.get_priority_counts(evaluations)

        title = f"🤖 Weekly Discovery: {counts['total']} New CLAUDE.md Candidates Found"
        if counts['high'] > 0:
            title += f" ({counts['high']} High Priority)"

        return title

    def create_issue_body(self, evaluations: list[dict[str, Any]]) -> str:
        """Create complete issue body from evaluations."""
        if not evaluations:
            return "No new candidates found in this discovery run."

        # Group evaluations by priority
        groups = self.priority_grouper.group_evaluations(evaluations)
        counts = self.priority_grouper.get_priority_counts(evaluations)

        # Build the issue body
        body_parts = []

        # Add summary section
        body_parts.append(self.summary_generator.generate_summary_section(counts))

        # Add priority sections
        priority_sections = [
            (groups['high'], "High Priority (≥7 points)"),
            (groups['medium'], "Medium Priority (4-6 points)"),
            (groups['low'], "Low Priority (<4 points)")
        ]

        for priority_group, title_suffix in priority_sections:
            if priority_group:
                body_parts.append(f"## 🔥 {title_suffix}")
                body_parts.append("")

                for eval_data in priority_group:
                    candidate_section = self.summary_generator.generate_candidate_section(eval_data)
                    body_parts.append(candidate_section)

        # Add guidelines
        body_parts.append(self.summary_generator.generate_guidelines_section())

        return "\n".join(body_parts)
