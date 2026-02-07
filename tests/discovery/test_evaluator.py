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

        # Recent update with production keywords and maintenance signals
        recent_date = datetime.now(UTC).isoformat()
        mature_candidate = {
            "updated_at": recent_date,
            "stars": 500,
            "description": "Production-ready enterprise software used by millions",
        }
        score, reasons = evaluator._calculate_project_maturity_score(mature_candidate)
        assert (
            score >= 14
        )  # Should get points for recent activity, maintenance, and production usage
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

    def test_calculate_ai_effectiveness_with_constraints(self, evaluator):
        """Test that constraint/directive patterns earn AI effectiveness points."""
        content = """
        ## Guidelines

        You must never use global variables.
        Always run tests before committing.
        Do not modify generated files.
        Important: follow the coding standards at all times.

        ## Commands
        npm install
        npm test
        """

        score, reasons = evaluator._calculate_ai_effectiveness_score(content)
        # Should earn: sections (0), pkg manager (3), constraints (4)
        assert score >= 7
        assert any(
            "constraints" in r.lower() or "directives" in r.lower() for r in reasons
        )

    def test_calculate_ai_effectiveness_with_role_assignment(self, evaluator):
        """Test that role/methodology patterns earn AI effectiveness points."""
        content = """
        ## Role
        You are a senior software engineer working on this project.

        ## Methodology
        Use TDD for all new features. Follow the test-driven development workflow.

        ## Setup
        ## Commands
        ## Architecture
        ## Testing
        pip install -r requirements.txt
        """

        score, reasons = evaluator._calculate_ai_effectiveness_score(content)
        # Should earn: sections (3), pkg manager (3), context (2), role/methodology (2)
        assert score >= 10
        assert any("role" in r.lower() or "methodology" in r.lower() for r in reasons)

    def test_calculate_content_depth_with_file_navigation(self, evaluator):
        """Test that file/function references earn content depth points."""
        content = """
        ## Architecture
        The main entry point is `src/main.py`.
        Configuration is in `/config/settings.ts`.
        The router lives at `src/routes/index.js`.

        ## Key Functions
        Call initialize() to set up the app.
        Use Database::connect() for DB access.
        Run build() to compile.
        """

        score, reasons = evaluator._calculate_content_depth_score(content)
        # Should earn: architecture (8), file/function navigation (4)
        assert score >= 12
        assert any("navigation" in r.lower() or "file" in r.lower() for r in reasons)

    def test_calculate_educational_value_separated_code_snippets(self, evaluator):
        """Test that code snippets without 'example' keyword earn 5 pts, not 8."""
        content_code_only = """
        ## Setup

        ```bash
        npm install
        npm run build
        ```

        This shows advanced patterns and best practices for deployment.
        """

        candidate = {"description": "A deployment tool"}
        score, reasons = evaluator._calculate_educational_value_score(
            content_code_only, candidate
        )
        # Code snippets (5) + advanced keywords (5 for "pattern" and "best practice") = 10
        # No "example" keyword, so code_example_score = 5 not 8
        assert any("code snippets" in r.lower() for r in reasons)
        assert not any("examples or usage" in r.lower() for r in reasons)

    def test_calculate_educational_value_rejected_approaches(self, evaluator):
        """Test that rejected approach documentation earns educational value points."""
        content = """
        ## Design Decisions

        We deliberately chose SQLite over PostgreSQL for simplicity.
        We decided against using an ORM because of performance concerns.

        This pattern demonstrates best practices.

        ```python
        db = sqlite3.connect("app.db")
        ```
        """

        candidate = {"description": "Database toolkit"}
        score, reasons = evaluator._calculate_educational_value_score(
            content, candidate
        )
        # Should earn: advanced (5 for "pattern"+"best practice"), code (5), rejection (3)
        assert score >= 13
        assert any(
            "rejected" in r.lower() or "deliberate" in r.lower() for r in reasons
        )

    def test_calculate_project_maturity_without_star_double_count(self, evaluator):
        """Test that stars are not counted in project maturity score."""
        from datetime import datetime

        recent_date = datetime.now(UTC).isoformat()
        high_star_candidate = {
            "updated_at": recent_date,
            "stars": 5000,
            "description": "A simple utility library",
        }

        score, reasons = evaluator._calculate_project_maturity_score(
            high_star_candidate
        )
        # Should only get recency (8), no star points, no CI/CD, no maintenance
        assert score == 8
        assert not any("stars" in r.lower() for r in reasons)
        assert any("recently updated" in r.lower() for r in reasons)
