#!/usr/bin/env python3
"""Parse discovery issue bodies and extract candidate data as JSON."""

import argparse
import html
import json
import logging
import re
import subprocess
import sys
from typing import Any

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def parse_candidates(issue_body: str) -> list[dict[str, Any]]:
    """Parse candidate blocks from a discovery issue body.

    Stops processing when the 'Below Threshold' section is reached.
    Returns candidates with score >= 60 only.
    """
    candidates: list[dict[str, Any]] = []

    # Split at the Below Threshold section to ignore it entirely
    below_threshold_pattern = re.compile(r"##\s+.*Below Threshold.*", re.IGNORECASE)
    match = below_threshold_pattern.search(issue_body)
    if match:
        issue_body = issue_body[: match.start()]

    # Find each candidate block starting with ### [
    block_pattern = re.compile(r"(### \[.+?)(?=### \[|\Z)", re.DOTALL)

    for block_match in block_pattern.finditer(issue_body):
        block = block_match.group(1).strip()
        candidate = _parse_candidate_block(block)
        if candidate is not None and candidate["score"] >= 60:
            candidates.append(candidate)

    return candidates


def _parse_candidate_block(block: str) -> dict[str, Any] | None:
    """Parse a single candidate block into a structured dict."""
    lines = block.splitlines()
    if not lines:
        return None

    # Parse header line: ### [owner/repo](html_url) - **score/100 points**
    header_pattern = re.compile(
        r"^### \[(?P<full_name>[^\]]+)\]\((?P<html_url>[^)]+)\)"
        r"\s+-\s+\*\*(?P<score>\d+)/100 points\*\*"
    )
    header_match = header_pattern.match(lines[0])
    if not header_match:
        logger.warning("Could not parse header line: %s", lines[0])
        return None

    full_name = html.unescape(header_match.group("full_name"))
    html_url = header_match.group("html_url")
    score = int(header_match.group("score"))

    owner, _, repo = full_name.partition("/")

    description = ""
    stars = 0
    language = "Unknown"
    suggested_category = ""
    topics: list[str] = []
    claude_file_path = ""
    claude_file_url = ""
    content_size = 0
    last_updated_days = 0
    scoring_reasons: list[str] = []

    in_scoring_reasons = False

    for line in lines[1:]:
        stripped = line.strip()

        if stripped.startswith("**Description**:"):
            description = html.unescape(stripped[len("**Description**:") :].strip())
            in_scoring_reasons = False

        elif stripped.startswith("**Stars**:"):
            # **Stars**: N | **Language**: X | **Suggested Category**: Y
            stars_match = re.search(r"\*\*Stars\*\*:\s*(\d+)", stripped)
            lang_match = re.search(r"\*\*Language\*\*:\s*([^|]+)", stripped)
            cat_match = re.search(r"\*\*Suggested Category\*\*:\s*(.+)", stripped)
            if stars_match:
                stars = int(stars_match.group(1))
            if lang_match:
                language = lang_match.group(1).strip()
            if cat_match:
                suggested_category = cat_match.group(1).strip()
            in_scoring_reasons = False

        elif stripped.startswith("**Topics**:"):
            topics_str = stripped[len("**Topics**:") :].strip()
            topics = [t.strip() for t in topics_str.split(",") if t.strip()]
            in_scoring_reasons = False

        elif stripped.startswith("**CLAUDE.md**:"):
            # **CLAUDE.md**: [claude_file_path](claude_file_url)
            claude_match = re.search(
                r"\*\*CLAUDE\.md\*\*:\s*\[([^\]]+)\]\(([^)]+)\)", stripped
            )
            if claude_match:
                claude_file_path = claude_match.group(1)
                claude_file_url = claude_match.group(2)
            in_scoring_reasons = False

        elif stripped.startswith("**Content Size**:"):
            # **Content Size**: N,NNN bytes | **Last Updated**: N days ago
            size_match = re.search(
                r"\*\*Content Size\*\*:\s*([\d,]+)\s*bytes", stripped
            )
            updated_match = re.search(
                r"\*\*Last Updated\*\*:\s*(\d+)\s*days ago", stripped
            )
            if size_match:
                content_size = int(size_match.group(1).replace(",", ""))
            if updated_match:
                last_updated_days = int(updated_match.group(1))
            in_scoring_reasons = False

        elif stripped == "**Scoring Reasons**:":
            in_scoring_reasons = True

        elif in_scoring_reasons and stripped.startswith("- "):
            scoring_reasons.append(stripped[2:].strip())

        elif stripped == "" and in_scoring_reasons:
            # Blank line ends scoring reasons
            in_scoring_reasons = False

    return {
        "full_name": full_name,
        "owner": owner,
        "repo": repo,
        "html_url": html_url,
        "score": score,
        "description": description,
        "stars": stars,
        "language": language,
        "suggested_category": suggested_category,
        "topics": topics,
        "claude_file_path": claude_file_path,
        "claude_file_url": claude_file_url,
        "content_size": content_size,
        "last_updated_days": last_updated_days,
        "scoring_reasons": scoring_reasons,
    }


def fetch_issue_body(issue_number: int) -> str:
    """Fetch issue body text from GitHub using the gh CLI."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_number), "--json", "body", "--jq", ".body"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> int:
    """Entry point for the process-issue script."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Parse discovery issue bodies and extract candidate data as JSON."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--issue-number",
        type=int,
        help="GitHub issue number to fetch and parse",
    )
    source_group.add_argument(
        "--body-file",
        type=str,
        help="Path to a file containing the issue body text",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (defaults to stdout)",
    )

    args = parser.parse_args()

    if args.issue_number is not None:
        logger.info("Fetching issue #%d from GitHub...", args.issue_number)
        try:
            issue_body = fetch_issue_body(args.issue_number)
        except subprocess.CalledProcessError as exc:
            logger.error("Failed to fetch issue: %s", exc)
            return 1
    else:
        logger.info("Reading issue body from file: %s", args.body_file)
        try:
            with open(args.body_file, encoding="utf-8") as fh:
                issue_body = fh.read()
        except OSError as exc:
            logger.error("Failed to read body file: %s", exc)
            return 1

    candidates = parse_candidates(issue_body)
    logger.info("Extracted %d candidate(s) above threshold", len(candidates))

    output_json = json.dumps(candidates, indent=2, ensure_ascii=False)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(output_json)
            logger.info("Wrote candidates to %s", args.output)
        except OSError as exc:
            logger.error("Failed to write output file: %s", exc)
            return 1
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
