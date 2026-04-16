"""Tests for the process_issue module."""

from scripts.process_issue import parse_candidates

SAMPLE_ISSUE_BODY = """## 🎯 Discovery Summary
- **Total Candidates**: 3
- **Exceptional** (≥85 points): 1
- **High** (70-84 points): 1
- **Good** (60-69 points): 1
- **Below Threshold** (<60 points): 0

## 🔥 Exceptional Quality (≥85 points)

### [example-org/amazing-project](https://github.com/example-org/amazing-project) - **92/100 points**
**Description**: An amazing project with great CLAUDE.md
**Stars**: 5000 | **Language**: TypeScript | **Suggested Category**: complex-projects
**Topics**: ai, typescript, framework
**CLAUDE.md**: [CLAUDE.md](https://github.com/example-org/amazing-project/blob/main/CLAUDE.md)
**Content Size**: 12,500 bytes | **Last Updated**: 5 days ago
**Scoring Reasons**:
- Comprehensive architecture documentation
- Excellent development workflow section

## 🔥 High Quality (70-84 points)

### [another-org/cool-tool](https://github.com/another-org/cool-tool) - **75/100 points**
**Description**: A cool developer tool
**Stars**: 800 | **Language**: Python | **Suggested Category**: developer-tooling
**CLAUDE.md**: [CLAUDE.md](https://github.com/another-org/cool-tool/blob/main/CLAUDE.md)
**Content Size**: 3,200 bytes | **Last Updated**: 15 days ago
**Scoring Reasons**:
- Clear command documentation

## 🔥 Below Threshold (<60 points)

### [skip-org/bad-project](https://github.com/skip-org/bad-project) - **45/100 points**
**Description**: Not great
**Stars**: 10 | **Language**: JavaScript | **Suggested Category**: getting-started
**CLAUDE.md**: [CLAUDE.md](https://github.com/skip-org/bad-project/blob/main/CLAUDE.md)
**Content Size**: 200 bytes | **Last Updated**: 90 days ago
**Scoring Reasons**:
- Minimal content
"""


class TestParseIssueBody:
    """Tests for parse_candidates function."""

    def test_parse_candidates_from_issue_body(self):
        """Parse the full sample and verify 2 candidates are returned (below threshold skipped)."""
        candidates = parse_candidates(SAMPLE_ISSUE_BODY)
        assert len(candidates) == 2

    def test_parse_single_candidate(self):
        """Verify all fields of the first (exceptional) candidate."""
        candidates = parse_candidates(SAMPLE_ISSUE_BODY)
        first = candidates[0]

        assert first["full_name"] == "example-org/amazing-project"
        assert first["owner"] == "example-org"
        assert first["repo"] == "amazing-project"
        assert first["html_url"] == "https://github.com/example-org/amazing-project"
        assert first["score"] == 92
        assert first["description"] == "An amazing project with great CLAUDE.md"
        assert first["stars"] == 5000
        assert first["language"] == "TypeScript"
        assert first["suggested_category"] == "complex-projects"
        assert first["topics"] == ["ai", "typescript", "framework"]
        assert first["claude_file_path"] == "CLAUDE.md"
        assert first["claude_file_url"] == (
            "https://github.com/example-org/amazing-project/blob/main/CLAUDE.md"
        )
        assert first["content_size"] == 12500
        assert first["last_updated_days"] == 5
        assert first["scoring_reasons"] == [
            "Comprehensive architecture documentation",
            "Excellent development workflow section",
        ]

    def test_parse_candidate_without_topics(self):
        """Verify the second candidate (no Topics line) has an empty topics list."""
        candidates = parse_candidates(SAMPLE_ISSUE_BODY)
        second = candidates[1]

        assert second["full_name"] == "another-org/cool-tool"
        assert second["topics"] == []

    def test_skip_below_threshold(self):
        """Verify the below-threshold candidate is excluded from results."""
        candidates = parse_candidates(SAMPLE_ISSUE_BODY)
        full_names = [c["full_name"] for c in candidates]
        assert "skip-org/bad-project" not in full_names

    def test_empty_issue_body(self):
        """Returns an empty list for an empty issue body."""
        candidates = parse_candidates("")
        assert candidates == []

    def test_parse_content_size_with_commas(self):
        """Verify '12,500 bytes' parses to integer 12500."""
        candidates = parse_candidates(SAMPLE_ISSUE_BODY)
        first = candidates[0]
        assert first["content_size"] == 12500

    def test_html_entities_are_unescaped(self):
        """Verify HTML entities from _sanitize_text are properly unescaped."""
        body = """## 🔥 High Quality (70-84 points)

### [some-org/a&amp;b&lt;c](https://github.com/some-org/a-b-c) - **72/100 points**
**Description**: Tools &amp; utilities for &lt;html&gt; processing
**Stars**: 100 | **Language**: Python | **Suggested Category**: developer-tooling
**CLAUDE.md**: [CLAUDE.md](https://github.com/some-org/a-b-c/blob/main/CLAUDE.md)
**Content Size**: 1,000 bytes | **Last Updated**: 10 days ago
**Scoring Reasons**:
- Good docs
"""
        candidates = parse_candidates(body)
        assert len(candidates) == 1
        assert candidates[0]["full_name"] == "some-org/a&b<c"
        assert candidates[0]["description"] == "Tools & utilities for <html> processing"
