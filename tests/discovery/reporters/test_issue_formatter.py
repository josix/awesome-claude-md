"""Tests for the IssueFormatter module."""

import pytest

from scripts.discovery.reporters.issue_formatter import IssueFormatter


class TestIssueFormatter:
    """Test the IssueFormatter class."""

    @pytest.fixture
    def issue_formatter(self):
        return IssueFormatter()

    def test_init(self, issue_formatter):
        """Test initialization of IssueFormatter."""
        assert issue_formatter.priority_grouper is not None
        assert issue_formatter.summary_generator is not None

    def test_create_issue_title_empty(self, issue_formatter):
        """Test creating issue title with empty evaluations."""
        title = issue_formatter.create_issue_title([])

        assert "0 New CLAUDE.md Candidates Found" in title
        assert "High Priority" not in title

    def test_create_issue_title_no_exceptional_priority(self, issue_formatter):
        """Test creating issue title with no exceptional priority candidates."""
        evaluations = [
            {"score": 75},  # high
            {"score": 65},  # good
        ]

        title = issue_formatter.create_issue_title(evaluations)

        assert "2 New CLAUDE.md Candidates Found" in title
        assert "Exceptional" not in title

    def test_create_issue_title_with_exceptional_priority(self, issue_formatter):
        """Test creating issue title with exceptional priority candidates."""
        evaluations = [
            {"score": 90},  # exceptional
            {"score": 75},  # high
            {"score": 85},  # exceptional
        ]

        title = issue_formatter.create_issue_title(evaluations)

        assert "3 New CLAUDE.md Candidates Found" in title
        assert "(2 Exceptional)" in title

    def test_create_issue_body_empty(self, issue_formatter):
        """Test creating issue body with empty evaluations."""
        body = issue_formatter.create_issue_body([])

        assert body == "No new candidates found in this discovery run."

    def test_create_issue_body_with_evaluations(self, issue_formatter):
        """Test creating issue body with evaluations."""
        evaluations = [
            {
                "score": 85,  # exceptional
                "candidate": {
                    "full_name": "test/repo",
                    "html_url": "https://github.com/test/repo",
                    "description": "Test repository",
                    "stars": 100,
                    "language": "Python",
                    "topics": ["test"],
                    "claude_file_path": "CLAUDE.md",
                },
                "suggested_category": "test-category",
                "claude_content_length": 1000,
                "last_updated_days": 5,
                "reasons": ["High quality"],
            },
            {
                "score": 75,  # high
                "candidate": {
                    "full_name": "test/repo2",
                    "html_url": "https://github.com/test/repo2",
                    "description": "Another test repository",
                    "stars": 50,
                    "language": "JavaScript",
                    "topics": ["js"],
                    "claude_file_path": "CLAUDE.md",
                },
                "suggested_category": "libraries-frameworks",
                "claude_content_length": 500,
                "last_updated_days": 10,
                "reasons": ["Good structure"],
            },
        ]

        body = issue_formatter.create_issue_body(evaluations)

        # Check summary section
        assert "Discovery Summary" in body
        assert "Total Candidates**: 2" in body
        assert "Exceptional** (≥85 points): 1" in body
        assert "High** (70-84 points): 1" in body
        assert "Good** (60-69 points): 0" in body

        # Check exceptional priority section
        assert "## 🔥 Exceptional Quality" in body
        assert "test/repo" in body
        assert "85/100 points" in body

        # Check high priority section
        assert "## 🔥 High Quality" in body
        assert "test/repo2" in body
        assert "75/100 points" in body

        # Check guidelines section
        assert "Review Guidelines" in body
        assert "Quality" in body
        assert "Next Steps" in body

    def test_create_issue_body_only_below_threshold(self, issue_formatter):
        """Test creating issue body with only below-threshold evaluations."""
        evaluations = [
            {
                "score": 50,  # below threshold
                "candidate": {
                    "full_name": "test/low-repo",
                    "html_url": "https://github.com/test/low-repo",
                    "description": "Below threshold repository",
                    "stars": 20,
                    "language": "Python",
                    "topics": ["test"],
                    "claude_file_path": "CLAUDE.md",
                },
                "suggested_category": "getting-started",
                "claude_content_length": 200,
                "last_updated_days": 30,
                "reasons": ["Minimal documentation"],
            }
        ]

        body = issue_formatter.create_issue_body(evaluations)

        # Check summary
        assert "Total Candidates**: 1" in body
        assert "Below Threshold** (<60 points): 1" in body

        # Check below threshold section
        assert "Below Threshold" in body
        assert "test/low-repo" in body
        assert "50/100 points" in body

        # Should not have high priority sections (beyond summary count)
        assert "## 🔥 Exceptional Quality" not in body
        assert "## 🔥 High Quality" not in body

    def test_create_issue_body_mixed_priorities(self, issue_formatter):
        """Test creating issue body with mixed priority evaluations."""
        evaluations = [
            {"score": 90},  # exceptional
            {"score": 75},  # high
            {"score": 65},  # good
            {"score": 85},  # exceptional
            {"score": 50},  # below_threshold
        ]

        # Add minimal candidate data
        for eval_data in evaluations:
            eval_data["candidate"] = {
                "full_name": f"test/repo{eval_data['score']}",
                "html_url": f"https://github.com/test/repo{eval_data['score']}",
                "description": f"Test repository {eval_data['score']}",
                "stars": eval_data["score"] * 10,
                "language": "Python",
                "topics": ["test"],
                "claude_file_path": "CLAUDE.md",
            }
            eval_data["suggested_category"] = "test-category"
            eval_data["claude_content_length"] = 1000
            eval_data["last_updated_days"] = 5
            eval_data["reasons"] = ["Test reason"]

        body = issue_formatter.create_issue_body(evaluations)

        # Check summary
        assert "Total Candidates**: 5" in body
        assert "Exceptional** (≥85 points): 2" in body
        assert "High** (70-84 points): 1" in body
        assert "Good** (60-69 points): 1" in body
        assert "Below Threshold** (<60 points): 1" in body

        # Check all sections exist
        assert "## 🔥 Exceptional Quality" in body
        assert "## 🔥 High Quality" in body
        assert "## 🔥 Good Quality" in body
        assert "## 🔥 Below Threshold" in body
