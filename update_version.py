#!/usr/bin/env python3
"""Script to update version in pyproject.toml to match .version file."""

import re
from pathlib import Path

from version import get_version


def update_pyproject_version():
    """Update the version in pyproject.toml to match .version file."""
    pyproject_path = Path("pyproject.toml")
    version = get_version()

    if not pyproject_path.exists():
        print("pyproject.toml not found!")
        return

    # Read the current content
    with open(pyproject_path, "r") as f:
        content = f.read()

    # Update the version line
    pattern = r'version = "([^"]*)"'
    replacement = f'version = "{version}"'

    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)

        # Write back the updated content
        with open(pyproject_path, "w") as f:
            f.write(new_content)

        print(f"Updated pyproject.toml version to {version}")
    else:
        print("Could not find version line in pyproject.toml")


if __name__ == "__main__":
    update_pyproject_version()
