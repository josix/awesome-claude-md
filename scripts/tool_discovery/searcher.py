"""GitHub repository searcher for finding CLAUDE.md-related tools."""

import logging
import time

import requests
import requests.exceptions
from github import Github
from github.GithubException import (
    GithubException,
    RateLimitExceededException,
    UnknownObjectException,
)

from scripts.discovery.utils import retry_with_backoff

logger = logging.getLogger(__name__)


class ToolSearcher:
    """Handles GitHub API interactions and tool repository searching."""

    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
        )

    @retry_with_backoff(
        max_retries=3,
        exceptions=(requests.exceptions.RequestException, GithubException),
    )
    def search_github_repos(self, existing_tools: set[str]) -> list[dict]:
        """Search GitHub for repositories related to CLAUDE.md tools."""
        logger.info("Starting GitHub tool repository search...")

        search_queries = [
            '"claude.md" generator',
            '"CLAUDE.md" sync OR linter OR analyzer',
            '"AGENTS.md" "CLAUDE.md" generator OR scaffold',
            '"claude-md" in:name',
            '"CLAUDE.md" tool OR CLI OR action',
        ]

        all_candidates: list[dict] = []
        seen_full_names: set[str] = set()

        for query in search_queries:
            logger.info(f"Searching with query: {query}")
            candidates = self._run_search_query(query, existing_tools, seen_full_names)
            # Filter out any that are already in existing_tools
            filtered = [c for c in candidates if c["full_name"] not in existing_tools]
            all_candidates.extend(filtered)

        logger.info(f"Found {len(all_candidates)} candidate tool repositories")
        return all_candidates

    def _run_search_query(
        self,
        query: str,
        existing_tools: set[str],
        seen_full_names: set[str],
    ) -> list[dict]:
        """Run a single GitHub search query and return tool candidates."""
        candidates = []

        try:
            search_results = self.github.search_repositories(
                query=query, sort="updated", order="desc"
            )

            for page_num in range(1, 4):  # Limit to 3 pages to avoid timeout
                page_results = search_results.get_page(page_num - 1)
                page_candidates = self._process_page_results(
                    page_results, existing_tools, seen_full_names
                )
                candidates.extend(page_candidates)
                time.sleep(5)

        except RateLimitExceededException:
            logger.warning(f"Rate limit exceeded for query: {query}")
            time.sleep(60)
        except Exception as e:
            logger.error(f"Error searching with query '{query}': {e}")

        return candidates

    def _process_page_results(
        self,
        page_results,
        existing_tools: set[str],
        seen_full_names: set[str],
    ) -> list[dict]:
        """Process a page of search results and return valid tool candidates."""
        candidates = []

        for repo in page_results:
            candidate = self._process_single_repo(repo, existing_tools)
            if candidate and repo.full_name not in seen_full_names:
                candidates.append(candidate)
                seen_full_names.add(repo.full_name)
                logger.info(
                    f"Found tool candidate: {repo.full_name} ({repo.stargazers_count} stars)"
                )

        return candidates

    def _process_single_repo(self, repo, existing_tools: set[str]) -> dict | None:
        """Process a single repository and return candidate dict if valid."""
        if repo.full_name in existing_tools:
            logger.debug(f"Skipping existing tool: {repo.full_name}")
            return None

        if repo.archived or repo.fork:
            logger.debug(f"Skipping archived/forked repository: {repo.full_name}")
            return None

        readme_content = self._fetch_readme(repo)
        return self._create_candidate_dict(repo, readme_content)

    def _create_candidate_dict(self, repo, readme_content: str = "") -> dict:
        """Create a candidate dictionary from repository information."""
        license_value = None
        if repo.license:
            license_value = repo.license.spdx_id if repo.license.spdx_id else None

        return {
            "full_name": repo.full_name,
            "name": repo.name,
            "owner": repo.owner.login,
            "description": repo.description or "",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language,
            "topics": repo.get_topics(),
            "html_url": repo.html_url,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "license": license_value,
            "readme_content": readme_content,
        }

    @retry_with_backoff(
        max_retries=3,
        exceptions=(
            UnknownObjectException,
            GithubException,
            requests.exceptions.HTTPError,
        ),
    )
    def _fetch_readme(self, repo) -> str:
        """Fetch README content from the repository for evaluation."""
        possible_paths = ["README.md", "README.rst", "README.txt", "README"]

        for path in possible_paths:
            try:
                file_contents = repo.get_contents(path)
                return file_contents.decoded_content.decode("utf-8", errors="replace")
            except UnknownObjectException:
                continue
            except (
                GithubException,
                requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
                UnicodeDecodeError,
            ) as e:
                logger.warning(f"Could not fetch {path} from {repo.full_name}: {e}")
                continue

        return ""
