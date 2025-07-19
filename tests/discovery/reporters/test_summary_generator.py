"""Tests for the SummaryGenerator module."""

import pytest

from scripts.discovery.reporters.summary_generator import SummaryGenerator


class TestSummaryGenerator:
    """Test the SummaryGenerator class."""

    @pytest.fixture
    def summary_generator(self):
        return SummaryGenerator()

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
            "total": 10,
            "exceptional": 2,
            "high": 3,
            "good": 4,
            "below_threshold": 1,
        }

        summary = summary_generator.generate_summary_section(counts)

        assert "Discovery Summary" in summary
        assert "Total Candidates**: 10" in summary
        assert "Exceptional** (≥85 points): 2" in summary
        assert "High** (70-84 points): 3" in summary
        assert "Good** (60-69 points): 4" in summary
        assert "Below Threshold** (<60 points): 1" in summary

    def test_generate_candidate_section(self, summary_generator):
        """Test generating candidate section."""
        eval_data = {
            "score": 85,  # Using new scoring scale
            "candidate": {
                "full_name": "test/repo",
                "html_url": "https://github.com/test/repo",
                "description": "Test repository",
                "stars": 100,
                "language": "Python",
                "topics": ["test", "python", "automation"],
                "claude_file_path": "claude.md",
            },
            "suggested_category": "test-category",
            "claude_content_length": 1000,
            "last_updated_days": 5,
            "reasons": ["High quality", "Good documentation"],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "test/repo" in section
        assert "85/100 points" in section
        assert "Test repository" in section
        assert "Stars**: 100" in section
        assert "Language**: Python" in section
        assert "Suggested Category**: test-category" in section
        assert "test, python, automation" in section
        assert "claude.md" in section
        assert "1,000 bytes" in section
        assert "5 days ago" in section
        assert "High quality" in section
        assert "Good documentation" in section

    def test_generate_candidate_section_no_topics(self, summary_generator):
        """Test generating candidate section without topics."""
        eval_data = {
            "score": 65,  # Using new scoring scale
            "candidate": {
                "full_name": "test/repo",
                "html_url": "https://github.com/test/repo",
                "description": "Test repository",
                "stars": 50,
                "language": "JavaScript",
                "topics": [],
                "claude_file_path": "CLAUDE.md",
            },
            "suggested_category": "test-category",
            "claude_content_length": 500,
            "last_updated_days": 10,
            "reasons": [],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "test/repo" in section
        assert "65/100 points" in section
        assert "Topics:" not in section  # Should not include topics section

    def test_generate_candidate_section_many_topics(self, summary_generator):
        """Test generating candidate section with many topics."""
        eval_data = {
            "score": 7,
            "candidate": {
                "full_name": "test/repo",
                "html_url": "https://github.com/test/repo",
                "description": "Test repository",
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
                "claude_file_path": "claude.md",
            },
            "suggested_category": "test-category",
            "claude_content_length": 2000,
            "last_updated_days": 3,
            "reasons": ["Good score"],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        # Should only include first 5 topics
        assert "topic1, topic2, topic3, topic4, topic5" in section
        assert "topic6" not in section
        assert "topic7" not in section

    def test_generate_candidate_section_no_description(self, summary_generator):
        """Test generating candidate section without description."""
        eval_data = {
            "score": 6,
            "candidate": {
                "full_name": "test/repo",
                "html_url": "https://github.com/test/repo",
                "description": "",
                "stars": 75,
                "language": "Go",
                "topics": ["go"],
                "claude_file_path": "claude.md",
            },
            "suggested_category": "test-category",
            "claude_content_length": 800,
            "last_updated_days": 7,
            "reasons": ["Decent score"],
        }

        section = summary_generator.generate_candidate_section(eval_data)

        assert "Description**: " in section

    def test_generate_guidelines_section(self, summary_generator):
        """Test generating guidelines section."""
        guidelines = summary_generator.generate_guidelines_section()

        assert "Review Guidelines" in guidelines
        assert "Quality" in guidelines
        assert "Uniqueness" in guidelines
        assert "Maintainability" in guidelines
        assert "Licensing" in guidelines
        assert "Category Fit" in guidelines
        assert "Next Steps" in guidelines
