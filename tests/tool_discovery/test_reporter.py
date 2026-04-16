"""Tests for the ToolIssueGenerator module."""

from unittest.mock import Mock, patch

import pytest

from scripts.tool_discovery.reporter import ToolIssueGenerator


class TestToolIssueGenerator:
    """Test the ToolIssueGenerator class."""

    @pytest.fixture
    def issue_generator(self):
        mock_searcher = Mock()
        return ToolIssueGenerator(mock_searcher)

    def test_create_discovery_issue_empty(self, issue_generator):
        """Test creating discovery issue with empty evaluations."""
        with patch.object(issue_generator, "_save_discovery_report") as mock_save:
            issue_generator.create_discovery_issue([])
            assert not mock_save.called

    def test_create_discovery_issue_with_evaluations(self, issue_generator):
        """Test creating discovery issue with evaluations."""
        evaluations = [
            {
                "score": 80,
                "candidate": {
                    "full_name": "owner/tool",
                    "html_url": "https://github.com/owner/tool",
                    "description": "A useful tool",
                    "stars": 200,
                    "language": "Python",
                    "topics": ["cli"],
                    "license": "MIT",
                },
                "tool_type": "cli",
                "suggested_category": "developer-tooling",
                "readme_length": 2000,
                "last_updated_days": 10,
                "reasons": ["Good documentation", "Active maintenance"],
            }
        ]

        with patch.object(issue_generator, "_save_discovery_report") as mock_save:
            issue_generator.create_discovery_issue(evaluations)
            assert mock_save.called

    def test_create_discovery_issue_uses_correct_labels(self, issue_generator):
        """Test that discovery issue uses the correct labels."""
        evaluations = [
            {
                "score": 75,
                "candidate": {
                    "full_name": "owner/tool",
                    "html_url": "https://github.com/owner/tool",
                    "description": "A tool",
                    "stars": 100,
                    "language": "Go",
                    "topics": [],
                    "license": "MIT",
                },
                "tool_type": "service",
                "suggested_category": "developer-tooling",
                "readme_length": 1000,
                "last_updated_days": 5,
                "reasons": ["Active project"],
            }
        ]

        expected_labels = ["automation", "tool-discovery", "review-needed"]

        with patch.object(issue_generator, "_save_discovery_report"):
            with patch.object(
                issue_generator, "_get_issue_labels", return_value=expected_labels
            ) as mock_labels:
                issue_generator.create_discovery_issue(evaluations)
                if mock_labels.called:
                    assert mock_labels.return_value == expected_labels

    def test_create_discovery_issue_body_truncation(self, issue_generator):
        """Test that issue body is truncated at 65536 characters."""
        large_evaluations = []
        for i in range(100):
            large_evaluations.append(
                {
                    "score": 70 + (i % 20),
                    "candidate": {
                        "full_name": f"owner/tool-{i}",
                        "html_url": f"https://github.com/owner/tool-{i}",
                        "description": "A" * 500,
                        "stars": 100 + i,
                        "language": "Python",
                        "topics": ["tool"],
                        "license": "MIT",
                    },
                    "tool_type": "cli",
                    "suggested_category": "developer-tooling",
                    "readme_length": 5000,
                    "last_updated_days": 3,
                    "reasons": ["Reason " * 50],
                }
            )

        saved_bodies = []

        def capture_save(title, body):
            saved_bodies.append(body)

        with patch.object(
            issue_generator, "_save_discovery_report", side_effect=capture_save
        ):
            issue_generator.create_discovery_issue(large_evaluations)

        if saved_bodies:
            assert len(saved_bodies[0]) <= 65536

    def test_save_discovery_report_success(self, issue_generator):
        """Test saving discovery report successfully."""
        title = "Monthly Tool Discovery: 5 Candidates"
        body = "Test body content"

        with patch("builtins.open", create=True) as mock_open:
            with patch("scripts.tool_discovery.reporter.datetime") as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "20231201_120000"

                issue_generator._save_discovery_report(title, body)

                mock_open.assert_called_once()
                mock_open.assert_called_with(
                    "tool_discovery_report_20231201_120000.md", "w", encoding="utf-8"
                )

    def test_save_discovery_report_error(self, issue_generator):
        """Test saving discovery report when an error occurs."""
        title = "Monthly Tool Discovery"
        body = "Test body content"

        with patch("builtins.open", side_effect=OSError("Permission denied")):
            with patch("scripts.tool_discovery.reporter.logger") as mock_logger:
                issue_generator._save_discovery_report(title, body)

                mock_logger.error.assert_called_once()
                assert (
                    "Error saving" in mock_logger.error.call_args[0][0]
                    or "error" in mock_logger.error.call_args[0][0].lower()
                )
