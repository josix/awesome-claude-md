"""Tests for the ClaudeFileDiscovery orchestrator."""

from unittest.mock import Mock, patch

import pytest

from scripts.discovery.orchestrator import ClaudeFileDiscovery


class TestClaudeFileDiscovery:
    """Test the ClaudeFileDiscovery orchestrator."""

    @pytest.fixture
    def discovery(self):
        return ClaudeFileDiscovery("dummy_token")

    def test_init(self, discovery):
        """Test initialization of ClaudeFileDiscovery."""
        assert discovery.repo_loader is not None
        assert discovery.github_searcher is not None
        assert discovery.evaluator is not None
        assert discovery.issue_generator is not None
        assert discovery.existing_repos is not None

    def test_discover_new_repositories_no_candidates(self, discovery):
        """Test discovery workflow with no candidates."""
        with patch.object(discovery.github_searcher, 'search_github_repos', return_value=[]):
            with patch.object(discovery.evaluator, 'evaluate_candidate', return_value=None):
                with patch.object(discovery.issue_generator, 'create_discovery_issue', return_value=None):
                    result = discovery.discover_new_repositories()
                    assert result == []

    def test_discover_new_repositories_with_candidates(self, discovery):
        """Test discovery workflow with candidates."""
        mock_candidate = {
            'full_name': 'test/repo',
            'name': 'repo',
            'owner': 'test',
            'stars': 100,
            'html_url': 'https://github.com/test/repo',
            'claude_file_path': 'claude.md'
        }

        mock_evaluation = {
            'candidate': mock_candidate,
            'score': 5,
            'reasons': ['Test reason'],
            'suggested_category': 'test-category'
        }

        with patch.object(discovery.github_searcher, 'search_github_repos', return_value=[mock_candidate]):
            with patch.object(discovery.evaluator, 'evaluate_candidate', return_value=mock_evaluation):
                with patch.object(discovery.issue_generator, 'create_discovery_issue', return_value=None):
                    result = discovery.discover_new_repositories()
                    assert len(result) == 1
                    assert result[0]['score'] == 5

    def test_discover_new_repositories_with_failed_evaluation(self, discovery):
        """Test discovery workflow with failed evaluation."""
        mock_candidate = {
            'full_name': 'test/repo',
            'name': 'repo',
            'owner': 'test',
            'stars': 100,
            'html_url': 'https://github.com/test/repo',
            'claude_file_path': 'claude.md'
        }

        with patch.object(discovery.github_searcher, 'search_github_repos', return_value=[mock_candidate]):
            with patch.object(discovery.evaluator, 'evaluate_candidate', return_value=None):  # Failed evaluation
                with patch.object(discovery.issue_generator, 'create_discovery_issue', return_value=None):
                    result = discovery.discover_new_repositories()
                    assert result == []

    def test_discover_new_repositories_multiple_candidates(self, discovery):
        """Test discovery workflow with multiple candidates."""
        mock_candidates = [
            {
                'full_name': 'test/repo1',
                'name': 'repo1',
                'owner': 'test',
                'stars': 100,
                'html_url': 'https://github.com/test/repo1',
                'claude_file_path': 'claude.md'
            },
            {
                'full_name': 'test/repo2',
                'name': 'repo2',
                'owner': 'test',
                'stars': 200,
                'html_url': 'https://github.com/test/repo2',
                'claude_file_path': 'CLAUDE.md'
            }
        ]

        mock_evaluations = [
            {
                'candidate': mock_candidates[0],
                'score': 5,
                'reasons': ['Test reason 1'],
                'suggested_category': 'test-category'
            },
            {
                'candidate': mock_candidates[1],
                'score': 7,
                'reasons': ['Test reason 2'],
                'suggested_category': 'test-category'
            }
        ]

        with patch.object(discovery.github_searcher, 'search_github_repos', return_value=mock_candidates):
            with patch.object(discovery.evaluator, 'evaluate_candidate', side_effect=mock_evaluations):
                with patch.object(discovery.issue_generator, 'create_discovery_issue', return_value=None) as mock_issue:
                    result = discovery.discover_new_repositories()
                    assert len(result) == 2
                    assert result[0]['score'] == 5
                    assert result[1]['score'] == 7
                    mock_issue.assert_called_once_with(result)