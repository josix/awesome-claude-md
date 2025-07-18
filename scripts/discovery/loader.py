"""Repository loader for handling existing repositories in the collection."""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class RepositoryLoader:
    """Handles loading existing repositories from the collection."""

    def __init__(self):
        pass

    def load_existing_repos(self) -> set[str]:
        """Load list of repositories already included in the collection."""
        existing = set()
        scenarios_dir = Path('scenarios')

        if not scenarios_dir.exists():
            logger.info("No scenarios directory found")
            return existing

        for category_dir in scenarios_dir.iterdir():
            if category_dir.is_dir():
                self._process_category_directory(category_dir, existing)

        logger.info(f"Loaded {len(existing)} existing repositories")
        return existing

    def _process_category_directory(self, category_dir: Path, existing: set[str]) -> None:
        """Process a single category directory and extract repository names."""
        for repo_dir in category_dir.iterdir():
            if repo_dir.is_dir():
                repo_name = self._extract_repo_name_from_directory(repo_dir)
                if repo_name:
                    existing.add(repo_name)

    def _extract_repo_name_from_directory(self, repo_dir: Path) -> str | None:
        """Extract repository name from directory, trying analysis file first, then fallback."""
        dir_name = repo_dir.name
        if '_' not in dir_name:
            return None

        # Try to extract from analysis file first
        repo_name = self._extract_repo_name_from_analysis_file(repo_dir)
        if repo_name:
            return repo_name

        # Fallback to directory name parsing
        return self._extract_repo_name_from_directory_name(dir_name)

    def _extract_repo_name_from_analysis_file(self, repo_dir: Path) -> str | None:
        """Extract repository name from analysis README.md file."""
        analysis_file = repo_dir / 'README.md'
        if not analysis_file.exists():
            return None

        try:
            with open(analysis_file, encoding='utf-8') as f:
                content = f.read()
                repo_match = re.search(
                    r'\*\*Repository\*\*:\s*(?:\[.*?\]\()?https://github\.com/([^/\)\s]+/[^/\)\s]+)',
                    content
                )
                if repo_match:
                    repo_name = repo_match.group(1)
                    if self._validate_repo_name(repo_name):
                        return repo_name
                    else:
                        logger.warning(f"Invalid repository name format extracted: {repo_name}")
        except (OSError, UnicodeDecodeError) as e:
            logger.warning(f"Could not read {analysis_file}: {e}")
        except (re.error, AttributeError) as e:
            logger.warning(f"Regex parsing error for {analysis_file}: {e}")

        return None

    def _extract_repo_name_from_directory_name(self, dir_name: str) -> str | None:
        """Extract repository name from directory name using owner_repo format."""
        parts = dir_name.split('_', 1)
        if len(parts) == 2:
            owner, repo = parts
            return f"{owner}/{repo}"
        return None

    def _validate_repo_name(self, repo_name: str) -> bool:
        """Validate GitHub repository name format (owner/repo)."""
        if not isinstance(repo_name, str) or '/' not in repo_name:
            return False

        parts = repo_name.split('/')
        if len(parts) != 2:
            return False

        owner, repo = parts
        # Basic validation for GitHub username/org and repo name rules
        # GitHub usernames: 1-39 chars, alphanumeric or hyphens, can't start/end with hyphen
        # Repo names: similar rules but can contain dots, underscores
        if not (1 <= len(owner) <= 39 and re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', owner)):
            return False
        if not (1 <= len(repo) <= 100 and re.match(r'^[a-zA-Z0-9._-]+$', repo)):
            return False

        return True