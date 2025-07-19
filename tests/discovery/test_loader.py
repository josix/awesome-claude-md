"""Tests for the RepositoryLoader module."""

from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from scripts.discovery.loader import RepositoryLoader


class TestRepositoryLoader:
    """Test the RepositoryLoader class."""

    @pytest.fixture
    def repo_loader(self):
        return RepositoryLoader()

    @pytest.mark.parametrize("repo_name", [
        "owner/repo",
        "microsoft/typescript",
        "pytorch/pytorch",
        "owner/repo-name",
        "owner/repo_name",
        "owner/repo.name"
    ])
    def test_validate_repo_name_valid(self, repo_loader, repo_name):
        """Test repository name validation with valid names."""
        assert repo_loader._validate_repo_name(repo_name), f"Expected {repo_name} to be valid"

    @pytest.mark.parametrize("repo_name", [
        "",
        "just-owner",
        "owner/",
        "/repo",
        "owner/repo/extra",
        "owner//repo",
        "owner with spaces/repo",
        "-invalid-start/repo",
        "invalid-end-/repo",
        "a" * 40 + "/repo",  # Owner too long
        "owner/" + "a" * 101  # Repo too long
    ])
    def test_validate_repo_name_invalid(self, repo_loader, repo_name):
        """Test repository name validation with invalid names."""
        assert not repo_loader._validate_repo_name(repo_name), f"Expected {repo_name} to be invalid"

    def test_load_existing_repos_no_scenarios(self, repo_loader):
        """Test loading existing repos when scenarios directory doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            existing_repos = repo_loader.load_existing_repos()
            assert len(existing_repos) == 0

    def test_extract_repo_name_from_directory_name(self, repo_loader):
        """Test extracting repo name from directory name."""
        result = repo_loader._extract_repo_name_from_directory_name("owner_repo")
        assert result == "owner/repo"

    def test_extract_repo_name_from_directory_name_invalid(self, repo_loader):
        """Test extracting repo name from invalid directory name."""
        result = repo_loader._extract_repo_name_from_directory_name("invalid")
        assert result is None

    def test_extract_repo_name_from_analysis_file(self, repo_loader):
        """Test extracting repo name from analysis file."""
        mock_content = """
        **Repository**: [test-repo](https://github.com/owner/repo)
        **CLAUDE.md**: [CLAUDE.md](https://github.com/owner/repo/blob/main/CLAUDE.md)
        """

        mock_repo_dir = Path("scenarios/test-category/owner_repo")

        with patch("builtins.open", mock_open(read_data=mock_content)):
            with patch.object(Path, 'exists', return_value=True):
                result = repo_loader._extract_repo_name_from_analysis_file(mock_repo_dir)
                assert result == "owner/repo"

    def test_extract_repo_name_from_analysis_file_no_file(self, repo_loader):
        """Test extracting repo name when analysis file doesn't exist."""
        mock_repo_dir = Path("scenarios/test-category/owner_repo")

        with patch.object(Path, 'exists', return_value=False):
            result = repo_loader._extract_repo_name_from_analysis_file(mock_repo_dir)
            assert result is None
