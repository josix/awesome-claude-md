"""Tests for the IssueGenerator module."""

from unittest.mock import Mock, patch

import pytest

from scripts.discovery.reporter import IssueGenerator


class TestIssueGenerator:
    """Test the IssueGenerator class."""

    @pytest.fixture
    def issue_generator(self):
        mock_searcher = Mock()
        return IssueGenerator(mock_searcher)

    def test_create_discovery_issue_empty(self, issue_generator):
        """Test creating discovery issue with empty evaluations."""
        with patch.object(issue_generator, '_save_discovery_report') as mock_save:
            issue_generator.create_discovery_issue([])
            assert not mock_save.called

    def test_create_discovery_issue_with_evaluations(self, issue_generator):
        """Test creating discovery issue with evaluations."""
        evaluations = [
            {
                'score': 8,
                'candidate': {
                    'full_name': 'test/repo',
                    'html_url': 'https://github.com/test/repo',
                    'description': 'Test repo',
                    'stars': 100,
                    'language': 'Python',
                    'topics': ['test'],
                    'claude_file_path': 'claude.md'
                },
                'suggested_category': 'test-category',
                'claude_content_length': 1000,
                'last_updated_days': 5,
                'reasons': ['High quality']
            }
        ]

        with patch.object(issue_generator, '_save_discovery_report') as mock_save:
            issue_generator.create_discovery_issue(evaluations)
            assert mock_save.called

    def test_save_discovery_report_success(self, issue_generator):
        """Test saving discovery report successfully."""
        title = "Test Discovery Report"
        body = "Test body content"

        with patch('builtins.open', create=True) as mock_open:
            with patch('scripts.discovery.reporter.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "20231201_120000"

                issue_generator._save_discovery_report(title, body)

                mock_open.assert_called_once()
                # Check that file was opened for writing
                mock_open.assert_called_with('discovery_report_20231201_120000.md', 'w', encoding='utf-8')

    def test_save_discovery_report_error(self, issue_generator):
        """Test saving discovery report with error."""
        title = "Test Discovery Report"
        body = "Test body content"

        with patch('builtins.open', side_effect=OSError("Permission denied")):
            with patch('scripts.discovery.reporter.logger') as mock_logger:
                issue_generator._save_discovery_report(title, body)

                mock_logger.error.assert_called_once()
                assert "Error saving discovery report" in mock_logger.error.call_args[0][0]
