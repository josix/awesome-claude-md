"""Summary generator for tool discovery reports."""

import html
from typing import Any


class ToolSummaryGenerator:
    """Generates summary sections for tool discovery reports."""

    def __init__(self):
        pass

    def _sanitize_text(self, text: str) -> str:
        """Sanitize text content for safe inclusion in markdown/issues."""
        if not isinstance(text, str):
            return ""

        sanitized = html.escape(text)

        max_length = 500
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."

        return sanitized

    def generate_summary_section(self, counts: dict[str, int]) -> str:
        """Generate the summary section of the tool discovery report."""
        summary_lines = [
            "## 🎯 Tool Discovery Summary",
            f"- **Total Candidates**: {counts['total']}",
            f"- **Exceptional** (≥80 points): {counts['exceptional']}",
            f"- **High** (65-79 points): {counts['high']}",
            f"- **Good** (50-64 points): {counts['good']}",
            f"- **Below Threshold** (<50 points): {counts['below_threshold']}",
            "",
        ]
        return "\n".join(summary_lines)

    def generate_candidate_section(self, eval_data: dict[str, Any]) -> str:
        """Generate a section for a single tool candidate."""
        candidate = eval_data["candidate"]
        safe_name = self._sanitize_text(candidate["full_name"])
        safe_description = self._sanitize_text(
            candidate.get("description", "No description")
        )

        license_name = (
            candidate.get("license") or candidate.get("license_name") or "Unknown"
        )
        tool_type = eval_data.get("tool_type", "other")

        lines = [
            f"### [{safe_name}]({candidate['html_url']}) - **{eval_data['score']}/100 points**",
            f"**Description**: {safe_description}",
            f"**Tool Type**: {tool_type} | **License**: {license_name} | **Stars**: {candidate['stars']} | **Language**: {candidate.get('language', 'Unknown')}",
        ]

        if candidate.get("topics"):
            topics_str = ", ".join(candidate["topics"][:5])
            lines.append(f"**Topics**: {topics_str}")

        # Support both field names for backwards compatibility
        readme_size = eval_data.get(
            "readme_content_length", eval_data.get("readme_length", 0)
        )
        last_updated = eval_data.get("last_updated_days", "?")
        lines.extend(
            [
                f"**README Size**: {readme_size:,} bytes | **Last Updated**: {last_updated} days ago",
            ]
        )

        if eval_data["reasons"]:
            lines.append("**Scoring Reasons**:")
            for reason in eval_data["reasons"]:
                lines.append(f"- {reason}")

        lines.append("")
        return "\n".join(lines)

    def generate_guidelines_section(self) -> str:
        """Generate the review guidelines section for tool candidates."""
        guidelines = [
            "## 📋 Review Guidelines",
            "When reviewing tool candidates, please consider:",
            "- **Relevance**: Does the tool directly support CLAUDE.md workflows?",
            "- **Quality**: Is the tool well-documented and maintained?",
            "- **License**: Does it carry a permissive open-source license?",
            "- **Uniqueness**: Does it fill a gap in our current Tools & Ecosystem table?",
            "- **Maturity**: Is the project stable enough for recommendation?",
            "",
            "**Next Steps**: Review the candidates and update the README `Tools & Ecosystem` table for those that qualify.",
        ]
        return "\n".join(guidelines)
