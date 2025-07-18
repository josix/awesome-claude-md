"""Tests for the RepositoryEvaluator module."""

from datetime import UTC
from unittest.mock import Mock

import pytest

from scripts.discovery.evaluator import RepositoryEvaluator


class TestRepositoryEvaluator:
    """Test the RepositoryEvaluator class."""

    @pytest.fixture
    def evaluator(self):
        mock_searcher = Mock()
        return RepositoryEvaluator(mock_searcher)

    def test_validate_candidate_valid(self, evaluator):
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

    def test_validate_candidate_missing_fields(self, evaluator):
        """Test candidate validation with missing required fields."""
        incomplete_candidate = {
            'full_name': 'owner/repo',
            'name': 'repo',
            # Missing other required fields
        }

        assert not evaluator._validate_candidate(incomplete_candidate)

    def test_validate_candidate_invalid_types(self, evaluator):
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

    def test_validate_candidate_invalid_url(self, evaluator):
        """Test candidate validation with invalid URL."""
        invalid_candidate = {
            'full_name': 'owner/repo',
            'name': 'repo',
            'owner': 'owner',
            'stars': 100,
            'html_url': 'https://example.com/repo',  # Not GitHub URL
            'claude_file_path': 'CLAUDE.md'
        }

        assert not evaluator._validate_candidate(invalid_candidate)

    def test_calculate_stars_score(self, evaluator):
        """Test stars score calculation."""
        high_stars = {'stars': 2000}
        score, reasons = evaluator._calculate_stars_score(high_stars)
        assert score == 3
        assert "High star count" in reasons[0]

        medium_stars = {'stars': 600}
        score, reasons = evaluator._calculate_stars_score(medium_stars)
        assert score == 2

        low_stars = {'stars': 150}
        score, reasons = evaluator._calculate_stars_score(low_stars)
        assert score == 1

        very_low_stars = {'stars': 50}
        score, reasons = evaluator._calculate_stars_score(very_low_stars)
        assert score == 0

    def test_calculate_content_score(self, evaluator):
        """Test content score calculation."""
        comprehensive_content = """
        ## Architecture
        This shows the system design.

        ## Development
        Here are the development commands.

        ## Testing
        Testing procedures are documented.
        """

        score, reasons = evaluator._calculate_content_score(comprehensive_content)
        assert score >= 3
        assert any("architecture" in reason.lower() for reason in reasons)
        assert any("development" in reason.lower() for reason in reasons)
        assert any("testing" in reason.lower() for reason in reasons)

    def test_calculate_content_score_empty(self, evaluator):
        """Test content score calculation with empty content."""
        score, reasons = evaluator._calculate_content_score("")
        assert score == 0
        assert len(reasons) == 0

    def test_calculate_activity_score(self, evaluator):
        """Test activity score calculation."""
        from datetime import datetime

        # Recent update (within 30 days)
        recent_date = datetime.now(UTC).isoformat()
        recent_candidate = {'updated_at': recent_date}
        score, reasons = evaluator._calculate_activity_score(recent_candidate)
        assert score == 2
        assert "Recently updated (last 30 days)" in reasons[0]

    def test_calculate_organization_score(self, evaluator):
        """Test organization score calculation."""
        # Recognized organization
        recognized_candidate = {
            'owner': 'microsoft',
            'organization': None
        }
        score, reasons = evaluator._calculate_organization_score(recognized_candidate)
        assert score == 2
        assert "microsoft" in reasons[0]

        # Unknown organization
        unknown_candidate = {
            'owner': 'unknown-org',
            'organization': None
        }
        score, reasons = evaluator._calculate_organization_score(unknown_candidate)
        assert score == 0

    def test_suggest_category_complex_project(self, evaluator):
        """Test category suggestion for complex projects."""
        complex_content = "This is a microservices architecture with distributed systems."

        candidate = {
            'description': 'Enterprise platform with microservices',
            'topics': ['microservices', 'architecture'],
            'language': 'Java'
        }

        result = evaluator._suggest_category(candidate, complex_content)
        assert result == 'complex-projects'

    def test_suggest_category_library_framework(self, evaluator):
        """Test category suggestion for libraries/frameworks."""
        library_content = "This is a utility library for developers."

        candidate = {
            'description': 'React component library',
            'topics': ['library', 'react'],
            'language': 'JavaScript'
        }

        result = evaluator._suggest_category(candidate, library_content)
        assert result == 'libraries-frameworks'

    def test_suggest_category_developer_tooling(self, evaluator):
        """Test category suggestion for developer tooling."""
        tooling_content = "This is a CLI tool for automation."

        candidate = {
            'description': 'Build automation tool',
            'topics': ['cli', 'automation'],
            'language': 'Python'
        }

        result = evaluator._suggest_category(candidate, tooling_content)
        assert result == 'developer-tooling'

    def test_suggest_category_getting_started(self, evaluator):
        """Test category suggestion for getting started projects."""
        tutorial_content = "This is a starter template for beginners."

        candidate = {
            'description': 'Beginner tutorial and examples',
            'topics': ['tutorial', 'example'],
            'language': 'TypeScript'
        }

        result = evaluator._suggest_category(candidate, tutorial_content)
        assert result == 'getting-started'

    def test_suggest_category_default_fallback(self, evaluator):
        """Test category suggestion default fallback."""
        generic_content = "Generic project description"

        dummy_candidate = {
            'description': 'Some generic project',
            'topics': [],
            'language': 'Go'  # Known language
        }

        result = evaluator._suggest_category(dummy_candidate, generic_content)
        assert result == 'libraries-frameworks'  # Default for known language

    def test_suggest_category_unknown_language_fallback(self, evaluator):
        """Test category suggestion with unknown language."""
        generic_content = "Generic project description"

        dummy_candidate = {
            'description': 'Some generic project',
            'topics': [],
            'language': 'UnknownLanguage'
        }

        result = evaluator._suggest_category(dummy_candidate, generic_content)
        assert result == 'complex-projects'  # Default fallback
