"""Tests for the RepositoryEvaluator module."""

from datetime import UTC, datetime, timedelta
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

    def test_calculate_star_count_score(self, evaluator):
        """Test star count score calculation (new 10-point system)."""
        # Exceptional star count (10k+)
        exceptional_stars = {'stars': 15000, 'owner': 'individual'}
        score, reasons = evaluator._calculate_star_count_score(exceptional_stars)
        assert score == 10
        assert "Exceptional star count" in reasons[0]

        # High star count (5k-9999)
        high_stars = {'stars': 7000, 'owner': 'individual'}
        score, reasons = evaluator._calculate_star_count_score(high_stars)
        assert score == 8
        assert "High star count" in reasons[0]

        # Good star count (1k-4999)
        good_stars = {'stars': 2000, 'owner': 'individual'}
        score, reasons = evaluator._calculate_star_count_score(good_stars)
        assert score == 6
        assert "Good star count" in reasons[0]

        # Moderate star count (500-999)
        medium_stars = {'stars': 600, 'owner': 'individual'}
        score, reasons = evaluator._calculate_star_count_score(medium_stars)
        assert score == 4
        assert "Moderate star count" in reasons[0]

        # Minimum threshold (100-499)
        low_stars = {'stars': 150, 'owner': 'individual'}
        score, reasons = evaluator._calculate_star_count_score(low_stars)
        assert score == 2
        assert "Minimum star threshold met" in reasons[0]

        # Below threshold (<100)
        very_low_stars = {'stars': 50, 'owner': 'individual'}
        score, reasons = evaluator._calculate_star_count_score(very_low_stars)
        assert score == 0
        assert "Below minimum star threshold" in reasons[0]

    def test_calculate_documentation_excellence_score(self, evaluator):
        """Test documentation excellence score calculation (new 30-point system)."""
        comprehensive_content = """
        # Project Overview
        This is a comprehensive project with detailed documentation.

        ## Architecture
        This shows the system design with components and relationships.

        ## Development Commands
        Here are the development commands and setup instructions.

        ## Testing
        Testing procedures are documented with examples.

        ```bash
        npm test
        npm run build
        ```

        ## Usage Examples
        Multiple code examples showing different use cases.

        ```javascript
        const example = require('./example');
        example.run();
        ```

        ## Configuration
        Detailed configuration options and setup.
        """

        score, reasons = evaluator._calculate_documentation_excellence_score(comprehensive_content)
        assert score >= 15  # Should score well across all categories
        assert len(reasons) >= 3  # Should have reasons from multiple categories

    def test_calculate_documentation_excellence_score_empty(self, evaluator):
        """Test documentation excellence score calculation with empty content."""
        score, reasons = evaluator._calculate_documentation_excellence_score("")
        assert score == 0
        assert "No CLAUDE.md content found" in reasons[0]

    def test_calculate_maintenance_score(self, evaluator):
        """Test maintenance score calculation (new 8-point system)."""
        from datetime import datetime

        # Very recent update (within 7 days)
        very_recent_date = datetime.now(UTC).isoformat()
        very_recent_candidate = {'updated_at': very_recent_date}
        score, reasons = evaluator._calculate_maintenance_score(very_recent_candidate)
        assert score == 8
        assert "Daily/weekly commits" in reasons[0]

        # Recent update (within 30 days)
        recent_date = (datetime.now(UTC) - timedelta(days=15)).isoformat()
        recent_candidate = {'updated_at': recent_date}
        score, reasons = evaluator._calculate_maintenance_score(recent_candidate)
        assert score == 6
        assert "Monthly commits" in reasons[0]

    def test_is_recognized_organization(self, evaluator):
        """Test recognized organization detection."""
        # Recognized organization
        recognized_candidate = {
            'owner': 'microsoft',
            'organization': None
        }
        assert evaluator._is_recognized_organization(recognized_candidate) == True

        # Another recognized organization
        anthropic_candidate = {
            'owner': 'anthropic',
            'organization': None
        }
        assert evaluator._is_recognized_organization(anthropic_candidate) == True

        # Unknown organization
        unknown_candidate = {
            'owner': 'unknown-org',
            'organization': None
        }
        assert evaluator._is_recognized_organization(unknown_candidate) == False

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
