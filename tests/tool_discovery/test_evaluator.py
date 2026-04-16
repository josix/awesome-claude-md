"""Tests for the ToolEvaluator module."""

from unittest.mock import Mock

import pytest

from scripts.tool_discovery.evaluator import ToolEvaluator


class TestToolEvaluator:
    """Test the ToolEvaluator class."""

    @pytest.fixture
    def evaluator(self):
        mock_searcher = Mock()
        return ToolEvaluator(mock_searcher)

    def test_evaluate_candidate_returns_lower_score_for_non_permissive_license(
        self, evaluator
    ):
        """Test that non-permissive licenses receive a lower score than permissive licenses."""
        non_permissive_candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 500,
            "html_url": "https://github.com/owner/tool",
            "license": "GPL-3.0",
            "description": "A tool",
            "topics": [],
            "language": "Python",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-01T00:00:00Z",
            "organization": None,
        }
        permissive_candidate = {
            **non_permissive_candidate,
            "license": "MIT",
        }

        evaluator._get_readme_content = Mock(return_value="Some readme content")

        non_permissive_result = evaluator.evaluate_candidate(non_permissive_candidate)
        permissive_result = evaluator.evaluate_candidate(permissive_candidate)

        assert non_permissive_result is not None
        assert permissive_result is not None
        assert non_permissive_result["score"] < permissive_result["score"]

    def test_evaluate_candidate_returns_result_for_permissive_license(self, evaluator):
        """Test that permissive licenses pass the hard gate."""
        candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://github.com/owner/tool",
            "license": "MIT",
            "description": "A great tool",
            "topics": ["cli"],
            "language": "Python",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-01T00:00:00Z",
            "organization": None,
        }

        evaluator._get_readme_content = Mock(return_value="Some readme content")

        result = evaluator.evaluate_candidate(candidate)
        assert result is not None
        assert "score" in result
        assert "candidate" in result

    def test_detect_tool_type_cli(self, evaluator):
        """Test detecting CLI tool type."""
        candidate = {
            "description": "A command-line interface tool",
            "topics": ["cli"],
            "language": "Python",
        }
        readme = "Use this CLI tool to automate tasks."

        tool_type = evaluator._detect_tool_type(candidate, readme)
        assert tool_type == "cli"

    def test_detect_tool_type_plugin(self, evaluator):
        """Test detecting plugin tool type."""
        candidate = {
            "description": "A plugin for extending functionality",
            "topics": ["plugin", "extension"],
            "language": "JavaScript",
        }
        readme = "Install this plugin to add features."

        tool_type = evaluator._detect_tool_type(candidate, readme)
        assert tool_type == "plugin"

    def test_detect_tool_type_library(self, evaluator):
        """Test detecting library tool type."""
        candidate = {
            "description": "A library for building applications",
            "topics": ["library", "sdk"],
            "language": "TypeScript",
        }
        readme = "Import this library into your project."

        tool_type = evaluator._detect_tool_type(candidate, readme)
        assert tool_type == "library"

    def test_detect_tool_type_service(self, evaluator):
        """Test detecting service tool type."""
        candidate = {
            "description": "An API service for data processing",
            "topics": ["api", "service"],
            "language": "Go",
        }
        readme = "Deploy this service to your infrastructure."

        tool_type = evaluator._detect_tool_type(candidate, readme)
        assert tool_type == "service"

    def test_detect_tool_type_default(self, evaluator):
        """Test detecting default tool type when none match."""
        candidate = {
            "description": "Some project",
            "topics": [],
            "language": "Rust",
        }
        readme = "A generic project."

        tool_type = evaluator._detect_tool_type(candidate, readme)
        assert tool_type is not None
        assert isinstance(tool_type, str)

    def test_score_star_count(self, evaluator):
        """Test scoring based on star count."""
        high_stars = {"stars": 1000, "license": "MIT"}
        low_stars = {"stars": 5, "license": "MIT"}

        high_score, _ = evaluator._score_star_count(high_stars)
        low_score, _ = evaluator._score_star_count(low_stars)

        assert high_score > low_score

    def test_score_readme_quality(self, evaluator):
        """Test scoring based on README quality."""
        rich_readme = """
## Installation

```bash
pip install mytool
```

## Usage

Run the tool with:

```bash
mytool --help
```

## Configuration

Set up your config file.

## Examples

Here are some examples of usage.
"""
        minimal_readme = "A tool."

        rich_score, _ = evaluator._score_readme_quality(rich_readme)
        minimal_score, _ = evaluator._score_readme_quality(minimal_readme)

        assert rich_score > minimal_score

    def test_score_readme_quality_empty(self, evaluator):
        """Test scoring empty README."""
        score, reasons = evaluator._score_readme_quality("")
        assert score == 0
        assert len(reasons) == 0

    def test_evaluate_candidate_score_range(self, evaluator):
        """Test that evaluated scores fall within expected range."""
        candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 500,
            "html_url": "https://github.com/owner/tool",
            "license": "MIT",
            "description": "A useful CLI tool for developers",
            "topics": ["cli", "developer-tools"],
            "language": "Python",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-01T00:00:00Z",
            "organization": None,
        }

        evaluator._get_readme_content = Mock(
            return_value="## Usage\n```bash\ntool --help\n```\n## Installation\npip install tool"
        )

        result = evaluator.evaluate_candidate(candidate)
        assert result is not None
        assert 0 <= result["score"] <= 100

    def test_evaluate_candidate_missing_license_field(self, evaluator):
        """Test evaluation when license field is missing."""
        candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://github.com/owner/tool",
            # No license field
            "description": "A tool",
            "topics": [],
            "language": "Python",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-01T00:00:00Z",
            "organization": None,
        }

        evaluator._get_readme_content = Mock(return_value="")

        # Should not raise, should return a result with lower score due to missing license
        result = evaluator.evaluate_candidate(candidate)
        # Missing license means no license points, but candidate is not rejected
        assert isinstance(result, dict)
        assert 0 <= result["score"] <= 100

    def test_evaluate_candidate_empty_readme(self, evaluator):
        """Test evaluation when README is empty."""
        candidate = {
            "full_name": "owner/tool",
            "name": "tool",
            "owner": "owner",
            "stars": 50,
            "html_url": "https://github.com/owner/tool",
            "license": "Apache-2.0",
            "description": "A tool",
            "topics": [],
            "language": "Go",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-01T00:00:00Z",
            "organization": None,
        }

        evaluator._get_readme_content = Mock(return_value="")

        result = evaluator.evaluate_candidate(candidate)
        # Should still return a result, just with lower score
        assert result is not None
        assert result["score"] >= 0

    def test_evaluate_candidate_includes_tool_type(self, evaluator):
        """Test that evaluation result includes tool_type field."""
        candidate = {
            "full_name": "owner/cli-tool",
            "name": "cli-tool",
            "owner": "owner",
            "stars": 100,
            "html_url": "https://github.com/owner/cli-tool",
            "license": "MIT",
            "description": "A CLI tool",
            "topics": ["cli"],
            "language": "Python",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-12-01T00:00:00Z",
            "organization": None,
        }

        evaluator._get_readme_content = Mock(return_value="A command line tool.")

        result = evaluator.evaluate_candidate(candidate)
        assert result is not None
        assert "tool_type" in result
