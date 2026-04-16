"""Tests for the ToolSearcher module."""

from unittest.mock import Mock, patch

import pytest

from scripts.tool_discovery.searcher import ToolSearcher


class TestToolSearcher:
    """Test the ToolSearcher class."""

    @pytest.fixture
    def tool_searcher(self):
        return ToolSearcher("dummy_token")

    def test_search_github_repos_returns_list(self, tool_searcher):
        """Test that search_github_repos returns a list."""
        with patch.object(tool_searcher, "_run_search_query", return_value=[]):
            result = tool_searcher.search_github_repos(set())
            assert isinstance(result, list)

    def test_search_github_repos_filters_existing(self, tool_searcher):
        """Test that search deduplicates against existing tools."""
        existing_tools = {"owner/existing-tool"}

        mock_candidate = {
            "full_name": "owner/existing-tool",
            "name": "existing-tool",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://github.com/owner/existing-tool",
        }

        with patch.object(
            tool_searcher, "_run_search_query", return_value=[mock_candidate]
        ):
            result = tool_searcher.search_github_repos(existing_tools)
            # Should filter out existing tool
            assert not any(c["full_name"] == "owner/existing-tool" for c in result)

    def test_search_github_repos_filters_archived(self, tool_searcher):
        """Test that archived repos are filtered out."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/archived-tool"
        mock_repo.archived = True
        mock_repo.fork = False

        result = tool_searcher._process_single_repo(mock_repo, set())
        assert result is None

    def test_search_github_repos_filters_forks(self, tool_searcher):
        """Test that forked repos are filtered out."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/forked-tool"
        mock_repo.archived = False
        mock_repo.fork = True

        result = tool_searcher._process_single_repo(mock_repo, set())
        assert result is None

    def test_process_single_repo_existing(self, tool_searcher):
        """Test processing a repo that already exists."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/existing-tool"

        existing_tools = {"owner/existing-tool"}

        result = tool_searcher._process_single_repo(mock_repo, existing_tools)
        assert result is None

    def test_process_single_repo_valid(self, tool_searcher):
        """Test processing a valid new repo."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/new-tool"
        mock_repo.archived = False
        mock_repo.fork = False
        mock_repo.stargazers_count = 50

        tool_searcher._create_candidate_dict = Mock(
            return_value={"full_name": "owner/new-tool"}
        )

        result = tool_searcher._process_single_repo(mock_repo, set())
        assert result == {"full_name": "owner/new-tool"}

    def test_create_candidate_dict_structure(self, tool_searcher):
        """Test that candidate dict has expected structure."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/tool"
        mock_repo.name = "tool"
        mock_repo.owner.login = "owner"
        mock_repo.description = "A useful tool"
        mock_repo.stargazers_count = 200
        mock_repo.forks_count = 20
        mock_repo.language = "Python"
        mock_repo.get_topics.return_value = ["cli", "automation"]
        mock_repo.html_url = "https://github.com/owner/tool"
        mock_repo.created_at.isoformat.return_value = "2023-01-01T00:00:00Z"
        mock_repo.updated_at.isoformat.return_value = "2023-12-01T00:00:00Z"
        mock_repo.organization = None
        mock_repo.license = Mock()
        mock_repo.license.spdx_id = "MIT"

        result = tool_searcher._create_candidate_dict(mock_repo)

        assert result["full_name"] == "owner/tool"
        assert result["name"] == "tool"
        assert result["owner"] == "owner"
        assert result["stars"] == 200
        assert result["language"] == "Python"
        assert result["html_url"] == "https://github.com/owner/tool"

    def test_create_candidate_dict_no_license(self, tool_searcher):
        """Test candidate dict with no license."""
        mock_repo = Mock()
        mock_repo.full_name = "owner/tool"
        mock_repo.name = "tool"
        mock_repo.owner.login = "owner"
        mock_repo.description = "A tool"
        mock_repo.stargazers_count = 10
        mock_repo.forks_count = 1
        mock_repo.language = "Go"
        mock_repo.get_topics.return_value = []
        mock_repo.html_url = "https://github.com/owner/tool"
        mock_repo.created_at.isoformat.return_value = "2023-01-01T00:00:00Z"
        mock_repo.updated_at.isoformat.return_value = "2023-12-01T00:00:00Z"
        mock_repo.organization = None
        mock_repo.license = None

        result = tool_searcher._create_candidate_dict(mock_repo)

        assert result["full_name"] == "owner/tool"
        # License should be None or empty when not present
        assert result.get("license") is None or result.get("license") == ""
