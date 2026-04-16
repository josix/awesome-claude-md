"""Tests for the ToolSummaryGenerator module."""

import pytest

from scripts.tool_discovery.reporters.summary_generator import ToolSummaryGenerator


class TestToolSummaryGenerator:
    """Test the ToolSummaryGenerator class."""

    @pytest.fixture
    def summary_generator(self):
        return ToolSummaryGenerator()

    def test_sanitize_text_normal(self, summary_generator):
        """Test sanitizing normal text."""
        result = summary_generator._sanitize_text("normal text")
        assert result == "normal text"

    def test_sanitize_text_html_escape(self, summary_generator):
        """Test sanitizing text with HTML characters."""
        result = summary_generator._sanitize_text("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
        assert "&lt;/script&gt;" in result

    def test_sanitize_text_length_limit(self, summary_generator):
        """Test sanitizing text that exceeds length limit."""
        long_text = "a" * 600
        result = summary_generator._sanitize_text(long_text)
        assert len(result) == 503  # 500 + "..."
        assert result.endswith("...")

    def test_sanitize_text_empty(self, summary_generator):
        """Test sanitizing empty text."""
        result = summary_generator._sanitize_text("")
        assert result == ""

    def test_sanitize_text_none(self, summary_generator):
        """Test sanitizing None."""
        result = summary_generator._sanitize_text(None)
        assert result == ""

    def test_sanitize_text_non_string(self, summary_generator):
        """Test sanitizing non-string input."""
        result = summary_generator._sanitize_text(123)
        assert result == ""

    def test_generate_summary_section(self, summary_generator):
        """Test generating summary section."""
        counts = {
            "total": 8,
            "exceptional": 2,
            "high": 3,
            "good": 2,
            "below_threshold": 1,
        }

        summary = summary_generator.generate_summary_section(counts)

        assert "Discovery Summary" in summary
        assert "Total Candidates" in summary
        assert "8" in summary
        assert "Exceptional" in summary
        assert "2" in summary

    def test_generate_candidate_section_includes_tool_type(self, summary_generator):
        """Test that candidate section includes tool_type field."""
        eval_data = {
            "score": 80,
            "candidate": {
                "full_name": "owner/cli-tool",
                "html_url": "https://github.com/owner/cli-tool",
                "description": "A CLI tool",
                "stars": 300,
                "language": "Python",
                "topics": ["cli", "automation"],
                "license": "MIT",
            },
            "tool_type": "cli",
            "suggested_category": "developer-tooling",
            "readme_length": 2500,
            "last_updated_days": 8,
            "reasons": ["Active project", "Good docs"],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "owner/cli-tool" in section
        assert "80" in section
        assert "A CLI tool" in section
        assert "Stars" in section
        assert "300" in section
        assert "Python" in section
        assert "cli" in section.lower()
        # Tool type should appear
        assert "cli" in section

    def test_generate_candidate_section_includes_license(self, summary_generator):
        """Test that candidate section includes license field."""
        eval_data = {
            "score": 70,
            "candidate": {
                "full_name": "owner/tool",
                "html_url": "https://github.com/owner/tool",
                "description": "A tool",
                "stars": 100,
                "language": "Go",
                "topics": [],
                "license": "Apache-2.0",
            },
            "tool_type": "service",
            "suggested_category": "developer-tooling",
            "readme_length": 1000,
            "last_updated_days": 30,
            "reasons": ["Open source"],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "Apache-2.0" in section or "License" in section

    def test_generate_candidate_section_no_topics(self, summary_generator):
        """Test generating candidate section without topics."""
        eval_data = {
            "score": 65,
            "candidate": {
                "full_name": "owner/tool",
                "html_url": "https://github.com/owner/tool",
                "description": "A simple tool",
                "stars": 50,
                "language": "JavaScript",
                "topics": [],
                "license": "MIT",
            },
            "tool_type": "plugin",
            "suggested_category": "developer-tooling",
            "readme_length": 800,
            "last_updated_days": 14,
            "reasons": [],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "owner/tool" in section
        assert "65" in section
        assert "Topics:" not in section

    def test_generate_candidate_section_many_topics(self, summary_generator):
        """Test generating candidate section with many topics (truncates to 5)."""
        eval_data = {
            "score": 75,
            "candidate": {
                "full_name": "owner/tool",
                "html_url": "https://github.com/owner/tool",
                "description": "A tool",
                "stars": 200,
                "language": "TypeScript",
                "topics": [
                    "topic1",
                    "topic2",
                    "topic3",
                    "topic4",
                    "topic5",
                    "topic6",
                    "topic7",
                ],
                "license": "MIT",
            },
            "tool_type": "library",
            "suggested_category": "developer-tooling",
            "readme_length": 1500,
            "last_updated_days": 3,
            "reasons": ["Comprehensive"],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "topic1, topic2, topic3, topic4, topic5" in section
        assert "topic6" not in section
        assert "topic7" not in section

    def test_generate_candidate_section_no_description(self, summary_generator):
        """Test generating candidate section without description."""
        eval_data = {
            "score": 55,
            "candidate": {
                "full_name": "owner/tool",
                "html_url": "https://github.com/owner/tool",
                "description": "",
                "stars": 30,
                "language": "Rust",
                "topics": ["tool"],
                "license": "MIT",
            },
            "tool_type": "cli",
            "suggested_category": "developer-tooling",
            "readme_length": 600,
            "last_updated_days": 45,
            "reasons": [],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "owner/tool" in section
        assert "Description" in section

    def test_generate_guidelines_section(self, summary_generator):
        """Test generating guidelines section."""
        guidelines = summary_generator.generate_guidelines_section()

        assert "Review Guidelines" in guidelines or "Guidelines" in guidelines
        assert "Next Steps" in guidelines

    def test_generate_summary_section_counts(self, summary_generator):
        """Test that summary section includes all priority level counts."""
        counts = {
            "total": 12,
            "exceptional": 3,
            "high": 4,
            "good": 3,
            "below_threshold": 2,
        }

        summary = summary_generator.generate_summary_section(counts)

        assert "12" in summary
        assert "3" in summary
        assert "4" in summary
        assert "2" in summary
