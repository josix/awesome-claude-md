"""Tests for the ClaudeToolDiscovery orchestrator."""

from unittest.mock import patch

import pytest

from scripts.tool_discovery.orchestrator import ClaudeToolDiscovery


class TestClaudeToolDiscovery:
    """Test the ClaudeToolDiscovery orchestrator."""

    @pytest.fixture
    def discovery(self):
        return ClaudeToolDiscovery("dummy_token")

    def test_init(self, discovery):
        """Test initialization of ClaudeToolDiscovery."""
        assert discovery.tool_loader is not None
        assert discovery.tool_searcher is not None
        assert discovery.evaluator is not None
        assert discovery.issue_generator is not None
        assert discovery.existing_tools is not None

    def test_discover_new_tools_no_candidates(self, discovery):
        """Test discovery workflow with no candidates."""
        with patch.object(
            discovery.tool_searcher, "search_github_repos", return_value=[]
        ):
            with patch.object(
                discovery.evaluator, "evaluate_candidate", return_value=None
            ):
                with patch.object(
                    discovery.issue_generator,
                    "create_discovery_issue",
                    return_value=None,
                ):
                    result = discovery.discover_new_tools()
                    assert result == []

    def test_discover_new_tools_with_candidates(self, discovery):
        """Test discovery workflow with candidates."""
        mock_candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 150,
            "html_url": "https://github.com/owner/tool",
            "license": "MIT",
        }

        mock_evaluation = {
            "candidate": mock_candidate,
            "score": 60,
            "tool_type": "cli",
            "reasons": ["Active project"],
            "suggested_category": "developer-tooling",
        }

        with patch.object(
            discovery.tool_searcher,
            "search_github_repos",
            return_value=[mock_candidate],
        ):
            with patch.object(
                discovery.evaluator, "evaluate_candidate", return_value=mock_evaluation
            ):
                with patch.object(
                    discovery.issue_generator,
                    "create_discovery_issue",
                    return_value=None,
                ):
                    result = discovery.discover_new_tools()
                    assert len(result) == 1
                    assert result[0]["score"] == 60

    def test_discover_new_tools_threshold_filtering(self, discovery):
        """Test that candidates below 50 points are filtered out."""
        mock_candidate = {
            "full_name": "owner/low-quality-tool",
            "name": "low-quality-tool",
            "owner": "owner",
            "stars": 5,
            "html_url": "https://github.com/owner/low-quality-tool",
            "license": "MIT",
        }

        mock_evaluation = {
            "candidate": mock_candidate,
            "score": 30,  # Below threshold of 50
            "tool_type": "unknown",
            "reasons": ["Low quality"],
            "suggested_category": "developer-tooling",
        }

        with patch.object(
            discovery.tool_searcher,
            "search_github_repos",
            return_value=[mock_candidate],
        ):
            with patch.object(
                discovery.evaluator, "evaluate_candidate", return_value=mock_evaluation
            ):
                with patch.object(
                    discovery.issue_generator,
                    "create_discovery_issue",
                    return_value=None,
                ) as mock_issue:
                    result = discovery.discover_new_tools()
                    # Below-threshold candidates should be filtered
                    assert len(result) == 0
                    # Issue should not be created for empty results
                    mock_issue.assert_not_called()

    def test_discover_new_tools_with_failed_evaluation(self, discovery):
        """Test discovery workflow with failed evaluation."""
        mock_candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://github.com/owner/tool",
            "license": "MIT",
        }

        with patch.object(
            discovery.tool_searcher,
            "search_github_repos",
            return_value=[mock_candidate],
        ):
            with patch.object(
                discovery.evaluator, "evaluate_candidate", return_value=None
            ):
                with patch.object(
                    discovery.issue_generator,
                    "create_discovery_issue",
                    return_value=None,
                ):
                    result = discovery.discover_new_tools()
                    assert result == []

    def test_discover_new_tools_multiple_candidates(self, discovery):
        """Test discovery workflow with multiple candidates."""
        mock_candidates = [
            {
                "full_name": "owner/tool-a",
                "name": "tool-a",
                "owner": "owner",
                "stars": 300,
                "html_url": "https://github.com/owner/tool-a",
                "license": "MIT",
            },
            {
                "full_name": "owner/tool-b",
                "name": "tool-b",
                "owner": "owner",
                "stars": 150,
                "html_url": "https://github.com/owner/tool-b",
                "license": "Apache-2.0",
            },
        ]

        mock_evaluations = [
            {
                "candidate": mock_candidates[0],
                "score": 80,
                "tool_type": "cli",
                "reasons": ["High quality"],
                "suggested_category": "developer-tooling",
            },
            {
                "candidate": mock_candidates[1],
                "score": 65,
                "tool_type": "library",
                "reasons": ["Good docs"],
                "suggested_category": "developer-tooling",
            },
        ]

        with patch.object(
            discovery.tool_searcher,
            "search_github_repos",
            return_value=mock_candidates,
        ):
            with patch.object(
                discovery.evaluator,
                "evaluate_candidate",
                side_effect=mock_evaluations,
            ):
                with patch.object(
                    discovery.issue_generator,
                    "create_discovery_issue",
                    return_value=None,
                ) as mock_issue:
                    result = discovery.discover_new_tools()
                    assert len(result) == 2
                    assert result[0]["score"] == 80
                    assert result[1]["score"] == 65
                    mock_issue.assert_called_once_with(result)
