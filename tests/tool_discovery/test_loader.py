"""Tests for the ToolLoader module."""

from unittest.mock import mock_open, patch

import pytest

from scripts.tool_discovery.loader import ToolLoader


class TestToolLoader:
    """Test the ToolLoader class."""

    @pytest.fixture
    def tool_loader(self):
        return ToolLoader()

    def test_load_existing_tools_no_readme(self, tool_loader):
        """Test loading existing tools when README.md doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            existing_tools = tool_loader.load_existing_tools()
            assert len(existing_tools) == 0

    def test_load_existing_tools_with_table_rows(self, tool_loader):
        """Test loading existing tools parses table rows correctly."""
        mock_readme = """
# Awesome Claude Tools

## Tools

| Tool | Repository | Description |
|------|-----------|-------------|
| MyTool | [owner/repo](https://github.com/owner/repo) | A cool tool |
| OtherTool | [owner2/repo2](https://github.com/owner2/repo2) | Another tool |
"""
        with patch("builtins.open", mock_open(read_data=mock_readme)):
            with patch("pathlib.Path.exists", return_value=True):
                existing_tools = tool_loader.load_existing_tools()
                assert "owner/repo" in existing_tools
                assert "owner2/repo2" in existing_tools

    def test_load_existing_tools_empty_table(self, tool_loader):
        """Test loading existing tools with an empty table."""
        mock_readme = """
# Awesome Claude Tools

## Tools

| Tool | Repository | Description |
|------|-----------|-------------|
"""
        with patch("builtins.open", mock_open(read_data=mock_readme)):
            with patch("pathlib.Path.exists", return_value=True):
                existing_tools = tool_loader.load_existing_tools()
                assert len(existing_tools) == 0

    def test_load_existing_tools_malformed_rows(self, tool_loader):
        """Test loading existing tools with malformed table rows."""
        mock_readme = """
# Awesome Claude Tools

## Tools

| Tool | Repository | Description |
|------|-----------|-------------|
| MalformedRow |
| | | |
| ValidTool | [owner/repo](https://github.com/owner/repo) | Valid |
"""
        with patch("builtins.open", mock_open(read_data=mock_readme)):
            with patch("pathlib.Path.exists", return_value=True):
                existing_tools = tool_loader.load_existing_tools()
                assert "owner/repo" in existing_tools

    def test_load_existing_tools_missing_section(self, tool_loader):
        """Test loading existing tools when tools section is missing."""
        mock_readme = """
# Awesome Claude Tools

No tools section here.
Just some random content.
"""
        with patch("builtins.open", mock_open(read_data=mock_readme)):
            with patch("pathlib.Path.exists", return_value=True):
                existing_tools = tool_loader.load_existing_tools()
                assert len(existing_tools) == 0

    def test_load_existing_tools_returns_set(self, tool_loader):
        """Test that load_existing_tools returns a set."""
        with patch("pathlib.Path.exists", return_value=False):
            existing_tools = tool_loader.load_existing_tools()
            assert isinstance(existing_tools, set)

    def test_load_existing_tools_deduplicates(self, tool_loader):
        """Test that load_existing_tools deduplicates repeated entries."""
        mock_readme = """
## Tools

| Tool | Repository | Description |
|------|-----------|-------------|
| Tool1 | [owner/repo](https://github.com/owner/repo) | First |
| Tool1Dup | [owner/repo](https://github.com/owner/repo) | Duplicate |
"""
        with patch("builtins.open", mock_open(read_data=mock_readme)):
            with patch("pathlib.Path.exists", return_value=True):
                existing_tools = tool_loader.load_existing_tools()
                assert len(existing_tools) == 1
                assert "owner/repo" in existing_tools
