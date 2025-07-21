#!/usr/bin/env python3
"""
Generate release notes for GitHub releases based on conventional commits.
"""

import os
import subprocess
import sys
from typing import Dict, List, Optional


def get_commits_since_tag(tag: Optional[str] = None) -> List[str]:
    """Get commits since the last tag or all commits if no tag exists."""
    if tag:
        cmd = ["git", "log", "--pretty=format:%s", f"{tag}..HEAD"]
    else:
        cmd = ["git", "log", "--pretty=format:%s", "--reverse"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []

    return [line.strip() for line in result.stdout.split("\n") if line.strip()]


def parse_conventional_commit(commit: str) -> Dict[str, str]:
    """Parse a conventional commit message."""
    # Check for breaking changes
    if "BREAKING CHANGE" in commit:
        return {
            "type": "breaking",
            "message": commit.split(": ", 1)[1] if ": " in commit else commit,
        }

    # Check for conventional commit format
    import re

    pattern = r"^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\([^)]+\))?: (.+)$"
    match = re.match(pattern, commit)

    if match:
        commit_type = match.group(1)
        scope = match.group(2) if match.group(2) else ""
        message = match.group(3)

        # Check for breaking change indicator
        if commit.startswith(f"{commit_type}{scope}!"):
            return {"type": "breaking", "message": message}

        return {"type": commit_type, "scope": scope.strip("()"), "message": message}

    return {"type": "other", "message": commit}


def categorize_commits(commits: List[str]) -> Dict[str, List[str]]:
    """Categorize commits by type."""
    categories = {
        "breaking": [],
        "feat": [],
        "fix": [],
        "docs": [],
        "chore": [],
        "other": [],
    }

    for commit in commits:
        parsed = parse_conventional_commit(commit)
        commit_type = parsed["type"]
        message = parsed["message"]

        if commit_type == "breaking":
            categories["breaking"].append(f"- **BREAKING**: {message}")
        elif commit_type in categories:
            categories[commit_type].append(f"- {message}")
        else:
            categories["other"].append(f"- {commit}")

    return categories


def generate_release_body(version: str, categories: Dict[str, List[str]]) -> str:
    """Generate the release body markdown."""
    lines = [f"## 🚀 Release v{version}", ""]

    # Breaking changes
    if categories["breaking"]:
        lines.extend(["### ⚠️ Breaking Changes"])
        lines.extend(categories["breaking"])
        lines.append("")

    # Features
    if categories["feat"]:
        lines.extend(["### ✨ New Features"])
        lines.extend(categories["feat"])
        lines.append("")

    # Bug fixes
    if categories["fix"]:
        lines.extend(["### 🐛 Bug Fixes"])
        lines.extend(categories["fix"])
        lines.append("")

    # Documentation
    if categories["docs"]:
        lines.extend(["### 📚 Documentation"])
        lines.extend(categories["docs"])
        lines.append("")

    # Maintenance
    if categories["chore"]:
        lines.extend(["### 🔧 Maintenance"])
        lines.extend(categories["chore"])
        lines.append("")

    # Other changes
    if categories["other"]:
        lines.extend(["### 📝 Other Changes"])
        lines.extend(categories["other"])
        lines.append("")

    # Standard sections
    lines.extend(
        [
            "### 🚀 Quick Start",
            "```bash",
            "git clone https://github.com/yugri/grafana_observer_tutorial.git",
            "cd grafana_observer_tutorial",
            "./start.sh",
            "```",
            "",
            "### 🌐 Access Points",
            "- **Application**: http://localhost:8000",
            "- **Prometheus**: http://localhost:9090",
            "- **Grafana**: http://localhost:3000 (admin/admin)",
            "",
            "### 📖 Documentation",
            "- [README.md](README.md) - Project overview and quick start",
            "- [TUTORIAL.md](TUTORIAL.md) - Detailed learning guide",
            "- [SECURITY.md](SECURITY.md) - Security information",
            "",
            "---",
            "*This release was automatically generated based on conventional commits.*",
        ]
    )

    return "\n".join(lines)


def main():
    """Main function to generate release notes."""
    if len(sys.argv) < 2:
        print("Usage: python generate_release_notes.py <version> [previous_tag]")
        sys.exit(1)

    version = sys.argv[1]
    previous_tag = sys.argv[2] if len(sys.argv) > 2 else None

    # Get commits since last tag
    commits = get_commits_since_tag(previous_tag)

    if not commits:
        print("No commits found")
        sys.exit(1)

    # Categorize commits
    categories = categorize_commits(commits)

    # Generate release body
    release_body = generate_release_body(version, categories)

    # Output for GitHub Actions
    print(f"release_body<<EOF")
    print(release_body)
    print("EOF")


if __name__ == "__main__":
    main()
