#!/usr/bin/env python3
"""
Integration tests for the CLAUDE.md discovery script.

These tests validate the complete workflow end-to-end.
"""
import pytest
import os
import tempfile
import shutil
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.discover_claude_files import ClaudeFileDiscovery
from github.GithubException import RateLimitExceededException, UnknownObjectException, GithubException


class TestClaudeFileDiscoveryIntegration:
    """Integration tests for the complete discovery workflow."""
    
    def setup_method(self):
        """Set up test environment for each test."""
        # Create temporary directory for test scenarios
        self.test_dir = tempfile.mkdtemp()
        self.scenarios_dir = Path(self.test_dir) / 'scenarios'
        self.scenarios_dir.mkdir(parents=True)
        
        # Create sample existing repository structure
        self._create_sample_scenarios()
        
        # Change to test directory
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
    def teardown_method(self):
        """Clean up after each test."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
        
    def _create_sample_scenarios(self):
        """Create sample scenario structure for testing."""
        # Create a sample category with existing repositories
        category_dir = self.scenarios_dir / 'complex-projects'
        category_dir.mkdir()
        
        # Create sample repository directory
        repo_dir = category_dir / 'microsoft_semanticworkbench'
        repo_dir.mkdir()
        
        # Create sample analysis.md file
        analysis_file = repo_dir / 'analysis.md'
        analysis_content = """# Analysis: Microsoft Semantic Workbench

