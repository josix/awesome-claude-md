"""Tool loader for handling existing tools in the collection."""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class ToolLoader:
    """Handles loading existing tools from the README Tools & Ecosystem table."""

    def __init__(self):
        pass

    def load_existing_tools(self) -> set[str]:
        """Load list of tools already included in the Tools & Ecosystem table."""
        existing = set()
        readme_path = Path(__file__).parents[2] / "README.md"

        if not readme_path.exists():
            logger.info("No README.md found")
            return existing

        try:
            with open(readme_path, encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            logger.warning(f"Could not read README.md: {e}")
            return existing

        section = self._extract_tools_section(content)
        if not section:
            logger.info("No 'Tools & Ecosystem' section found in README.md")
            return existing

        existing = self._parse_tool_table(section)
        logger.info(f"Loaded {len(existing)} existing tools")
        return existing

    def _extract_tools_section(self, content: str) -> str | None:
        """Extract the Tools & Ecosystem (or similar) section from README content."""
        # Try "Tools & Ecosystem" or "Tools" heading first (specific match)
        patterns = [
            r"##\s+.*?Tools.*?Ecosystem.*?\n(.*?)(?=\n##\s|\Z)",
            r"##\s+Tools\b.*?\n(.*?)(?=\n##\s|\Z)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1)

        # Fallback: return entire content so GitHub link regex can still find matches
        if re.search(r"\|\s*\[.*?\]\(https://github\.com/", content):
            return content

        return None

    def _parse_tool_table(self, section: str) -> set[str]:
        """Parse GitHub repo full_names from the tools table in the section."""
        existing = set()
        # Match markdown table rows with GitHub links
        pattern = r"\|\s*\[.*?\]\(https://github\.com/([^/]+/[^/)]+)\)"

        for match in re.finditer(pattern, section):
            full_name = match.group(1).strip()
            if self._validate_repo_name(full_name):
                existing.add(full_name)
                logger.debug(f"Loaded existing tool: {full_name}")
            else:
                logger.warning(f"Invalid repo name format in table: {full_name}")

        return existing

    def _validate_repo_name(self, repo_name: str) -> bool:
        """Validate GitHub repository name format (owner/repo)."""
        if not isinstance(repo_name, str) or "/" not in repo_name:
            return False

        parts = repo_name.split("/")
        if len(parts) != 2:
            return False

        owner, repo = parts
        if not (
            1 <= len(owner) <= 39
            and re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", owner)
        ):
            return False
        if not (1 <= len(repo) <= 100 and re.match(r"^[a-zA-Z0-9._-]+$", repo)):
            return False

        return True
