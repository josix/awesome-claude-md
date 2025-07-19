#!/usr/bin/env python3
"""
Automated discovery script for new CLAUDE.md files across GitHub.

This script searches GitHub for repositories containing CLAUDE.md files,
evaluates them against quality standards, and creates issues for community
review of promising candidates.

Refactored into modular components following single responsibility principle.
"""

import os

from scripts.discovery.orchestrator import ClaudeFileDiscovery
from scripts.discovery.utils import setup_logging

logger = setup_logging()


def main():
    """Main execution function."""
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.error("Error: GITHUB_TOKEN environment variable is required")
        return 1

    logger.info("🔍 Starting automated CLAUDE.md discovery...")

    discovery = ClaudeFileDiscovery(github_token)

    # Run the discovery workflow
    evaluations = discovery.discover_new_repositories()

    # Filter for quality threshold (60+ points on 100-point scale)
    quality_evaluations = [e for e in evaluations if e["score"] >= 60]

    logger.info(
        f"Found {len(quality_evaluations)} candidates that meet quality thresholds (60+ points)"
    )

    if not quality_evaluations:
        logger.info("No candidates met the quality threshold for review")

    return 0


if __name__ == "__main__":
    exit(main())
