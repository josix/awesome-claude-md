"""GitHub repository searcher for finding CLAUDE.md files."""

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

from .utils import retry_with_backoff

logger = logging.getLogger(__name__)


class GitHubSearcher:
    """Handles GitHub API interactions and repository searching."""

    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
        )
        # Content-first approach - no star minimums
        self.min_file_size = 1000  # Increased for more substantial content

    def _handle_rate_limiting(self, response: requests.Response) -> None:
        """Handle GitHub API rate limiting adaptively."""
        # Check rate limit headers
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset_time = response.headers.get("X-RateLimit-Reset")

        if remaining and int(remaining) < 10:
            if reset_time:
                try:
                    reset_timestamp = int(reset_time)
                    current_time = time.time()
                    # Cap sleep time at 60 seconds to avoid workflow timeout
                    sleep_time = min(reset_timestamp - current_time + 1, 60)
                    if sleep_time > 0:
                        logger.warning(
                            f"Rate limit low, sleeping for {sleep_time} seconds"
                        )
                        time.sleep(sleep_time)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not parse rate limit headers: {e}")
                    time.sleep(1)  # Default 1 second delay

    @retry_with_backoff(
        max_retries=3,
        exceptions=(requests.exceptions.RequestException, GithubException),
    )
    def search_github_repos(self, existing_repos: set[str]) -> list[dict]:
        """Search GitHub for repositories with CLAUDE.md files."""
        logger.info("Starting GitHub repository search...")

        search_queries = [
            "filename:claude.md",
            "filename:CLAUDE.md",
            "filename:Claude.md",
        ]

        all_candidates = []

        for query in search_queries:
            logger.info(f"Searching with query: {query}")
            candidates = self._search_with_query(query, existing_repos)
            all_candidates.extend(candidates)

        logger.info(f"Found {len(all_candidates)} candidate repositories")
        return all_candidates

    def _search_with_query(self, query: str, existing_repos: set[str]) -> list[dict]:
        """Search GitHub with a specific query and return candidates."""
        candidates = []

        try:
            # Search for repositories using the GitHub API
            # Use pagination to get more results (up to 3 pages = 300 results)
            for page in range(1, 4):  # Pages 1, 2, 3
                search_results = self.github.search_code(
                    query=query, sort="indexed", order="desc"
                )

                # Get specific page results
                page_results = search_results.get_page(
                    page - 1
                )  # get_page is 0-indexed
                page_candidates = self._process_search_results(
                    page_results, existing_repos
                )
                candidates.extend(page_candidates)

                # Add a small delay between page requests to be respectful
                time.sleep(1)

        except RateLimitExceededException:
            logger.warning(f"Rate limit exceeded for query: {query}")
            time.sleep(60)  # Wait a minute before continuing
        except Exception as e:
            logger.error(f"Error searching with query '{query}': {e}")

        return candidates

    def _process_search_results(
        self, page_results, existing_repos: set[str]
    ) -> list[dict]:
        """Process search results and return valid candidates."""
        candidates = []

        for code_result in page_results:
            # Code search results have a .repository property
            repo = code_result.repository
            candidate = self._process_single_repository(repo, existing_repos)
            if candidate:
                candidates.append(candidate)
                logger.info(
                    f"Found candidate: {repo.full_name} ({repo.stargazers_count} stars)"
                )

        return candidates

    def _process_single_repository(self, repo, existing_repos: set[str]) -> dict | None:
        """Process a single repository and return candidate dict if valid."""
        # Skip repos we already have
        if repo.full_name in existing_repos:
            logger.debug(f"Skipping existing repository: {repo.full_name}")
            return None

        # Skip archived or forked repositories
        if repo.archived or repo.fork:
            logger.debug(f"Skipping archived/forked repository: {repo.full_name}")
            return None

        # No star-based filtering - content quality is evaluated in the evaluator

        # Try to fetch the CLAUDE.md file
        claude_file_path = self._find_claude_file(repo)
        if not claude_file_path:
            logger.debug(f"No CLAUDE.md file found in {repo.full_name}")
            return None

        return self._create_candidate_dict(repo, claude_file_path)

    def _create_candidate_dict(self, repo, claude_file_path: str) -> dict:
        """Create a candidate dictionary from repository information."""
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
            "claude_file_path": claude_file_path,
            "organization": repo.organization.login if repo.organization else None,
        }

    @retry_with_backoff(
        max_retries=3,
        exceptions=(
            UnknownObjectException,
            GithubException,
            requests.exceptions.HTTPError,
        ),
    )
    def _find_claude_file(self, repo) -> str | None:
        """Find CLAUDE.md file in repository and validate its size."""
        possible_paths = ["claude.md", "CLAUDE.md", "Claude.md"]

        for path in possible_paths:
            try:
                file_contents = repo.get_contents(path)

                # Check file size
                if file_contents.size < self.min_file_size:
                    logger.debug(
                        f"CLAUDE.md file too small in {repo.full_name}: {file_contents.size} bytes"
                    )
                    continue

                return path

            except UnknownObjectException:
                # File doesn't exist at this path
                continue
            except (
                GithubException,
                requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
            ) as e:
                logger.warning(f"Could not fetch CLAUDE.md from {repo.full_name}: {e}")
                continue

        return None
