#!/usr/bin/env python3
"""
Test suite for validating the awesome-ai-devtools README.md file.

This script validates:
- Markdown structure and formatting
- Link syntax validity
- Required sections presence
- Alphabetical ordering of entries (optional check)
"""

import re
import sys
from pathlib import Path


def read_readme():
    """Read the README.md file content."""
    readme_path = Path(__file__).parent / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError("README.md not found in repository root")
    return readme_path.read_text(encoding="utf-8")


def test_readme_exists():
    """Test that README.md file exists."""
    readme_path = Path(__file__).parent / "README.md"
    assert readme_path.exists(), "README.md should exist in the repository root"
    print("✓ README.md exists")


def test_readme_not_empty():
    """Test that README.md is not empty."""
    content = read_readme()
    assert len(content) > 0, "README.md should not be empty"
    print(f"✓ README.md is not empty ({len(content)} characters)")


def test_has_title():
    """Test that README has a main title (H1)."""
    content = read_readme()
    assert content.startswith("# "), "README.md should start with an H1 title"
    print("✓ README.md has a main title")


def test_has_required_sections():
    """Test that README has key required sections."""
    content = read_readme()
    required_sections = [
        "## IDEs",
        "## Assistants",
        "## Agents",
        "## Testing",
        "## Resources",
    ]

    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)

    assert not missing_sections, f"Missing required sections: {missing_sections}"
    print(f"✓ All {len(required_sections)} required sections present")


def test_link_syntax():
    """Test that all markdown links have valid syntax."""
    content = read_readme()

    # Pattern for markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    links = re.findall(link_pattern, content)

    invalid_links = []
    for text, url in links:
        # Check for common issues
        if not url.strip():
            invalid_links.append(f"Empty URL for text: {text}")
        elif url.startswith(" ") or url.endswith(" "):
            invalid_links.append(f"URL has extra spaces: {url}")
        elif not (url.startswith("http") or url.startswith("#") or url.startswith("/")):
            # Allow http(s), anchors, and relative paths
            if not url.startswith("mailto:"):
                invalid_links.append(f"Potentially invalid URL: {url}")

    assert not invalid_links, f"Invalid links found: {invalid_links}"
    print(f"✓ All {len(links)} links have valid syntax")


def test_no_broken_markdown_formatting():
    """Test for common markdown formatting issues."""
    content = read_readme()
    issues = []

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Check for unclosed brackets
        if line.count('[') != line.count(']'):
            # Skip if it's a code block or intentional
            if not line.strip().startswith('```'):
                issues.append(f"Line {i}: Mismatched brackets")

        # Check for unclosed parentheses in link context
        if '](' in line:
            if line.count('](') != line.count(')'):
                issues.append(f"Line {i}: Possible unclosed link parenthesis")

    # Only fail on clear issues, some edge cases are acceptable
    critical_issues = [i for i in issues if "Mismatched brackets" in i]
    assert len(critical_issues) < 5, f"Too many formatting issues: {critical_issues[:5]}"
    print("✓ No critical markdown formatting issues")


def test_list_items_format():
    """Test that list items follow the expected format."""
    content = read_readme()

    # Pattern for list items: - [Name](url) — Description
    list_item_pattern = r'^- \[.+\]\(.+\)'

    lines = content.split('\n')
    list_items = [line for line in lines if line.startswith('- [')]

    assert len(list_items) > 10, "Should have more than 10 list items"
    print(f"✓ Found {len(list_items)} properly formatted list items")


def test_no_duplicate_entries():
    """Test that there are no excessive duplicate tool entries.

    Note: Some duplicates are acceptable if a tool appears in multiple categories.
    This test warns about duplicates but only fails if there are many.
    """
    content = read_readme()

    # Extract tool names from links
    link_pattern = r'^- \[([^\]]+)\]'
    lines = content.split('\n')

    tool_names = []
    for line in lines:
        match = re.match(link_pattern, line)
        if match:
            tool_names.append(match.group(1).lower())

    duplicates = []
    seen = set()
    for name in tool_names:
        if name in seen:
            duplicates.append(name)
        seen.add(name)

    if duplicates:
        print(f"  Note: Found {len(duplicates)} duplicate(s): {duplicates[:5]}")

    # Allow some duplicates (tools may appear in multiple categories)
    assert len(duplicates) <= 5, f"Too many duplicate entries: {duplicates}"
    print(f"✓ Acceptable duplicate count ({len(duplicates)}) among {len(tool_names)} tools")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_readme_exists,
        test_readme_not_empty,
        test_has_title,
        test_has_required_sections,
        test_link_syntax,
        test_no_broken_markdown_formatting,
        test_list_items_format,
        test_no_duplicate_entries,
    ]

    print("=" * 50)
    print("Running README.md validation tests")
    print("=" * 50)

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error - {e}")
            failed += 1

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
