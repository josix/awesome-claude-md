"""Summary generator for discovery reports."""

import html
from typing import Any


class SummaryGenerator:
    """Generates summary sections for discovery reports."""

    def __init__(self):
        pass

    def _sanitize_text(self, text: str) -> str:
        """Sanitize text content for safe inclusion in markdown/issues."""
        if not isinstance(text, str):
            return ""

        # HTML escape to prevent injection
        sanitized = html.escape(text)

        # Limit length to prevent excessively long content
        max_length = 500
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."

        return sanitized

    def generate_summary_section(self, counts: dict[str, int]) -> str:
        """Generate the summary section of the report."""
        summary_lines = [
            "## 🎯 Discovery Summary",
            f"- **Total Candidates**: {counts['total']}",
            f"- **High Priority** (≥7 points): {counts['high']}",
            f"- **Medium Priority** (4-6 points): {counts['medium']}",
            f"- **Low Priority** (<4 points): {counts['low']}",
            ""
        ]
        return "\n".join(summary_lines)

    def generate_candidate_section(self, eval_data: dict[str, Any]) -> str:
        """Generate a section for a single candidate."""
        candidate = eval_data['candidate']
        safe_name = self._sanitize_text(candidate['full_name'])
        safe_description = self._sanitize_text(candidate.get('description', 'No description'))

        lines = [
            f"### [{safe_name}]({candidate['html_url']}) - **{eval_data['score']}/10 points**",
            f"**Description**: {safe_description}",
            f"**Stars**: {candidate['stars']} | **Language**: {candidate.get('language', 'Unknown')} | **Suggested Category**: {eval_data['suggested_category']}",
        ]

        if candidate.get('topics'):
            topics_str = ', '.join(candidate['topics'][:5])  # Limit to first 5 topics
            lines.append(f"**Topics**: {topics_str}")

        lines.extend([
            f"**CLAUDE.md**: [{candidate['claude_file_path']}]({candidate['html_url']}/blob/main/{candidate['claude_file_path']})",
            f"**Content Size**: {eval_data['claude_content_length']:,} bytes | **Last Updated**: {eval_data['last_updated_days']} days ago"
        ])

        # Add scoring reasons
        if eval_data['reasons']:
            lines.append("**Scoring Reasons**:")
            for reason in eval_data['reasons']:
                lines.append(f"- {reason}")

        lines.append("")
        return "\n".join(lines)

    def generate_guidelines_section(self) -> str:
        """Generate the review guidelines section."""
        guidelines = [
            "## 📋 Review Guidelines",
            "When reviewing candidates, please consider:",
            "- **Quality**: Is the CLAUDE.md comprehensive and well-structured?",
            "- **Uniqueness**: Does it demonstrate patterns not already in our collection?",
            "- **Maintainability**: Is the repository actively maintained?",
            "- **Licensing**: Does it have an appropriate open source license?",
            "- **Category Fit**: Is the suggested category appropriate?",
            "",
            "**Next Steps**: Review the candidates and create PRs for those that should be added to the collection."
        ]
        return "\n".join(guidelines)
