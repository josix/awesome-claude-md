"""Issue formatter for creating GitHub issues from tool discovery results."""

from typing import Any

from .priority_grouper import ToolPriorityGrouper
from .summary_generator import ToolSummaryGenerator


class ToolIssueFormatter:
    """Formats tool discovery results into GitHub issue content."""

    def __init__(self):
        self.priority_grouper = ToolPriorityGrouper()
        self.summary_generator = ToolSummaryGenerator()

    def create_issue_title(self, evaluations: list[dict[str, Any]]) -> str:
        """Create issue title based on tool evaluation results."""
        counts = self.priority_grouper.get_priority_counts(evaluations)

        title = f"Monthly Tool Discovery: {counts['total']} New CLAUDE.md Tool Candidates Found"
        if counts["exceptional"] > 0:
            title += f" ({counts['exceptional']} Exceptional)"
        elif counts["high"] > 0:
            title += f" ({counts['high']} High Priority)"

        return title

    def create_issue_body(self, evaluations: list[dict[str, Any]]) -> str:
        """Create complete issue body from tool evaluations."""
        if not evaluations:
            return "No new tool candidates found in this discovery run."

        groups = self.priority_grouper.group_evaluations(evaluations)
        counts = self.priority_grouper.get_priority_counts(evaluations)

        body_parts = []

        # Add summary section
        body_parts.append(self.summary_generator.generate_summary_section(counts))

        # Add priority sections
        priority_sections = [
            (groups["exceptional"], "Exceptional Quality (≥80 points)"),
            (groups["high"], "High Quality (65-79 points)"),
            (groups["good"], "Good Quality (50-64 points)"),
            (groups["below_threshold"], "Below Threshold (<50 points)"),
        ]

        for priority_group, title_suffix in priority_sections:
            if priority_group:
                body_parts.append(f"## 🔥 {title_suffix}")
                body_parts.append("")

                for eval_data in priority_group:
                    candidate_section = (
                        self.summary_generator.generate_candidate_section(eval_data)
                    )
                    body_parts.append(candidate_section)

        # Add guidelines
        body_parts.append(self.summary_generator.generate_guidelines_section())

        return "\n".join(body_parts)
