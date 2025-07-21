#!/usr/bin/env python3
"""Script to bump version and update all related files."""

import sys
from pathlib import Path

from update_version import update_pyproject_version


def bump_version(version_type="patch"):
    """Bump version according to semantic versioning."""
    version_file = Path(".version")

    if not version_file.exists():
        print(".version file not found!")
        return

    # Read current version
    with open(version_file, "r") as f:
        current_version = f.read().strip()

    # Parse version components
    parts = current_version.split(".")
    if len(parts) != 3:
        print(f"Invalid version format: {current_version}")
        return

    major, minor, patch = map(int, parts)

    # Bump version according to type
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        print(f"Invalid version type: {version_type}. Use 'major', 'minor', or 'patch'")
        return

    new_version = f"{major}.{minor}.{patch}"

    # Update .version file
    with open(version_file, "w") as f:
        f.write(new_version + "\n")

    # Update pyproject.toml
    update_pyproject_version()

    print(f"Version bumped from {current_version} to {new_version}")
    print("Updated .version and pyproject.toml files")


if __name__ == "__main__":
    version_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    bump_version(version_type)
