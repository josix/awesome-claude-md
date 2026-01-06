#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def extract_takeaways(content: str) -> list[str]:
    """
    Auto-extract takeaways using regex patterns.

    Priority:
    1. Look for "## Takeaways" or "## Key Takeaways" section
    2. Extract bullet points (- or *)
    3. Fallback: Extract first 3 bullets from "## Key Features" or "## Why"
    """
    takeaways: list[str] = []

    # Pattern 1: Explicit takeaways section
    takeaway_patterns = [
        r"##\s*(?:Key\s+)?Takeaways?\s*\n((?:[-*]\s+.+\n?)+)",
        r"##\s*(?:Key\s+)?Insights?\s*\n((?:[-*]\s+.+\n?)+)",
        r"##\s*What\s+(?:Makes|Sets).+\n((?:[-*]\s+.+\n?)+)",
    ]

    for pattern in takeaway_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            bullets = re.findall(r"[-*]\s+(.+)", match.group(1))
            takeaways.extend([b.strip() for b in bullets[:5]])
            if takeaways:
                return takeaways

    # Pattern 2: Key Features section (fallback)
    features_pattern = r"##\s*(?:Key\s+)?Features?\s*\n((?:[-*]\s+.+\n?)+)"
    match = re.search(features_pattern, content, re.IGNORECASE)
    if match:
        bullets = re.findall(r"[-*]\s+(.+)", match.group(1))
        takeaways.extend([b.strip() for b in bullets[:3]])
        if takeaways:
            return takeaways

    # Pattern 3: Why section
    why_pattern = r"##\s*Why.+\n((?:[-*]\s+.+\n?)+)"
    match = re.search(why_pattern, content, re.IGNORECASE)
    if match:
        bullets = re.findall(r"[-*]\s+(.+)", match.group(1))
        takeaways.extend([b.strip() for b in bullets[:3]])

    return takeaways


def extract_languages(content: str) -> list[str]:
    """
    Infer programming languages from content.

    Detection methods:
    1. Explicit "Languages:" or "Stack:" mentions
    2. Code block language hints (```python, ```typescript)
    3. File extension mentions (.py, .ts, .rs)
    """
    languages: set[str] = set()

    # Language mapping for normalization
    lang_map = {
        "python": "Python",
        "py": "Python",
        "typescript": "TypeScript",
        "ts": "TypeScript",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "rust": "Rust",
        "rs": "Rust",
        "go": "Go",
        "golang": "Go",
        "ruby": "Ruby",
        "rb": "Ruby",
        "java": "Java",
        "kotlin": "Kotlin",
        "kt": "Kotlin",
        "swift": "Swift",
        "cpp": "C++",
        "c++": "C++",
        "csharp": "C#",
        "c#": "C#",
        "php": "PHP",
        "scala": "Scala",
        "elixir": "Elixir",
        "haskell": "Haskell",
        "lua": "Lua",
        "shell": "Shell",
        "bash": "Shell",
        "nix": "Nix",
        "zig": "Zig",
        "ocaml": "OCaml",
        "react": "React",
        "vue": "Vue",
        "svelte": "Svelte",
        "nextjs": "Next.js",
        "next.js": "Next.js",
    }

    # Method 1: Explicit language mentions
    explicit_patterns = [
        r"(?:Languages?|Stack|Tech(?:nology)?|Built with):\s*([^\n]+)",
        r"(?:Written in|Powered by)\s+(\w+(?:,?\s*\w+)*)",
    ]

    for pattern in explicit_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            words = re.findall(r"\b\w+\b", match.lower())
            for word in words:
                if word in lang_map:
                    languages.add(lang_map[word])

    # Method 2: Code block language hints
    code_blocks = re.findall(r"```(\w+)", content)
    for lang in code_blocks:
        lang_lower = lang.lower()
        if lang_lower in lang_map:
            languages.add(lang_map[lang_lower])

    # Method 3: File extension mentions
    extensions = re.findall(r"\.([a-z]{1,4})\b", content.lower())
    ext_map = {
        "py": "Python",
        "ts": "TypeScript",
        "js": "JavaScript",
        "rs": "Rust",
        "go": "Go",
        "rb": "Ruby",
        "kt": "Kotlin",
        "swift": "Swift",
        "java": "Java",
        "php": "PHP",
    }
    for ext in extensions:
        if ext in ext_map:
            languages.add(ext_map[ext])

    return sorted(languages)