**Category**: Complex Projects
**Repository**: [Microsoft Semantic Workbench](https://github.com/microsoft/semanticworkbench)
**License**: MIT License
**Stars**: 1200+

## Why it's exemplary

This CLAUDE.md file demonstrates comprehensive project documentation...
"""
        analysis_file.write_text(analysis_content)
        
    @patch('scripts.discover_claude_files.Github')
    @patch('requests.Session')
    def test_complete_discovery_workflow(self, mock_session, mock_github_class):
        """Test the complete discovery workflow from search to evaluation."""
        # Mock GitHub API responses
        mock_github = Mock()
        mock_github_class.return_value = mock_github
        
        # Mock search API results
        mock_search_result = Mock()
        mock_repo_item = Mock()
        mock_repo_item.full_name = 'test/new-repo'
        mock_repo_item.name = 'new-repo'
        mock_repo_item.owner.login = 'test'
        mock_repo_item.description = 'A test repository'
        mock_repo_item.stargazers_count = 100  # Make sure this is an int
        mock_repo_item.forks_count = 10
        mock_repo_item.language = 'Python'
        mock_repo_item.updated_at = datetime(2023, 12, 1)
        mock_repo_item.created_at = datetime(2023, 1, 1)
        mock_repo_item.html_url = 'https://github.com/test/new-repo'
        mock_repo_item.clone_url = 'https://github.com/test/new-repo.git'
        mock_repo_item.archived = False
        mock_repo_item.fork = False
        mock_repo_item.get_topics.return_value = ['python', 'tool']
        
        # Mock file contents for CLAUDE.md file
        mock_file_contents = Mock()
        mock_file_contents.size = 1000  # Larger than min_file_size
        mock_repo_item.get_contents.return_value = mock_file_contents
        
        # Make sure mock comparison operations work
        mock_search_result.totalCount = 1
        mock_search_result.get_page.return_value = [mock_repo_item]  # Mock get_page method
        
        mock_github.search_repositories.return_value = mock_search_result
        
        # Mock repository object for evaluation
        mock_repo = Mock()
        mock_repo.stargazers_count = 100
        mock_repo.updated_at = datetime(2023, 12, 1)
        mock_repo.created_at = datetime(2023, 1, 1)
        mock_repo.organization = None
        mock_repo.owner.login = 'test'
        
        # Mock CLAUDE.md file content
        mock_file = Mock()
        mock_file.decoded_content = b"""# Project Name

## Architecture

This project has a complex architecture...

## Development Commands

- `npm start` - Start development server
- `npm test` - Run tests

## Setup Instructions

1. Clone repository
2. Install dependencies
"""
        mock_file.size = 500
        
        mock_repo.get_contents.return_value = mock_file
        mock_github.get_repo.return_value = mock_repo
        
        # Initialize discovery with dummy token
        discovery = ClaudeFileDiscovery("dummy_token")
        
        # Run the complete workflow
        candidates = discovery.github_searcher.search_github_repos(discovery.existing_repos)
        
        # Verify search found candidates
        assert len(candidates) > 0
        assert candidates[0]['full_name'] == 'test/new-repo'
        
        # Evaluate the candidate
        evaluation = discovery.evaluator.evaluate_candidate(candidates[0])
        
        # Verify evaluation was successful
        assert evaluation is not None
        assert 'score' in evaluation
        assert 'suggested_category' in evaluation
        assert evaluation['score'] > 0
        
    def test_existing_repository_detection(self):
        """Test that existing repositories are properly detected and skipped."""
        discovery = ClaudeFileDiscovery("dummy_token")
        
        # Verify existing repository is loaded
        assert 'microsoft/semanticworkbench' in discovery.existing_repos
        
    @patch('scripts.discover_claude_files.Github')
    def test_error_handling_in_evaluation(self, mock_github_class):
        """Test error handling during repository evaluation."""
        mock_github = Mock()
        mock_github_class.return_value = mock_github
        
        # Mock GitHub API to raise exceptions
        mock_github.get_repo.side_effect = [
            UnknownObjectException(status=404, data='Not Found', headers={}),
            RateLimitExceededException(status=403, data='Rate Limited', headers={}),
            GithubException(status=500, data='Server Error', headers={})
        ]
        
        discovery = ClaudeFileDiscovery("dummy_token")
        
        candidate = {
            'full_name': 'test/repo',
            'name': 'repo',
            'owner': 'test',
            'description': 'Test repo',
            'stars': 100,
            'language': 'Python',
            'updated_at': '2023-12-01T00:00:00Z',
            'html_url': 'https://github.com/test/repo',
            'claude_file_path': 'CLAUDE.md',
            'clone_url': 'https://github.com/test/repo.git'
        }
        
        # Test handling of different exceptions
        result1 = discovery.evaluator.evaluate_candidate(candidate)
        assert result1 is None  # Should handle UnknownObjectException
        
        result2 = discovery.evaluator.evaluate_candidate(candidate)
        assert result2 is None  # Should handle RateLimitExceededException
        
        result3 = discovery.evaluator.evaluate_candidate(candidate)
        assert result3 is None  # Should handle GithubException
        
    def test_candidate_validation(self):
        """Test comprehensive candidate validation."""
        discovery = ClaudeFileDiscovery("dummy_token")
        
        # Valid candidate
        valid_candidate = {
            'full_name': 'test/repo',
            'name': 'repo',
            'owner': 'test',
            'description': 'Test repo',
            'stars': 100,
            'language': 'Python',
            'updated_at': '2023-12-01T00:00:00Z',
            'html_url': 'https://github.com/test/repo',
            'claude_file_path': 'CLAUDE.md',
            'clone_url': 'https://github.com/test/repo.git'
        }
        # Test candidate validation using the evaluator
        assert discovery.evaluator._validate_candidate(valid_candidate)
        
        # Invalid candidates - missing required fields
        invalid_candidates = [
            {},  # Empty
            {'full_name': 'test/repo'},  # Missing fields
            {**valid_candidate, 'stars': 'not_a_number'},  # Invalid type
            {k: ('' if k == 'full_name' else v) for k, v in valid_candidate.items() if k != 'name'},  # Missing 'name' field
        ]
        
        for i, invalid in enumerate(invalid_candidates):
            result = discovery.evaluator._validate_candidate(invalid)
            assert not result, f"Invalid candidate {i} should have failed validation: {invalid}"
            
    def test_text_sanitization(self):
        """Test content sanitization for security."""
        discovery = ClaudeFileDiscovery("dummy_token")
        
        # Test HTML escaping
        dangerous_text = '<script>alert("xss")</script>Safe text'
        sanitized = discovery.issue_generator._sanitize_text(dangerous_text)
        assert '<script>' not in sanitized
        assert '&lt;script&gt;' in sanitized
        assert 'Safe text' in sanitized
        
    def test_category_suggestion_algorithm(self):
        """Test the category suggestion algorithm with various content types."""
        discovery = ClaudeFileDiscovery("dummy_token")
        
        test_cases = [
            {
                'content': 'infrastructure runtime kubernetes docker platform engine',
                'expected': 'complex-projects'  # infrastructure is categorized under complex-projects
            },
            {
                'content': 'cli tool build generator formatter compiler',
                'expected': 'developer-tooling'
            },
            {
                'content': 'library framework sdk api client wrapper',
                'expected': 'libraries-frameworks'
            },
            {
                'content': 'tutorial example demo quickstart starter template',
                'expected': 'getting-started'
            }
        ]
        
        candidate = {
            'full_name': 'test/repo',
            'name': 'repo',
            'owner': 'test',
            'description': 'Test repo',
            'stars': 100,
            'language': 'Python',
            'updated_at': '2023-12-01T00:00:00Z',
            'html_url': 'https://github.com/test/repo',
            'claude_file_path': 'CLAUDE.md',
            'clone_url': 'https://github.com/test/repo.git'
        }
        
        for case in test_cases:
            suggested = discovery.evaluator._suggest_category(candidate, case['content'])
            assert suggested == case['expected'], f"Expected {case['expected']}, got {suggested} for content: {case['content'][:50]}..."


if __name__ == '__main__':
    pytest.main([__file__])