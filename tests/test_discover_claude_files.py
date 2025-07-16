#!/usr/bin/env python3
"""
Basic unit tests for the CLAUDE.md discovery script.
"""
import pytest
import time
from unittest.mock import Mock, patch
import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.discover_claude_files import ClaudeFileDiscovery, RepositoryLoader, GitHubSearcher, RepositoryEvaluator, IssueGenerator


@pytest.fixture
def discovery():
    """Set up test fixture for ClaudeFileDiscovery."""
    # Use a dummy token for testing (methods being tested don't need a valid token)
    return ClaudeFileDiscovery("dummy_token")


@pytest.fixture
def repo_loader():
    """Set up test fixture for RepositoryLoader."""
    return RepositoryLoader()


@pytest.fixture
def github_searcher():
    """Set up test fixture for GitHubSearcher."""
    return GitHubSearcher("dummy_token")


@pytest.fixture
def evaluator(github_searcher):
    """Set up test fixture for RepositoryEvaluator."""
    return RepositoryEvaluator(github_searcher)


@pytest.fixture
def issue_generator(github_searcher):
    """Set up test fixture for IssueGenerator."""
    return IssueGenerator(github_searcher)


@pytest.mark.parametrize("repo_name", [
    "owner/repo",
    "microsoft/typescript",
    "pytorch/pytorch",
    "owner/repo-name",
    "owner/repo_name",
    "owner/repo.name"
])
def test_validate_repo_name_valid(repo_loader, repo_name):
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
def test_validate_repo_name_invalid(repo_loader, repo_name):
    """Test repository name validation with invalid names."""
    assert not repo_loader._validate_repo_name(repo_name), f"Expected {repo_name} to be invalid"


def test_validate_candidate_valid(evaluator):
    """Test candidate validation with valid candidate."""
    valid_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        'owner': 'owner',
        'stars': 100,
        'html_url': 'https://github.com/owner/repo',
        'claude_file_path': 'CLAUDE.md'
    }
    
    assert evaluator._validate_candidate(valid_candidate)


def test_validate_candidate_missing_fields(evaluator):
    """Test candidate validation with missing required fields."""
    incomplete_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        # Missing other required fields
    }
    
    assert not evaluator._validate_candidate(incomplete_candidate)


def test_validate_candidate_invalid_types(evaluator):
    """Test candidate validation with invalid data types."""
    invalid_candidate = {
        'full_name': 'owner/repo',
        'name': 'repo',
        'owner': 'owner',
        'stars': 'not-a-number',  # Should be int
        'html_url': 'https://github.com/owner/repo',
        'claude_file_path': 'CLAUDE.md'
    }
    
    assert not evaluator._validate_candidate(invalid_candidate)


@pytest.mark.parametrize("input_text,expected", [
    ("normal text", "normal text"),
    ("<script>alert('xss')</script>", "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"),
    ("", ""),
    ("a" * 600, "a" * 500 + "..."),  # Test length limiting
])
def test_sanitize_text_basic(issue_generator, input_text, expected):
    """Test text sanitization with basic input."""
    result = issue_generator._sanitize_text(input_text)
    assert result == expected


@pytest.mark.parametrize("input_value", [None, 123])
def test_sanitize_text_non_string(issue_generator, input_value):
    """Test text sanitization with non-string input."""
    result = issue_generator._sanitize_text(input_value)
    assert result == ""


def test_suggest_category_complex_project(evaluator):
    """Test category suggestion logic for complex project."""
    complex_content = """
    # Architecture
    
    This is a multi-service application with microservices.
    
    ## Development Commands
    
    - npm run dev
    - docker-compose up
    """
    
    dummy_candidate = {
        'description': 'Enterprise platform with microservices architecture',
        'topics': ['microservices', 'platform'],
        'language': 'Java'
    }
    
    result = evaluator._suggest_category(dummy_candidate, complex_content)
    assert result == 'complex-projects'


