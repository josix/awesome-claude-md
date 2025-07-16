#!/usr/bin/env python3
"""
Basic unit tests for the CLAUDE.md discovery script.
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the script to the path
sys.path.insert(0, os.path.dirname(__file__))
from discover_claude_files import ClaudeFileDiscovery


class TestClaudeFileDiscovery(unittest.TestCase):
    """Test cases for ClaudeFileDiscovery class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use a dummy token for testing (methods being tested don't need a valid token)
        self.discovery = ClaudeFileDiscovery("dummy_token")
    
    def test_validate_repo_name_valid(self):
        """Test repository name validation with valid names."""
        valid_names = [
            "owner/repo",
            "microsoft/typescript",
            "pytorch/pytorch",
            "owner/repo-name",
            "owner/repo_name",
            "owner/repo.name"
        ]
        
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(
                    self.discovery._validate_repo_name(name),
                    f"Expected {name} to be valid"
                )
    
    def test_validate_repo_name_invalid(self):
        """Test repository name validation with invalid names."""
        invalid_names = [
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
        ]
        
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(
                    self.discovery._validate_repo_name(name),
                    f"Expected {name} to be invalid"
                )
    
    def test_validate_candidate_valid(self):
        """Test candidate validation with valid candidate."""
        valid_candidate = {
            'full_name': 'owner/repo',
            'name': 'repo',
            'owner': 'owner',
            'stars': 100,
            'html_url': 'https://github.com/owner/repo',
            'claude_file_path': 'CLAUDE.md'
        }
        
        self.assertTrue(self.discovery._validate_candidate(valid_candidate))
    
    def test_validate_candidate_missing_fields(self):
        """Test candidate validation with missing required fields."""
        incomplete_candidate = {
            'full_name': 'owner/repo',
            'name': 'repo',
            # Missing other required fields
        }
        
        self.assertFalse(self.discovery._validate_candidate(incomplete_candidate))
    
    def test_validate_candidate_invalid_types(self):
        """Test candidate validation with invalid data types."""
        invalid_candidate = {
            'full_name': 'owner/repo',
            'name': 'repo',
            'owner': 'owner',
            'stars': 'not-a-number',  # Should be int
            'html_url': 'https://github.com/owner/repo',
            'claude_file_path': 'CLAUDE.md'
        }
        
        self.assertFalse(self.discovery._validate_candidate(invalid_candidate))
    
    def test_sanitize_text_basic(self):
        """Test text sanitization with basic input."""
        test_cases = [
            ("normal text", "normal text"),
            ("<script>alert('xss')</script>", "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"),
            ("", ""),
            ("a" * 600, "a" * 500 + "..."),  # Test length limiting
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                result = self.discovery._sanitize_text(input_text)
                self.assertEqual(result, expected)
    
    def test_sanitize_text_non_string(self):
        """Test text sanitization with non-string input."""
        result = self.discovery._sanitize_text(None)
        self.assertEqual(result, "")
        
        result = self.discovery._sanitize_text(123)
        self.assertEqual(result, "")
    
    def test_suggest_category(self):
        """Test category suggestion logic."""
        # Test case for complex project
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
        
        category = self.discovery._suggest_category(dummy_candidate, complex_content)
        self.assertIn(category, ["complex-projects", "developer-tooling", "getting-started"])
        
        # Test case for library
        library_content = """
        # API Reference
        
        This library provides core functionality.
        
        ## Usage
        
        ```python
        import library
        ```
        """
        
        category = self.discovery._suggest_category(dummy_candidate, library_content)
        # Should suggest an appropriate category
        self.assertIsInstance(category, str)
        self.assertTrue(len(category) > 0)


if __name__ == '__main__':
    unittest.main()