"""Tests for the GitHubSearcher module."""

import time
from unittest.mock import Mock, patch

import pytest

from scripts.discovery.searcher import GitHubSearcher


class TestGitHubSearcher:
    """Test the GitHubSearcher class."""

    @pytest.fixture
    def github_searcher(self):
        return GitHubSearcher("dummy_token")

    def test_handle_rate_limiting_low_remaining(self, github_searcher):
        """Test rate limiting handling when remaining is low."""
        mock_response = Mock()
        mock_response.headers = {
            'X-RateLimit-Remaining': '5',
            'X-RateLimit-Reset': str(int(time.time()) + 60)
        }

        with patch('time.sleep') as mock_sleep:
            github_searcher._handle_rate_limiting(mock_response)
            assert mock_sleep.called

    def test_handle_rate_limiting_high_remaining(self, github_searcher):
        """Test rate limiting handling when remaining is high."""
        mock_response = Mock()
        mock_response.headers = {
            'X-RateLimit-Remaining': '50',
            'X-RateLimit-Reset': str(int(time.time()) + 60)
        }

        with patch('time.sleep') as mock_sleep:
            github_searcher._handle_rate_limiting(mock_response)
            assert not mock_sleep.called

    def test_create_candidate_dict(self, github_searcher):
        """Test creating candidate dictionary."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_repo.name = "repo"
        mock_repo.owner.login = "owner"
        mock_repo.description = "Test repository"
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 10
        mock_repo.language = "Python"
        mock_repo.get_topics.return_value = ["test", "python"]
        mock_repo.html_url = "https://github.com/owner/repo"
        mock_repo.created_at.isoformat.return_value = "2023-01-01T00:00:00Z"
        mock_repo.updated_at.isoformat.return_value = "2023-12-01T00:00:00Z"
        mock_repo.organization = None

        result = github_searcher._create_candidate_dict(mock_repo, "claude.md")

        assert result['full_name'] == "owner/repo"
        assert result['stars'] == 100
        assert result['claude_file_path'] == "claude.md"
        assert result['organization'] is None

    def test_process_single_repository_existing_repo(self, github_searcher):
        """Test processing a repository that already exists."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"

        existing_repos = {"owner/repo"}

        result = github_searcher._process_single_repository(mock_repo, existing_repos)
        assert result is None

    def test_process_single_repository_archived(self, github_searcher):
        """Test processing an archived repository."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_repo.archived = True
        mock_repo.fork = False

        existing_repos = set()

        result = github_searcher._process_single_repository(mock_repo, existing_repos)
        assert result is None

    def test_process_single_repository_low_stars(self, github_searcher):
        """Test processing a repository with low stars."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/repo"
        mock_repo.archived = False
        mock_repo.fork = False
        mock_repo.stargazers_count = 10  # Below minimum

        existing_repos = set()

        result = github_searcher._process_single_repository(mock_repo, existing_repos)
        assert result is None

    def test_find_claude_file_found(self, github_searcher):
        """Test finding CLAUDE.md file in repository."""
        mock_repo = Mock()
        mock_file_contents = Mock()
        mock_file_contents.size = 1000  # Above minimum

        mock_repo.get_contents.return_value = mock_file_contents

        result = github_searcher._find_claude_file(mock_repo)
        assert result == "claude.md"

    def test_find_claude_file_too_small(self, github_searcher):
        """Test finding CLAUDE.md file that is too small."""
        mock_repo = Mock()
        mock_file_contents = Mock()
        mock_file_contents.size = 100  # Below minimum

        mock_repo.get_contents.return_value = mock_file_contents

        result = github_searcher._find_claude_file(mock_repo)
        assert result is None

    def test_find_claude_file_not_found(self, github_searcher):
        """Test when CLAUDE.md file is not found."""
        from github.GithubException import UnknownObjectException

        mock_repo = Mock()
        mock_repo.get_contents.side_effect = UnknownObjectException(404, "Not Found", headers={})

        result = github_searcher._find_claude_file(mock_repo)
        assert result is None
