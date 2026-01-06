# DISCOVERY MODULE KNOWLEDGE BASE

**Parent**: See root AGENTS.md for project context

## OVERVIEW

Modular GitHub discovery system. Searches for CLAUDE.md files, evaluates quality, creates review issues.

## STRUCTURE

```
discovery/
├── orchestrator.py   # Workflow coordinator (49 lines)
├── loader.py         # Load existing repos, prevent duplicates (114 lines)
├── searcher.py       # GitHub API integration (206 lines)
├── evaluator.py      # Content-first scoring (516 lines) - CORE
├── reporter.py       # Issue generation (95 lines)
├── reporters/        # Formatting sub-components
│   ├── issue_formatter.py
│   ├── priority_grouper.py
│   └── summary_generator.py
└── utils.py          # Logging, retry decorator
```

## WHERE TO LOOK

| Task | File | Key Functions |
|------|------|---------------|
| Change search queries | `searcher.py` | `search_github_repos()`, `_search_with_query()` |
| Modify scoring weights | `evaluator.py` | `_calculate_*_score()` methods |
| Add recognized org | `evaluator.py` | `RECOGNIZED_ORGS` set |
| Change quality threshold | `../discover_claude_files.py` | Line 35: `e["score"] >= 60` |
| Customize issue format | `reporters/issue_formatter.py` | Format templates |
| Handle rate limits | `searcher.py` | `_handle_rate_limiting()` |

## DATA FLOW

```
main() → ClaudeFileDiscovery
         ├── RepositoryLoader.load_existing_repos()
         │   └── Scans scenarios/ for owner_repo dirs
         ├── GitHubSearcher.search_github_repos()
         │   └── 2 queries × 3 pages, filters archives/forks
         ├── RepositoryEvaluator.evaluate_candidate()
         │   └── 100-point scoring system
         └── IssueGenerator.create_discovery_issue()
             └── Creates GitHub issue if 60+ candidates exist
```

## SCORING SYSTEM

| Component | Points | Key Indicators |
|-----------|--------|----------------|
| Content Depth | 30 | Architecture, dev workflow, testing sections |
| Educational Value | 25 | Patterns, examples, actionable guidance |
| AI Effectiveness | 15 | Section count, commands, context |
| Project Maturity | 20 | Recent activity, stars, production indicators |
| Community Recognition | 10 | Recognized orgs, high stars (1000+) |

## ANTI-PATTERNS

- **Never** bypass rate limiting (respects `X-RateLimit-Remaining`)
- **Never** include archived/forked repos
- **Never** skip validation in `_validate_candidate()`
- **Avoid** files < 1000 bytes (too shallow)

## TESTING

Tests mirror module structure in `tests/discovery/`:
```bash
pytest tests/discovery/test_evaluator.py -v  # Core scoring tests
pytest tests/discovery/ --cov=scripts/discovery
```

## RECOGNIZED_ORGS

anthropic, openai, microsoft, cloudflare, google, vercel, supabase, prisma, langchain-ai, huggingface, pytorch, facebook, aws, hashicorp, docker, kubernetes
