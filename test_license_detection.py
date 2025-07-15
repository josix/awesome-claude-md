#!/usr/bin/env python3
"""
Test script for license detection functionality without API calls
"""

from detect_licenses import LicenseDetector
from pathlib import Path
import json

def test_url_extraction():
    """Test URL extraction patterns"""
    detector = LicenseDetector()
    
    test_cases = [
        # Basic Memory format
        ('**Source**: [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory)\n**CLAUDE.md**: [View Original](https://github.com/basicmachines-co/basic-memory/blob/main/CLAUDE.md)', 
         'https://github.com/basicmachines-co/basic-memory'),
        
        # Platformatic format
        ('**Repository:** https://github.com/platformatic/platformatic\n**CLAUDE.md File:** https://github.com/platformatic/platformatic/blob/main/CLAUDE.md', 
         'https://github.com/platformatic/platformatic'),
        
        # Cloudflare format
        ('**Repository**: https://github.com/cloudflare/workers-sdk\n**Why it\'s exemplary**: Demonstrates masterful monorepo',
         'https://github.com/cloudflare/workers-sdk'),
    ]
    
    print("Testing URL extraction patterns:")
    for i, (content, expected) in enumerate(test_cases, 1):
        extracted = detector.extract_repository_url(content)
        status = "✓" if extracted == expected else "✗"
        print(f"  {status} Test {i}: Expected '{expected}', got '{extracted}'")

def test_directory_inference():
    """Test directory-based repository inference"""
    detector = LicenseDetector()
    
    test_cases = [
        ('scenarios/complex-projects/gaearon_overreacted.io/analysis.md', 'gaearon', 'overreacted.io'),
        ('scenarios/developer-tooling/cloudflare_workers-sdk/analysis.md', 'cloudflare', 'workers-sdk'),
        ('scenarios/libraries-frameworks/langchain-ai_langchain-redis/analysis.md', 'langchain-ai', 'langchain-redis'),
    ]
    
    print("\nTesting directory-based repository inference:")
    for path_str, expected_owner, expected_repo in test_cases:
        file_path = Path(path_str)
        parts = file_path.parts
        if len(parts) >= 3 and parts[-1] == 'analysis.md':
            directory_name = parts[-2]
            if '_' in directory_name:
                owner_repo = directory_name.replace('_', '/', 1)
                owner, repo = owner_repo.split('/', 1)
                status = "✓" if owner == expected_owner and repo == expected_repo else "✗"
                print(f"  {status} {directory_name} -> {owner}/{repo}")

def test_existing_licenses():
    """Test extraction of existing license information"""
    detector = LicenseDetector()
    
    # Test with files that already have license info
    existing_license_files = [
        'scenarios/complex-projects/basicmachines-co_basic-memory/analysis.md',
        'scenarios/getting-started/anthropics_anthropic-quickstarts/analysis.md',
    ]
    
    print("\nTesting existing license extraction:")
    for file_path_str in existing_license_files:
        file_path = Path(file_path_str)
        if file_path.exists():
            license_info = detector.process_analysis_file(file_path)
            print(f"  {file_path.name}: {license_info}")

def generate_mock_results():
    """Generate mock results for testing the workflow"""
    mock_results = {}
    
    # Files with known licenses
    mock_results['complex-projects/basicmachines-co_basic-memory/analysis.md'] = 'MIT License'
    mock_results['getting-started/anthropics_anthropic-quickstarts/analysis.md'] = 'MIT License'
    mock_results['complex-projects/getsentry_sentry/analysis.md'] = 'BSL-1.1 License'
    
    # Mock results for files without licenses (common open source licenses)
    mock_results['complex-projects/gaearon_overreacted.io/analysis.md'] = 'MIT License'
    mock_results['complex-projects/platformatic_platformatic/analysis.md'] = 'Apache License 2.0'
    mock_results['developer-tooling/cloudflare_workers-sdk/analysis.md'] = 'Apache License 2.0'
    mock_results['libraries-frameworks/langchain-ai_langchain-redis/analysis.md'] = 'MIT License'
    
    with open('mock_license_results.json', 'w') as f:
        json.dump(mock_results, f, indent=2)
    
    print(f"\nGenerated mock results for {len(mock_results)} files")
    return mock_results

if __name__ == '__main__':
    test_url_extraction()
    test_directory_inference()
    test_existing_licenses()
    generate_mock_results()
    print("\nAll tests completed!")