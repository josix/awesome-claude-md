# Static Site Design Doc: awesome-claude-md

**Status:** Draft
**Author:** [TBD]
**Date:** 2025-01-07
**Target:** MVP

---

## Problem

89 CLAUDE.md examples exist but are hard to discover. Users must manually browse GitHub directories. No search, no structured takeaways, no filtering.

## Goals (MVP)

| Priority | Feature | MVP Scope |
|----------|---------|-----------|
| P0 | Filter by category/language | Dropdown + tag filters |
| P0 | Full-text search | Client-side (Pagefind) |
| P1 | Browse takeaways | Card grid view |
| P2 | Compare side-by-side | Defer to v2 |
| P2 | Direct CLAUDE.md links | Include in cards |

## Non-Goals (MVP)

- Server-side search
- User accounts / favorites
- Comments / ratings
- Live CLAUDE.md preview (iframe)
- Side-by-side comparison

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Build Time                           │
├─────────────────────────────────────────────────────────┤
│  scenarios/**/*.md                                      │
│         │                                               │
│         ▼                                               │
│  ┌─────────────────┐    ┌──────────────────┐           │
│  │ Extract Script  │───▶│ scenarios.json   │           │
│  │ (takeaways,     │    │ (structured data)│           │
│  │  metadata)      │    └──────────────────┘           │
│  └─────────────────┘              │                    │
│                                   ▼                    │
│                          ┌──────────────────┐          │
│                          │   Astro Build    │          │
│                          │  (SSG + Pagefind)│          │
│                          └──────────────────┘          │
│                                   │                    │
│                                   ▼                    │
│                          ┌──────────────────┐          │
│                          │   _site/         │          │
│                          │   (static HTML)  │          │
│                          └──────────────────┘          │
└─────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────┐
│                    Runtime (Browser)                    │
├─────────────────────────────────────────────────────────┤
│  - Pagefind WASM for search                            │
│  - Client-side filtering (JS)                          │
│  - Zero server dependencies                            │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| SSG | **Astro** | Content collections, island architecture, fast builds |
| Search | **Pagefind** | Static search index, WASM runtime, zero config |
| Styling | **Tailwind CSS** | Rapid prototyping, small bundle |
| Hosting | **GitHub Pages** | Already configured, free |

**Why Astro over 11ty?**
- Native TypeScript support
- Content collections with schema validation
- Better DX for component islands (if needed later)

---

## Data Model

### Extraction Script Output (`scenarios.json`)

```json
{
  "scenarios": [
    {
      "id": "getsentry_sentry",
      "category": "complex-projects",
      "owner": "getsentry",
      "repo": "sentry",
      "title": "Sentry",
      "sourceUrl": "https://github.com/getsentry/sentry/blob/main/CLAUDE.md",
      "analysisPath": "scenarios/complex-projects/getsentry_sentry/README.md",
      "languages": ["Python", "TypeScript"],
      "takeaways": [
        "Uses monorepo structure with clear module boundaries",
        "Comprehensive testing strategy documented",
        "AI-specific debugging workflows included"
      ],
      "keyFeatures": [
        "Architecture overview",
        "Development workflow",
        "Testing guidelines"
      ],
      "stars": 35000,
      "lastUpdated": "2025-01-05"
    }
  ],
  "categories": ["complex-projects", "developer-tooling", ...],
  "languages": ["Python", "TypeScript", "Rust", ...]
}
```

### Extraction Logic (Build Script)

```python
# scripts/extract_scenarios.py

def extract_takeaways(content: str) -> list[str]:
    """
    Auto-extract takeaways using regex patterns:
    1. Look for "## Takeaways" or "## Key Takeaways" section
    2. Extract bullet points (- or *)
    3. Fallback: Extract first 3 bullets from "## Key Features"
    """
    patterns = [
        r"##\s*(?:Key\s+)?Takeaways\s*\n((?:[-*]\s+.+\n?)+)",
        r"##\s*Key\s+Features\s*\n((?:[-*]\s+.+\n?)+)",
    ]
    # ... extraction logic

def extract_languages(content: str) -> list[str]:
    """
    Infer from:
    1. Explicit "Languages:" or "Stack:" mentions
    2. Code block language hints (```python, ```typescript)
    3. File extension mentions (.py, .ts, .rs)
    """
    # ... extraction logic

def extract_metadata(readme_path: str) -> dict:
    """Parse README.md/analysis.md for structured data."""
    # ... extraction logic
```

---

## Site Structure

