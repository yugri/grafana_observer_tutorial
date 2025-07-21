"""Version management for the Observer application."""

import os
from pathlib import Path


def get_version() -> str:
    """Get the current version from the .version file."""
    version_file = Path(__file__).parent / ".version"

    if version_file.exists():
        with open(version_file, "r") as f:
            version = f.read().strip()
            return version

    # Fallback version if .version file doesn't exist
    return "0.0.0"


def get_app_info() -> dict:
    """Get application information including version."""
    return {
        "title": "Observer - Monitoring Practice",
        "version": get_version(),
        "description": "Observability practice project with FastAPI, Prometheus, and Grafana",
    }


# Export version for easy access
__version__ = get_version()
