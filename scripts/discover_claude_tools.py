#!/usr/bin/env python3
"""
Automated discovery script for CLAUDE.md-related tools across GitHub.

This script searches GitHub for repositories containing tools that generate,
sync, lint, or otherwise manage CLAUDE.md files, evaluates them against quality
standards, and creates issues for community review of promising candidates.
"""

import os

from scripts.discovery.utils import setup_logging
from scripts.tool_discovery.orchestrator import ClaudeToolDiscovery

logger = setup_logging()


def main():
    """Main execution function."""
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.error("Error: GITHUB_TOKEN environment variable is required")
        return 1

    logger.info("🔍 Starting automated CLAUDE.md tool discovery...")

    discovery = ClaudeToolDiscovery(github_token)

    # Run the tool discovery workflow
    evaluations = discovery.discover_new_tools()

    logger.info(
        f"Found {len(evaluations)} tool candidates that meet quality thresholds"
    )

    if not evaluations:
        logger.info("No tool candidates met the quality threshold for review")

    return 0


if __name__ == "__main__":
    exit(main())