```
docs/
├── astro.config.mjs
├── package.json
├── src/
│   ├── content/
│   │   └── config.ts          # Content collection schema
│   ├── pages/
│   │   ├── index.astro        # Homepage with search + filters
│   │   ├── scenarios/
│   │   │   └── [id].astro     # Individual scenario page
│   │   └── categories/
│   │       └── [category].astro
│   ├── components/
│   │   ├── SearchBar.astro
│   │   ├── FilterPanel.astro
│   │   ├── ScenarioCard.astro
│   │   └── TakeawayList.astro
│   ├── layouts/
│   │   └── BaseLayout.astro
│   └── styles/
│       └── global.css
├── public/
│   └── scenarios.json         # Generated at build time
└── scripts/
    └── extract_scenarios.py   # Pre-build extraction
```

---

## UI Wireframes (ASCII)

### Homepage

```
┌─────────────────────────────────────────────────────────────┐
│  awesome-claude-md                              [GitHub ↗]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔍 Search scenarios...                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Category: [All ▼]   Language: [All ▼]   Sort: [Recent ▼]  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │ getsentry/sentry │  │ cloudflare/      │  │ vercel/   │ │
│  │ ────────────────│  │ workers-sdk      │  │ next.js   │ │
│  │ complex-projects │  │ ────────────────│  │ ─────────│ │
│  │                  │  │ developer-tooling│  │ libraries │ │
│  │ • Monorepo with  │  │                  │  │           │ │
│  │   clear modules  │  │ • pnpm only      │  │ • App     │ │
│  │ • Testing docs   │  │ • Changesets     │  │   router  │ │
│  │                  │  │                  │  │           │ │
│  │ Python, TS  ⭐35k│  │ TypeScript ⭐12k │  │ TS   ⭐95k│ │
│  │ [View →]        │  │ [View →]         │  │ [View →]  │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │ ...              │  │ ...              │  │ ...       │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
│                                                             │
│  Showing 1-9 of 89                          [1] [2] [→]    │
└─────────────────────────────────────────────────────────────┘
```

### Scenario Detail Page

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to scenarios                        [GitHub ↗]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  getsentry/sentry                                          │
│  ══════════════════                                        │
│  complex-projects  •  Python, TypeScript  •  ⭐ 35,000     │
│                                                             │
│  [View Original CLAUDE.md ↗]                               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## Key Takeaways                                          │
│                                                             │
│  ✓ Uses monorepo structure with clear module boundaries    │
│  ✓ Comprehensive testing strategy documented               │
│  ✓ AI-specific debugging workflows included                │
│  ✓ Clear separation of frontend/backend concerns           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## Analysis                                               │
│                                                             │
│  [Rendered markdown from README.md]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Foundation (MVP) — ~3-4 days

| Task | Effort | Output |
|------|--------|--------|
| Set up Astro project | 0.5d | `docs/` scaffolding |
| Write extraction script | 1d | `scripts/extract_scenarios.py` |
| Build homepage with cards | 1d | Filter + grid view |
| Integrate Pagefind | 0.5d | Working search |
| Deploy to GitHub Pages | 0.5d | Live site |

### Phase 2: Polish — ~2 days

| Task | Effort |
|------|--------|
| Scenario detail pages | 0.5d |
| Category landing pages | 0.5d |
| Mobile responsive | 0.5d |
| SEO meta tags | 0.5d |

### Phase 3: Future (v2)

- Side-by-side comparison view
- "Similar scenarios" recommendations
- RSS feed for new additions
- Dark mode
- Contribute CTA with issue template link

---

## Build Pipeline

```yaml
# .github/workflows/deploy-site.yml

name: Deploy Site

on:
  push:
    branches: [main]
    paths:
      - 'scenarios/**'
      - 'docs/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Extract scenario data
        run: |
          uv run python scripts/extract_scenarios.py
          cp scenarios.json docs/public/

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Build Astro site
        working-directory: docs
        run: |
          npm install
          npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/dist
```

---

## Open Questions

1. **Takeaway quality** — Should we manually review auto-extracted takeaways before launch, or ship and iterate?

2. **Language detection** — Regex-based vs. using existing metadata from analyses?

3. **Stars freshness** — Fetch live from GitHub API at build time, or accept stale data?

4. **URL structure** — `/scenarios/getsentry_sentry` or `/scenarios/complex-projects/getsentry_sentry`?

---

## Decision Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| SSG framework | Astro | Content collections, TS support |
| Search | Pagefind | Static, fast, zero backend |
| Styling | Tailwind | Rapid MVP iteration |
| Extraction | Build-time regex | Simpler than LLM, good enough for MVP |

---

## Success Metrics

| Metric | Target (MVP) |
|--------|--------------|
| Time to first search result | < 500ms |
| Lighthouse performance | > 90 |
| All 89 scenarios indexed | 100% |
| Filter combinations work | Category × Language |

---

## Next Steps

1. [ ] Review and approve design
2. [ ] Scaffold Astro project in `docs/`
3. [ ] Implement extraction script
4. [ ] Build MVP homepage
5. [ ] Deploy and validate
