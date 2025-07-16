#!/usr/bin/env python3
"""
Basic unit tests for the CLAUDE.md discovery script.
"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the script to the path
sys.path.insert(0, os.path.dirname(__file__))
from discover_claude_files import ClaudeFileDiscovery


@pytest.fixture
def discovery():
    """Set up test fixture for ClaudeFileDiscovery."""
    # Use a dummy token for testing (methods being tested don't need a valid token)
    return ClaudeFileDiscovery("dummy_token")


@pytest.mark.parametrize("repo_name", [
    "owner/repo",
    "microsoft/typescript",
    "pytorch/pytorch",
    "owner/repo-name",
    "owner/repo_name",
    "owner/repo.name"
])
def test_validate_repo_name_valid(discovery, repo_name):
    """Test repository name validation with valid names."""
    assert discovery._validate_repo_name(repo_name), f"Expected {repo_name} to be valid"


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
def test_validate_repo_name_invalid(discovery, repo_name):
    """Test repository name validation with invalid names."""
    assert not discovery._validate_repo_name(repo_name), f"Expected {repo_name} to be invalid"


def test_validate_candidate_valid(discovery):
    """Test candidate validation with valid candidate."""
    valid_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        'owner': 'owner',
        'stars': 100,
        'html_url': 'https://github.com/owner/repo',
        'claude_file_path': 'CLAUDE.md'
    }
    
    assert discovery._validate_candidate(valid_candidate)


def test_validate_candidate_missing_fields(discovery):
    """Test candidate validation with missing required fields."""
    incomplete_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        # Missing other required fields
    }
    
    assert not discovery._validate_candidate(incomplete_candidate)


def test_validate_candidate_invalid_types(discovery):
    """Test candidate validation with invalid data types."""
    invalid_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        'owner': 'owner',
        'stars': 'not-a-number',  # Should be int
        'html_url': 'https://github.com/owner/repo',
        'claude_file_path': 'CLAUDE.md'
    }
    
    assert not discovery._validate_candidate(invalid_candidate)


@pytest.mark.parametrize("input_text,expected", [
    ("normal text", "normal text"),
    ("<script>alert('xss')</script>", "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"),
    ("", ""),
    ("a" * 600, "a" * 500 + "..."),  # Test length limiting
])
def test_sanitize_text_basic(discovery, input_text, expected):
    """Test text sanitization with basic input."""
    result = discovery._sanitize_text(input_text)
    assert result == expected


@pytest.mark.parametrize("input_value", [None, 123])
def test_sanitize_text_non_string(discovery, input_value):
    """Test text sanitization with non-string input."""
    result = discovery._sanitize_text(input_value)
    assert result == ""


def test_suggest_category_complex_project(discovery):
    """Test category suggestion logic for complex project."""
    complex_content = """
    # Architecture
    
    This is a multi-service application with microservices.
    
    ## Development Commands
    
    - npm run dev
    - docker-compose up
    """
    
    dummy_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        'owner': 'owner',
        'stars': 100,
        'html_url': 'https://github.com/owner/repo',
        'claude_file_path': 'CLAUDE.md',
        'description': 'A test repository'
    }
    
    category = discovery._suggest_category(dummy_candidate, complex_content)
    assert category in ["complex-projects", "developer-tooling", "getting-started"]


def test_suggest_category_library(discovery):
    """Test category suggestion logic for library."""
    library_content = """
    # API Reference
    
    This library provides core functionality.
    
    ## Usage
    
    ```python
    import library
    ```
    """
    
    dummy_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        'owner': 'owner',
        'stars': 100,
        'html_url': 'https://github.com/owner/repo',
        'claude_file_path': 'CLAUDE.md',
        'description': 'A test repository'
    }
    
    category = discovery._suggest_category(dummy_candidate, library_content)
    # Should suggest an appropriate category
    assert isinstance(category, str)
    assert len(category) > 0