def extract_key_features(content: str) -> list[str]:
    """Extract key features from the analysis."""
    features: list[str] = []

    # Look for sections that indicate features
    section_patterns = [
        r"##\s*(?:Key\s+)?Features?\s*\n((?:[-*]\s+.+\n?)+)",
        r"##\s*Highlights?\s*\n((?:[-*]\s+.+\n?)+)",
        r"##\s*What.+Covers?\s*\n((?:[-*]\s+.+\n?)+)",
    ]

    for pattern in section_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            bullets = re.findall(r"[-*]\s+(.+)", match.group(1))
            features.extend([b.strip() for b in bullets[:5]])
            if features:
                return features

    return features


def extract_source_url(content: str, owner: str, repo: str) -> str:
    """Extract or construct the source CLAUDE.md URL."""
    # Try to find explicit URL in content
    url_pattern = r"https://github\.com/[^\s\)]+/(?:blob/[^/]+/)?CLAUDE\.md"
    match = re.search(url_pattern, content)
    if match:
        return match.group(0)

    # Construct default URL
    return f"https://github.com/{owner}/{repo}/blob/main/CLAUDE.md"


def extract_title(content: str, repo: str) -> str:
    """Extract title from content or use repo name."""
    # Try to find H1 heading
    h1_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        # Clean up markdown links
        title = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", title)
        return title

    # Use repo name, converting to title case
    return repo.replace("-", " ").replace("_", " ").title()


def process_scenario(scenario_path: Path) -> dict[str, Any] | None:
    """Process a single scenario directory."""
    # Find README.md or analysis.md
    readme_path = scenario_path / "README.md"
    analysis_path = scenario_path / "analysis.md"

    content_path = None
    if readme_path.exists():
        content_path = readme_path
    elif analysis_path.exists():
        content_path = analysis_path
    else:
        return None

    content = content_path.read_text(encoding="utf-8")

    # Parse directory name: owner_repo
    dir_name = scenario_path.name
    parts = dir_name.split("_", 1)
    if len(parts) != 2:
        return None

    owner, repo = parts
    category = scenario_path.parent.name

    # Get file modification time
    mtime = datetime.fromtimestamp(content_path.stat().st_mtime)

    return {
        "id": dir_name,
        "category": category,
        "owner": owner,
        "repo": repo,
        "title": extract_title(content, repo),
        "sourceUrl": extract_source_url(content, owner, repo),
        "analysisPath": str(
            content_path.relative_to(scenario_path.parent.parent.parent)
        ),
        "languages": extract_languages(content),
        "takeaways": extract_takeaways(content),
        "keyFeatures": extract_key_features(content),
        "lastUpdated": mtime.strftime("%Y-%m-%d"),
        "content": content,  # Full content for search indexing
    }


def main() -> None:
    """Main extraction function."""
    # Find project root (where scenarios/ is located)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    scenarios_dir = project_root / "scenarios"

    if not scenarios_dir.exists():
        print(f"Error: scenarios directory not found at {scenarios_dir}")
        return

    scenarios: list[dict[str, Any]] = []
    categories: set[str] = set()
    all_languages: set[str] = set()

    # Walk through all category directories
    for category_dir in sorted(scenarios_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue

        categories.add(category_dir.name)

        # Process each scenario in the category
        for scenario_dir in sorted(category_dir.iterdir()):
            if not scenario_dir.is_dir() or scenario_dir.name.startswith("."):
                continue

            scenario = process_scenario(scenario_dir)
            if scenario:
                scenarios.append(scenario)
                all_languages.update(scenario.get("languages", []))

    # Sort scenarios by category, then by title
    scenarios.sort(key=lambda s: (s["category"], s["title"].lower()))

    # Build output
    output = {
        "scenarios": scenarios,
        "categories": sorted(categories),
        "languages": sorted(all_languages),
        "generatedAt": datetime.now().isoformat(),
        "totalCount": len(scenarios),
    }

    # Write to docs/public/scenarios.json
    output_path = project_root / "docs" / "public" / "scenarios.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(scenarios)} scenarios across {len(categories)} categories")
    print(f"Languages detected: {', '.join(sorted(all_languages))}")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