def test_suggest_category_library_framework(evaluator):
    """Test category suggestion for library/framework."""
    library_content = """
    # API Documentation
    
    This is a utility library for developers.
    """
    
    dummy_candidate = {
        'description': 'Utility library for React components',
        'topics': ['library', 'react'],
        'language': 'JavaScript'
    }
    
    result = evaluator._suggest_category(dummy_candidate, library_content)
    assert result == 'libraries-frameworks'


def test_suggest_category_developer_tooling(evaluator):
    """Test category suggestion for developer tooling."""
    tooling_content = """
    # CLI Tool
    
    This is a command line interface for automation.
    """
    
    dummy_candidate = {
        'description': 'CLI tool for build automation',
        'topics': ['cli', 'automation'],
        'language': 'Python'
    }
    
    result = evaluator._suggest_category(dummy_candidate, tooling_content)
    assert result == 'developer-tooling'


def test_suggest_category_getting_started(evaluator):
    """Test category suggestion for getting started projects."""
    tutorial_content = """
    # Tutorial
    
    This is a starter template for beginners.
    """
    
    dummy_candidate = {
        'description': 'Beginner tutorial and examples',
        'topics': ['tutorial', 'example'],
        'language': 'TypeScript'
    }
    
    result = evaluator._suggest_category(dummy_candidate, tutorial_content)
    assert result == 'getting-started'


def test_suggest_category_default_fallback(evaluator):
    """Test category suggestion default fallback."""
    generic_content = "Generic project description"
    
    dummy_candidate = {
        'description': 'Some generic project',
        'topics': [],
        'language': 'Go'  # Known language
    }
    
    result = evaluator._suggest_category(dummy_candidate, generic_content)
    assert result == 'libraries-frameworks'  # Default for known language


def test_integration_workflow(discovery):
    """Test the complete discovery workflow without external API calls."""
    # Mock the component methods to test the workflow
    with patch.object(discovery.github_searcher, 'search_github_repos', return_value=[]):
        with patch.object(discovery.evaluator, 'evaluate_candidate', return_value=None):
            with patch.object(discovery.issue_generator, 'create_discovery_issue', return_value=None):
                result = discovery.discover_new_repositories()
                assert result == []


def test_integration_workflow_with_candidates(discovery):
    """Test the discovery workflow with mock candidates."""
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


def test_integration_empty_scenarios_directory(discovery):
    """Test loading existing repos when scenarios directory doesn't exist."""
    # Mock the scenarios directory to not exist
    with patch('pathlib.Path.exists', return_value=False):
        existing_repos = discovery.repo_loader.load_existing_repos()
        assert len(existing_repos) == 0


def test_integration_rate_limiting(github_searcher):
    """Test rate limiting handling."""
    mock_response = Mock()
    mock_response.headers = {
        'X-RateLimit-Remaining': '5',
        'X-RateLimit-Reset': str(int(time.time()) + 60)
    }
    
    with patch('time.sleep') as mock_sleep:
        github_searcher._handle_rate_limiting(mock_response)
        # Should sleep when remaining is low
        assert mock_sleep.called


def test_integration_error_handling(evaluator):
    """Test error handling in evaluation."""
    invalid_candidate = {
        'full_name': 'invalid/repo',
        # Missing required fields
    }
    
    result = evaluator.evaluate_candidate(invalid_candidate)
    assert result is None


def test_integration_discovery_report_generation(issue_generator):
    """Test discovery report generation."""
    mock_evaluations = [
        {
            'candidate': {
                'full_name': 'test/repo',
                'html_url': 'https://github.com/test/repo',
                'description': 'Test repo',
                'stars': 100,
                'language': 'Python',
                'topics': ['test'],
                'claude_file_path': 'claude.md'
            },
            'score': 8,
            'reasons': ['High quality'],
            'suggested_category': 'test-category',
            'claude_content_length': 1000,
            'last_updated_days': 5
        }
    ]
    
    with patch('builtins.open', create=True) as mock_open:
        with patch.object(issue_generator, '_save_discovery_report', return_value=None):
            issue_generator.create_discovery_issue(mock_evaluations)
            # Should not raise any exceptions
            assert True