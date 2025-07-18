"""Repository evaluator for scoring and assessing repository candidates."""

import logging
from datetime import datetime

import requests.exceptions
from github.GithubException import GithubException, UnknownObjectException

from .utils import retry_with_backoff

logger = logging.getLogger(__name__)


class RepositoryEvaluator:
    """Handles evaluation and scoring of repository candidates."""

    def __init__(self, github_searcher):
        self.github_searcher = github_searcher
        # Criteria thresholds based on CRITERIA.md
        self.acceptance_threshold = 70  # 100-point scale

    def _validate_candidate(self, candidate: dict) -> bool:
        """Validate that a candidate dictionary has the required structure."""
        required_fields = ['full_name', 'name', 'owner', 'stars', 'html_url', 'claude_file_path']

        if not isinstance(candidate, dict):
            return False

        for field in required_fields:
            if field not in candidate:
                logger.warning(f"Candidate missing required field '{field}'")
                return False

        # Validate data types
        if not isinstance(candidate['stars'], int) or candidate['stars'] < 0:
            logger.warning(f"Invalid stars value for {candidate.get('full_name', 'unknown')}")
            return False

        # Validate URLs
        if not (candidate['html_url'].startswith('https://github.com/') or
                candidate['html_url'].startswith('http://github.com/')):
            logger.warning(f"Invalid GitHub URL for {candidate.get('full_name', 'unknown')}")
            return False

        return True

    @retry_with_backoff(max_retries=3, exceptions=(UnknownObjectException, GithubException, requests.exceptions.RequestException, UnicodeDecodeError))
    def evaluate_candidate(self, candidate: dict) -> dict | None:
        """Evaluate a repository candidate and return a scored assessment."""

        if not self._validate_candidate(candidate):
            return None

        try:
            # Get repository object and fetch CLAUDE.md content
            repo = self.github_searcher.github.get_repo(candidate['full_name'])
            claude_content = self._fetch_claude_content(repo, candidate)

            # Calculate scores
            score = 0
            reasons = []

            # Calculate scores based on CRITERIA.md 100-point system
            repo_quality_score, repo_quality_reasons = self._calculate_repository_quality_score(repo, candidate)
            doc_excellence_score, doc_excellence_reasons = self._calculate_documentation_excellence_score(claude_content)
            ai_friendly_score, ai_friendly_reasons = self._calculate_ai_friendly_score(claude_content)
            uniqueness_score, uniqueness_reasons = self._calculate_uniqueness_score(candidate, claude_content)

            # Combine scores (total out of 100)
            score = repo_quality_score + doc_excellence_score + ai_friendly_score + uniqueness_score
            reasons.extend(repo_quality_reasons + doc_excellence_reasons + ai_friendly_reasons + uniqueness_reasons)

            # Suggest appropriate category
            suggested_category = self._suggest_category(candidate, claude_content)

            evaluation = {
                'candidate': candidate,
                'score': score,
                'reasons': reasons,
                'suggested_category': suggested_category,
                'claude_content_length': len(claude_content) if claude_content else 0,
                'last_updated_days': self._calculate_days_since_update(candidate)
            }

            logger.info(f"Evaluated {candidate['full_name']}: score {score}/100")
            return evaluation

        except (UnknownObjectException, GithubException) as e:
            logger.warning(f"Could not evaluate {candidate['full_name']}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error evaluating {candidate['full_name']}: {e}")
            return None

    def _fetch_claude_content(self, repo, candidate: dict) -> str:
        """Fetch CLAUDE.md content from repository."""
        try:
            claude_file = repo.get_contents(candidate['claude_file_path'])
            return claude_file.decoded_content.decode('utf-8')
        except (UnknownObjectException, GithubException, UnicodeDecodeError) as e:
            logger.warning(f"Could not fetch CLAUDE.md content from {candidate['full_name']}: {e}")
            return ""

    def _calculate_repository_quality_score(self, repo, candidate: dict) -> tuple[int, list[str]]:
        """Calculate Repository Quality score (25 points) based on CRITERIA.md."""
        score = 0
        reasons = []
        
        # Star Count & Recognition (10 points)
        stars_score, stars_reasons = self._calculate_star_count_score(candidate)
        score += stars_score
        reasons.extend(stars_reasons)
        
        # Maintenance & Activity (8 points)
        maintenance_score, maintenance_reasons = self._calculate_maintenance_score(candidate)
        score += maintenance_score
        reasons.extend(maintenance_reasons)
        
        # Production Usage & Impact (4 points)
        production_score, production_reasons = self._calculate_production_usage_score(candidate)
        score += production_score
        reasons.extend(production_reasons)
        
        # License & Legal (3 points)
        license_score, license_reasons = self._calculate_license_score(repo)
        score += license_score
        reasons.extend(license_reasons)
        
        return score, reasons

    def _calculate_star_count_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Star Count & Recognition scoring (0-10 points) per CRITERIA.md."""
        stars = candidate['stars']
        
        # Check if from recognized organization first
        if self._is_recognized_organization(candidate):
            if stars >= 10000:
                return 10, [f"Top-tier organization with {stars} stars"]
            elif stars >= 5000:
                return 10, [f"Top-tier organization ({candidate['owner']}) with {stars} stars"]
            elif stars >= 1000:
                return 8, [f"Well-known organization ({candidate['owner']}) with {stars} stars"]
            else:
                return 6, [f"Established organization ({candidate['owner']}) with {stars} stars"]
        
        # For non-organization repositories
        if stars >= 10000:
            return 10, [f"Exceptional star count ({stars})"]
        elif stars >= 5000:
            return 8, [f"High star count ({stars})"]
        elif stars >= 1000:
            return 6, [f"Good star count ({stars})"]
        elif stars >= 500:
            return 4, [f"Moderate star count ({stars})"]
        elif stars >= 100:
            return 2, [f"Minimum star threshold met ({stars})"]
        else:
            return 0, [f"Below minimum star threshold ({stars})"]

    def _calculate_maintenance_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Maintenance & Activity scoring (0-8 points) per CRITERIA.md."""
        days_since_update = self._calculate_days_since_update(candidate)
        
        if days_since_update <= 7:
            return 8, ["Daily/weekly commits, very active maintenance"]
        elif days_since_update <= 30:
            return 6, ["Monthly commits, responsive maintenance"]
        elif days_since_update <= 90:
            return 4, ["Commits within 3 months, basic maintenance"]
        elif days_since_update <= 180:
            return 2, ["Commits within 6 months"]
        else:
            return 0, [f"No commits in {days_since_update} days (>6 months)"]

    def _calculate_production_usage_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Production Usage & Impact scoring (0-4 points) per CRITERIA.md."""
        stars = candidate['stars']
        
        # Use star count and organization as proxy for production usage
        if self._is_recognized_organization(candidate) and stars >= 1000:
            return 4, ["Major production usage (recognized org + high stars)"]
        elif stars >= 5000:
            return 3, ["Significant community adoption"]
        elif stars >= 1000:
            return 2, ["Active user base, production-ready"]
        elif stars >= 500:
            return 1, ["Used in some production contexts"]
        else:
            return 0, ["Experimental/personal project"]

    def _calculate_license_score(self, repo) -> tuple[int, list[str]]:
        """License & Legal scoring (0-3 points) per CRITERIA.md."""
        try:
            license = repo.get_license()
            if not license:
                return 0, ["No license found"]
            
            license_name = license.license.spdx_id.lower() if license.license.spdx_id else ""
            
            permissive_licenses = ['mit', 'apache-2.0', 'bsd-2-clause', 'bsd-3-clause', 'isc']
            copyleft_licenses = ['gpl-2.0', 'gpl-3.0', 'lgpl-2.1', 'lgpl-3.0', 'agpl-3.0']
            
            if license_name in permissive_licenses:
                return 3, [f"Permissive license ({license.license.name})"]
            elif license_name in copyleft_licenses:
                return 2, [f"Copyleft license ({license.license.name})"]
            elif license_name:
                return 1, [f"Custom license ({license.license.name})"]
            else:
                return 1, ["License present but unrecognized"]
                
        except Exception as e:
            logger.warning(f"Could not check license: {e}")
            return 0, ["Could not determine license"]

    def _is_recognized_organization(self, candidate: dict) -> bool:
        """Check if repository is from a recognized organization per CRITERIA.md."""
        recognized_orgs = {
            # Top-tier organizations
            'anthropic', 'openai', 'microsoft', 'google', 'meta', 'facebook',
            'apple', 'amazon', 'netflix', 'uber', 'airbnb', 'spotify',
            
            # Well-known organizations  
            'github', 'gitlab', 'atlassian', 'docker', 'kubernetes',
            'pytorch', 'tensorflow', 'huggingface', 'langchain',
            'cloudflare', 'vercel', 'netlify', 'elastic', 'mongodb',
            'redis', 'postgresql', 'mysql', 'sentry', 'datadog',
            'stripe', 'twilio', 'shopify', 'square', 'paypal',
            'ethereum', 'bitcoin', 'polygon', 'chainlink'
        }
        
        owner_lower = candidate['owner'].lower()
        return owner_lower in recognized_orgs

    def _calculate_documentation_excellence_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Calculate Documentation Excellence score (30 points) based on CRITERIA.md."""
        if not claude_content:
            return 0, ["No CLAUDE.md content found"]
        
        score = 0
        reasons = []
        
        # Clarity & Structure (12 points)
        clarity_score, clarity_reasons = self._calculate_clarity_score(claude_content)
        score += clarity_score
        reasons.extend(clarity_reasons)
        
        # Completeness & Depth (10 points)
        completeness_score, completeness_reasons = self._calculate_completeness_score(claude_content)
        score += completeness_score
        reasons.extend(completeness_reasons)
        
        # Technical Accuracy (8 points)
        accuracy_score, accuracy_reasons = self._calculate_technical_accuracy_score(claude_content)
        score += accuracy_score
        reasons.extend(accuracy_reasons)
        
        return score, reasons

    def _calculate_clarity_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Clarity & Structure scoring (0-12 points) per CRITERIA.md."""
        content_lower = claude_content.lower()
        
        # Count clear sections/headers
        section_indicators = ['##', '###', '####']
        section_count = sum(claude_content.count(indicator) for indicator in section_indicators)
        
        # Look for logical organization
        has_overview = any(term in content_lower for term in ['overview', 'introduction', 'about'])
        has_architecture = any(term in content_lower for term in ['architecture', 'design', 'structure'])
        has_setup = any(term in content_lower for term in ['setup', 'installation', 'getting started'])
        has_usage = any(term in content_lower for term in ['usage', 'examples', 'commands'])
        
        organization_score = sum([has_overview, has_architecture, has_setup, has_usage])
        
        if section_count >= 10 and organization_score >= 3:
            return 12, ["Exceptional organization with clear sections and logical flow"]
        elif section_count >= 6 and organization_score >= 3:
            return 9, ["Well-organized with clear structure"]
        elif section_count >= 4 and organization_score >= 2:
            return 6, ["Generally well-structured with minor gaps"]
        elif section_count >= 2:
            return 3, ["Basic structure but could be clearer"]
        else:
            return 0, ["Poor organization or confusing structure"]

    def _calculate_completeness_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Completeness & Depth scoring (0-10 points) per CRITERIA.md."""
        content_lower = claude_content.lower()
        content_length = len(claude_content)
        
        # Check for comprehensive coverage areas
        coverage_areas = {
            'architecture': any(term in content_lower for term in ['architecture', 'design', 'structure', 'components']),
            'setup': any(term in content_lower for term in ['setup', 'installation', 'environment', 'dependencies']),
            'workflows': any(term in content_lower for term in ['workflow', 'process', 'development', 'building']),
            'context': any(term in content_lower for term in ['context', 'background', 'purpose', 'goals']),
            'examples': any(term in content_lower for term in ['example', 'sample', 'demo', 'usage']),
            'commands': '```' in claude_content or 'command' in content_lower
        }
        
        coverage_count = sum(coverage_areas.values())
        
        if content_length >= 3000 and coverage_count >= 5:
            return 10, ["Comprehensive coverage of architecture, setup, workflows, and context"]
        elif content_length >= 2000 and coverage_count >= 4:
            return 8, ["Covers most essential areas with good detail"]
        elif content_length >= 1500 and coverage_count >= 3:
            return 6, ["Covers key areas but missing some important details"]
        elif content_length >= 1000 and coverage_count >= 2:
            return 4, ["Basic coverage of main topics"]
        elif content_length >= 500:
            return 2, ["Limited coverage, significant gaps"]
        else:
            return 0, ["Minimal or inadequate documentation"]

    def _calculate_technical_accuracy_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Technical Accuracy scoring (0-8 points) per CRITERIA.md."""
        # This is a simplified heuristic - in practice would need more sophisticated analysis
        content_lower = claude_content.lower()
        
        # Look for signs of good technical documentation
        has_code_blocks = claude_content.count('```') >= 2
        has_file_paths = any(indicator in claude_content for indicator in ['/', '\\', '.js', '.py', '.md', '.json'])
        has_commands = any(cmd in content_lower for cmd in ['npm', 'yarn', 'pip', 'docker', 'git', 'make'])
        has_versions = any(char.isdigit() and '.' in claude_content[max(0, claude_content.find(char)-10):claude_content.find(char)+10] for char in claude_content if char.isdigit())
        
        technical_indicators = sum([has_code_blocks, has_file_paths, has_commands, has_versions])
        
        if technical_indicators >= 3:
            return 8, ["Technically accurate with up-to-date information"]
        elif technical_indicators >= 2:
            return 6, ["Generally accurate with minor issues"]
        elif technical_indicators >= 1:
            return 4, ["Mostly accurate but some unclear information"]
        else:
            return 2, ["Limited technical detail"]

    def _calculate_ai_friendly_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Calculate AI-Friendly Structure score (25 points) based on CRITERIA.md."""
        if not claude_content:
            return 0, ["No CLAUDE.md content found"]
        
        score = 0
        reasons = []
        
        # Context Provision (10 points)
        context_score, context_reasons = self._calculate_context_score(claude_content)
        score += context_score
        reasons.extend(context_reasons)
        
        # Command & Code Examples (8 points)
        examples_score, examples_reasons = self._calculate_examples_score(claude_content)
        score += examples_score
        reasons.extend(examples_reasons)
        
        # Architecture Description (7 points)
        arch_score, arch_reasons = self._calculate_architecture_score(claude_content)
        score += arch_score
        reasons.extend(arch_reasons)
        
        return score, reasons

    def _calculate_context_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Context Provision scoring (0-10 points) per CRITERIA.md."""
        content_lower = claude_content.lower()
        
        # Look for rich context indicators
        context_indicators = {
            'project_goals': any(term in content_lower for term in ['goal', 'purpose', 'mission', 'objective']),
            'architecture': any(term in content_lower for term in ['architecture', 'design', 'structure']),
            'workflows': any(term in content_lower for term in ['workflow', 'process', 'development']),
            'background': any(term in content_lower for term in ['background', 'context', 'overview']),
            'use_cases': any(term in content_lower for term in ['use case', 'usage', 'application', 'example'])
        }
        
        context_count = sum(context_indicators.values())
        content_length = len(claude_content)
        
        if content_length >= 2000 and context_count >= 4:
            return 10, ["Rich context about project goals, architecture, and workflows"]
        elif content_length >= 1500 and context_count >= 3:
            return 8, ["Good context with clear project understanding"]
        elif content_length >= 1000 and context_count >= 2:
            return 6, ["Adequate context for basic understanding"]
        elif context_count >= 2:
            return 4, ["Limited context, some gaps"]
        elif context_count >= 1:
            return 2, ["Minimal context provided"]
        else:
            return 0, ["Insufficient context for AI assistance"]

    def _calculate_examples_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Command & Code Examples scoring (0-8 points) per CRITERIA.md."""
        code_blocks = claude_content.count('```')
        content_lower = claude_content.lower()
        
        # Count different types of examples
        has_commands = any(cmd in content_lower for cmd in ['npm', 'yarn', 'pip', 'docker', 'git', 'make', 'cargo', 'go'])
        has_code_examples = code_blocks >= 2
        has_config_examples = any(term in content_lower for term in ['config', 'configuration', '.json', '.yaml', '.toml'])
        has_usage_examples = 'example' in content_lower or 'usage' in content_lower
        
        example_types = sum([has_commands, has_code_examples, has_config_examples, has_usage_examples])
        
        if code_blocks >= 6 and example_types >= 3:
            return 8, ["Extensive, accurate examples covering major workflows"]
        elif code_blocks >= 4 and example_types >= 2:
            return 6, ["Good examples for most common tasks"]
        elif code_blocks >= 2 and example_types >= 2:
            return 4, ["Basic examples covering some key areas"]
        elif code_blocks >= 1:
            return 2, ["Limited examples"]
        else:
            return 0, ["Few or no practical examples"]

    def _calculate_architecture_score(self, claude_content: str) -> tuple[int, list[str]]:
        """Architecture Description scoring (0-7 points) per CRITERIA.md."""
        content_lower = claude_content.lower()
        
        # Look for architectural information
        has_architecture_section = any(term in content_lower for term in ['## architecture', '## design', '## structure'])
        has_components = any(term in content_lower for term in ['component', 'module', 'service', 'layer'])
        has_relationships = any(term in content_lower for term in ['relationship', 'interaction', 'communication', 'flow'])
        has_diagrams = any(term in content_lower for term in ['diagram', 'chart', 'graph', 'visual'])
        
        arch_indicators = sum([has_architecture_section, has_components, has_relationships, has_diagrams])
        
        if arch_indicators >= 3 and has_architecture_section:
            return 7, ["Detailed architecture with component relationships"]
        elif arch_indicators >= 2:
            return 5, ["Clear architecture overview"]
        elif arch_indicators >= 1:
            return 3, ["Basic architectural information"]
        elif any(term in content_lower for term in ['architecture', 'design']):
            return 1, ["Minimal architectural details"]
        else:
            return 0, ["No clear architecture description"]

    def _calculate_uniqueness_score(self, candidate: dict, claude_content: str) -> tuple[int, list[str]]:
        """Calculate Uniqueness & Learning Value score (20 points) based on CRITERIA.md."""
        score = 0
        reasons = []
        
        # Novel Patterns or Techniques (8 points)
        novel_score, novel_reasons = self._calculate_novel_patterns_score(candidate, claude_content)
        score += novel_score
        reasons.extend(novel_reasons)
        
        # Educational Value (7 points)
        educational_score, educational_reasons = self._calculate_educational_value_score(candidate, claude_content)
        score += educational_score
        reasons.extend(educational_reasons)
        
        # Fills Collection Gap (5 points)
        gap_score, gap_reasons = self._calculate_collection_gap_score(candidate)
        score += gap_score
        reasons.extend(gap_reasons)
        
        return score, reasons

    def _calculate_novel_patterns_score(self, candidate: dict, claude_content: str) -> tuple[int, list[str]]:
        """Novel Patterns or Techniques scoring (0-8 points) per CRITERIA.md."""
        content_lower = claude_content.lower()
        
        # Look for advanced/unique patterns
        advanced_patterns = [
            'microservice', 'distributed', 'event-driven', 'reactive',
            'machine learning', 'ai', 'blockchain', 'serverless',
            'monorepo', 'micro-frontend', 'edge computing', 'streaming'
        ]
        
        unique_techniques = [
            'custom', 'novel', 'innovative', 'advanced', 'experimental',
            'cutting-edge', 'state-of-the-art', 'proprietary'
        ]
        
        pattern_count = sum(1 for pattern in advanced_patterns if pattern in content_lower)
        unique_count = sum(1 for technique in unique_techniques if technique in content_lower)
        
        # Consider organization reputation for innovation
        is_innovative_org = candidate['owner'].lower() in ['anthropic', 'openai', 'meta', 'google', 'microsoft']
        
        if pattern_count >= 3 or (pattern_count >= 2 and unique_count >= 1):
            return 8, ["Demonstrates unique, advanced patterns not seen elsewhere"]
        elif pattern_count >= 2 or (pattern_count >= 1 and unique_count >= 1):
            return 6, ["Shows interesting techniques with some uniqueness"]
        elif pattern_count >= 1 or is_innovative_org:
            return 4, ["Good practices but similar to existing examples"]
        elif len(claude_content) > 1000:
            return 2, ["Standard practices, limited novelty"]
        else:
            return 0, ["No unique value or patterns"]

    def _calculate_educational_value_score(self, candidate: dict, claude_content: str) -> tuple[int, list[str]]:
        """Educational Value scoring (0-7 points) per CRITERIA.md."""
        content_lower = claude_content.lower()
        
        # Look for educational indicators
        educational_terms = [
            'tutorial', 'guide', 'example', 'sample', 'demo',
            'best practice', 'pattern', 'lesson', 'learning'
        ]
        
        has_educational_content = sum(1 for term in educational_terms if term in content_lower)
        
        # Check for multiple audience levels
        has_beginner_content = any(term in content_lower for term in ['beginner', 'start', 'intro', 'basic'])
        has_advanced_content = any(term in content_lower for term in ['advanced', 'expert', 'deep', 'detailed'])
        
        # Content depth
        content_length = len(claude_content)
        code_blocks = claude_content.count('```')
        
        audience_range = sum([has_beginner_content, has_advanced_content])
        
        if content_length >= 2000 and code_blocks >= 4 and has_educational_content >= 2:
            return 7, ["High learning value for multiple developer levels"]
        elif content_length >= 1500 and (code_blocks >= 2 or has_educational_content >= 2):
            return 5, ["Good learning value for most developers"]
        elif content_length >= 1000 and has_educational_content >= 1:
            return 3, ["Some learning value for specific audiences"]
        elif has_educational_content >= 1:
            return 1, ["Limited educational benefit"]
        else:
            return 0, ["Little to no educational value"]

    def _calculate_collection_gap_score(self, candidate: dict) -> tuple[int, list[str]]:
        """Fills Collection Gap scoring (0-5 points) per CRITERIA.md."""
        # This is simplified - in practice would check against existing collection
        
        # Get language and topics
        language = candidate.get('language', '').lower()
        topics = [topic.lower() for topic in candidate.get('topics', [])]
        
        # Identify underrepresented areas (this would need to be updated based on actual collection)
        underrepresented_languages = ['rust', 'go', 'kotlin', 'swift', 'elixir', 'haskell']
        underrepresented_topics = [
            'blockchain', 'machine-learning', 'ai', 'edge-computing', 
            'iot', 'embedded', 'quantum', 'webassembly'
        ]
        
        fills_language_gap = language in underrepresented_languages
        fills_topic_gap = any(topic in underrepresented_topics for topic in topics)
        
        if fills_language_gap and fills_topic_gap:
            return 5, [f"Addresses underrepresented category ({language}) and technology ({topics})"]
        elif fills_language_gap or fills_topic_gap:
            return 3, ["Adds to less-represented area"]
        elif len(topics) > 0:
            return 1, ["Fits existing categories but adds value"]
        else:
            return 0, ["May duplicate existing coverage"]

    def _calculate_days_since_update(self, candidate: dict) -> int:
        """Calculate days since last repository update."""
        updated_date = datetime.fromisoformat(candidate['updated_at'].replace('Z', '+00:00'))
        return (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days

    def _suggest_category(self, candidate: dict, claude_content: str) -> str:
        """Suggest appropriate category based on repository characteristics."""

        # Keywords that suggest different categories
        categories = {
            'complex-projects': [
                'microservices', 'architecture', 'distributed', 'enterprise',
                'platform', 'system', 'infrastructure', 'scalable', 'multi-service'
            ],
            'libraries-frameworks': [
                'library', 'framework', 'sdk', 'api', 'npm', 'pypi', 'package',
                'component', 'widget', 'utility', 'helper'
            ],
            'developer-tooling': [
                'cli', 'tool', 'build', 'deploy', 'automation', 'workflow',
                'pipeline', 'ci/cd', 'development', 'debugging'
            ],
            'getting-started': [
                'tutorial', 'example', 'demo', 'sample', 'template', 'boilerplate',
                'starter', 'quickstart', 'beginner', 'learning'
            ]
        }

        # Analyze description and topics
        text_to_analyze = (
            (candidate.get('description', '') + ' ' +
             ' '.join(candidate.get('topics', [])) + ' ' +
             claude_content).lower()
        )

        category_scores = {}

        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                category_scores[category] = score

        # Return the category with the highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)

        # Default fallback based on language or other factors
        language = candidate.get('language', '').lower()
        if language in ['javascript', 'typescript', 'python', 'java', 'go', 'rust', 'c++']:
            return 'libraries-frameworks'

        return 'complex-projects'  # Default category
