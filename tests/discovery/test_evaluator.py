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
            "full_name": "owner/repo",
            "name": "repo",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://github.com/owner/repo",
            "claude_file_path": "CLAUDE.md",
        }

        assert evaluator._validate_candidate(valid_candidate)

    def test_validate_candidate_missing_fields(self, evaluator):
        """Test candidate validation with missing required fields."""
        incomplete_candidate = {
            "full_name": "owner/repo",
            "name": "repo",
            # Missing other required fields
        }

        assert not evaluator._validate_candidate(incomplete_candidate)

    def test_validate_candidate_invalid_types(self, evaluator):
        """Test candidate validation with invalid data types."""
        invalid_candidate = {
            "full_name": "owner/repo",
            "name": "repo",
            "owner": "owner",
            "stars": "not-a-number",  # Should be int
            "html_url": "https://github.com/owner/repo",
            "claude_file_path": "CLAUDE.md",
        }

        assert not evaluator._validate_candidate(invalid_candidate)

    def test_validate_candidate_invalid_url(self, evaluator):
        """Test candidate validation with invalid URL."""
        invalid_candidate = {
            "full_name": "owner/repo",
            "name": "repo",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://example.com/repo",  # Not GitHub URL
            "claude_file_path": "CLAUDE.md",
        }

        assert not evaluator._validate_candidate(invalid_candidate)

    def test_calculate_community_recognition_score(self, evaluator):
        """Test community recognition score calculation."""
        high_stars = {"stars": 2000, "owner": "microsoft", "organization": None}
        score, reasons = evaluator._calculate_community_recognition_score(high_stars)
        assert score == 10  # 5 for org + 5 for high stars
        assert "recognized organization" in reasons[0]
        assert "High community validation" in reasons[1]

        medium_stars = {"stars": 600, "owner": "individual", "organization": None}
        score, reasons = evaluator._calculate_community_recognition_score(medium_stars)
        assert score == 3  # Only star validation

        low_stars = {"stars": 150, "owner": "individual", "organization": None}
        score, reasons = evaluator._calculate_community_recognition_score(low_stars)
        assert score == 0

    def test_calculate_content_depth_score(self, evaluator):
        """Test content depth score calculation."""
        comprehensive_content = (
            """
        ## Architecture
        This shows the system design.

        ## Development
        Here are the development commands.

        ## Testing
        Testing procedures are documented.

        ## Troubleshooting
        Debug information is provided.
        """
            + "x" * 3000
        )  # Make it substantial

        score, reasons = evaluator._calculate_content_depth_score(comprehensive_content)
        assert (
            score >= 20
        )  # Should get points for arch, dev, testing, troubleshooting, and length
        assert any("architecture" in reason.lower() for reason in reasons)
        assert any("development" in reason.lower() for reason in reasons)
        assert any("testing" in reason.lower() for reason in reasons)

    def test_calculate_content_depth_score_empty(self, evaluator):
        """Test content depth score calculation with empty content."""
        score, reasons = evaluator._calculate_content_depth_score("")
        assert score == 0
        assert len(reasons) == 0

    def test_calculate_project_maturity_score(self, evaluator):
        """Test project maturity score calculation."""
        from datetime import datetime

        # Recent update with high stars and production keywords
        recent_date = datetime.now(UTC).isoformat()
        mature_candidate = {
            "updated_at": recent_date,
            "stars": 500,
            "description": "Production-ready enterprise software used by millions",
        }
        score, reasons = evaluator._calculate_project_maturity_score(mature_candidate)
        assert (
            score >= 15
        )  # Should get points for recent activity, stars, and production usage
        assert any("recently updated" in reason.lower() for reason in reasons)

    def test_calculate_educational_value_score(self, evaluator):
        """Test educational value score calculation."""
        educational_content = """
        This demonstrates best practices and advanced patterns.

        ## Example Usage
        ```python
        # Example code here
        ```

        ## Step-by-step Guide
        Follow these instructions carefully.
        """

        candidate = {"description": "Educational example showing best practices"}
        score, reasons = evaluator._calculate_educational_value_score(
            educational_content, candidate
        )
        assert score >= 15  # Should get points for patterns, examples, and guidance
        assert any(
            "pattern" in reason.lower() or "example" in reason.lower()
            for reason in reasons
        )

    def test_suggest_category_complex_project(self, evaluator):
        """Test category suggestion for complex projects."""
        complex_content = (
            "This is a microservices architecture with distributed systems."
        )

        candidate = {
            "description": "Enterprise platform with microservices",
            "topics": ["microservices", "architecture"],
            "language": "Java",
        }

        result = evaluator._suggest_category(candidate, complex_content)
        assert result == "complex-projects"

    def test_suggest_category_library_framework(self, evaluator):
        """Test category suggestion for libraries/frameworks."""
        library_content = "This is a utility library for developers."

        candidate = {
            "description": "React component library",
            "topics": ["library", "react"],
            "language": "JavaScript",
        }

        result = evaluator._suggest_category(candidate, library_content)
        assert result == "libraries-frameworks"

    def test_suggest_category_developer_tooling(self, evaluator):
        """Test category suggestion for developer tooling."""
        tooling_content = "This is a CLI tool for automation."

        candidate = {
            "description": "Build automation tool",
            "topics": ["cli", "automation"],
            "language": "Python",
        }

        result = evaluator._suggest_category(candidate, tooling_content)
        assert result == "developer-tooling"

    def test_suggest_category_getting_started(self, evaluator):
        """Test category suggestion for getting started projects."""
        tutorial_content = "This is a starter template for beginners."

        candidate = {
            "description": "Beginner tutorial and examples",
            "topics": ["tutorial", "example"],
            "language": "TypeScript",
        }

        result = evaluator._suggest_category(candidate, tutorial_content)
        assert result == "getting-started"

    def test_suggest_category_default_fallback(self, evaluator):
        """Test category suggestion default fallback."""
        generic_content = "Generic project description"

        dummy_candidate = {
            "description": "Some generic project",
            "topics": [],
            "language": "Go",  # Known language
        }

        result = evaluator._suggest_category(dummy_candidate, generic_content)
        assert result == "libraries-frameworks"  # Default for known language

    def test_suggest_category_unknown_language_fallback(self, evaluator):
        """Test category suggestion with unknown language."""
        generic_content = "Generic project description"

        dummy_candidate = {
            "description": "Some generic project",
            "topics": [],
            "language": "UnknownLanguage",
        }

        result = evaluator._suggest_category(dummy_candidate, generic_content)
        assert result == "complex-projects"  # Default fallback
