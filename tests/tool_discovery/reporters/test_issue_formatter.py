"""Tests for the ToolIssueFormatter module."""

import pytest

from scripts.tool_discovery.reporters.issue_formatter import ToolIssueFormatter


class TestToolIssueFormatter:
    """Test the ToolIssueFormatter class."""

    @pytest.fixture
    def issue_formatter(self):
        return ToolIssueFormatter()

    def test_init(self, issue_formatter):
        """Test initialization of ToolIssueFormatter."""
        assert issue_formatter.priority_grouper is not None
        assert issue_formatter.summary_generator is not None

    def test_create_issue_title_empty(self, issue_formatter):
        """Test creating issue title with no evaluations."""
        title = issue_formatter.create_issue_title([])

        assert "Monthly Tool Discovery" in title
        assert "0" in title

    def test_create_issue_title_format(self, issue_formatter):
        """Test that issue title follows expected format."""
        evaluations = [{"score": 70}, {"score": 55}]
        title = issue_formatter.create_issue_title(evaluations)

        assert "Monthly Tool Discovery" in title
        assert "2" in title

    def test_create_issue_title_with_exceptional_priority(self, issue_formatter):
        """Test creating issue title with exceptional priority candidates."""
        evaluations = [
            {"score": 85},  # exceptional
            {"score": 72},  # high
            {"score": 90},  # exceptional
        ]

        title = issue_formatter.create_issue_title(evaluations)

        assert "Monthly Tool Discovery" in title
        assert "3" in title
        assert "Exceptional" in title or "exceptional" in title.lower()

    def test_create_issue_title_no_exceptional(self, issue_formatter):
        """Test creating issue title when no exceptional candidates exist."""
        evaluations = [
            {"score": 72},  # high
            {"score": 60},  # good
        ]

        title = issue_formatter.create_issue_title(evaluations)

        assert "Monthly Tool Discovery" in title
        assert "Exceptional" not in title

    def test_create_issue_body_empty(self, issue_formatter):
        """Test creating issue body with empty evaluations."""
        body = issue_formatter.create_issue_body([])

        assert body == "No new tool candidates found in this discovery run."

    def test_create_issue_body_with_evaluations(self, issue_formatter):
        """Test creating issue body with evaluations."""
        evaluations = [
            {
                "score": 80,
                "candidate": {
                    "full_name": "owner/cli-tool",
                    "html_url": "https://github.com/owner/cli-tool",
                    "description": "A powerful CLI tool",
                    "stars": 500,
                    "language": "Python",
                    "topics": ["cli", "automation"],
                    "license": "MIT",
                },
                "tool_type": "cli",
                "suggested_category": "developer-tooling",
                "readme_length": 3000,
                "last_updated_days": 7,
                "reasons": ["Active maintenance", "Good documentation"],
            },
            {
                "score": 65,
                "candidate": {
                    "full_name": "owner/lib-tool",
                    "html_url": "https://github.com/owner/lib-tool",
                    "description": "A useful library",
                    "stars": 150,
                    "language": "TypeScript",
                    "topics": ["library"],
                    "license": "Apache-2.0",
                },
                "tool_type": "library",
                "suggested_category": "developer-tooling",
                "readme_length": 1500,
                "last_updated_days": 20,
                "reasons": ["Clear documentation"],
            },
        ]

        body = issue_formatter.create_issue_body(evaluations)

        # Check summary section
        assert "Discovery Summary" in body
        assert "Total Candidates" in body
        assert "2" in body

        # Check candidate content
        assert "owner/cli-tool" in body
        assert "owner/lib-tool" in body

        # Check tool-specific fields
        assert "tool_type" in body.lower() or "Tool Type" in body or "cli" in body

        # Check license information
        assert "MIT" in body or "Apache-2.0" in body or "License" in body

        # Check guidelines section
        assert "Review Guidelines" in body or "Guidelines" in body

    def test_create_issue_body_includes_tool_type(self, issue_formatter):
        """Test that issue body includes tool_type for each candidate."""
        evaluations = [
            {
                "score": 75,
                "candidate": {
                    "full_name": "owner/plugin-tool",
                    "html_url": "https://github.com/owner/plugin-tool",
                    "description": "A plugin",
                    "stars": 200,
                    "language": "JavaScript",
                    "topics": ["plugin"],
                    "license": "MIT",
                },
                "tool_type": "plugin",
                "suggested_category": "developer-tooling",
                "readme_length": 2000,
                "last_updated_days": 5,
                "reasons": ["Popular plugin"],
            }
        ]

        body = issue_formatter.create_issue_body(evaluations)

        assert "plugin" in body

    def test_create_issue_body_includes_license(self, issue_formatter):
        """Test that issue body includes license information."""
        evaluations = [
            {
                "score": 70,
                "candidate": {
                    "full_name": "owner/tool",
                    "html_url": "https://github.com/owner/tool",
                    "description": "A tool",
                    "stars": 100,
                    "language": "Go",
                    "topics": [],
                    "license": "Apache-2.0",
                },
                "tool_type": "service",
                "suggested_category": "developer-tooling",
                "readme_length": 1000,
                "last_updated_days": 15,
                "reasons": ["Open source"],
            }
        ]

        body = issue_formatter.create_issue_body(evaluations)

        assert "Apache-2.0" in body or "License" in body

    def test_create_issue_body_only_below_threshold(self, issue_formatter):
        """Test creating issue body with only below-threshold evaluations."""
        evaluations = [
            {
                "score": 40,
                "candidate": {
                    "full_name": "owner/weak-tool",
                    "html_url": "https://github.com/owner/weak-tool",
                    "description": "Minimal tool",
                    "stars": 10,
                    "language": "Python",
                    "topics": [],
                    "license": "MIT",
                },
                "tool_type": "cli",
                "suggested_category": "developer-tooling",
                "readme_length": 200,
                "last_updated_days": 365,
                "reasons": ["Minimal docs"],
            }
        ]

        body = issue_formatter.create_issue_body(evaluations)

        assert "owner/weak-tool" in body
        assert "40" in body

    def test_create_issue_body_mixed_priorities(self, issue_formatter):
        """Test creating issue body with mixed priority evaluations."""
        evaluations = []
        scores = [90, 75, 63, 88, 45]
        tool_types = ["cli", "plugin", "library", "service", "cli"]

        for i, (score, tool_type) in enumerate(zip(scores, tool_types, strict=False)):
            evaluations.append(
                {
                    "score": score,
                    "candidate": {
                        "full_name": f"owner/tool-{i}",
                        "html_url": f"https://github.com/owner/tool-{i}",
                        "description": f"Tool {i}",
                        "stars": score * 5,
                        "language": "Python",
                        "topics": [tool_type],
                        "license": "MIT",
                    },
                    "tool_type": tool_type,
                    "suggested_category": "developer-tooling",
                    "readme_length": 1000,
                    "last_updated_days": 10,
                    "reasons": [f"Reason for tool {i}"],
                }
            )

        body = issue_formatter.create_issue_body(evaluations)

        assert "Total Candidates" in body
        for i in range(len(scores)):
            assert f"owner/tool-{i}" in body
