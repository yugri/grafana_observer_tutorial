#!/usr/bin/env python3
"""
Basic tests for the Observer application
"""

import pytest
from fastapi.testclient import TestClient

from main import app
from version import get_version

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Observer - Monitoring Practice API"
    assert data["version"] == get_version()
    assert "endpoints" in data


def test_health_endpoint():
    """Test the health endpoint returns healthy status"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "active_connections" in data


def test_metrics_endpoint():
    """Test the metrics endpoint returns Prometheus format"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert (
        response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
    )

    # Check for some expected metrics
    content = response.text
    assert "http_requests_total" in content
    assert "active_connections" in content


def test_simulate_endpoint():
    """Test the simulate endpoint (may return error due to randomness)"""
    response = client.get("/simulate")
    # Should return either 200 or 500 (due to 10% error rate)
    assert response.status_code in [200, 500]


def test_error_endpoint():
    """Test the error endpoint returns 500"""
    response = client.get("/error")
    assert response.status_code == 500
    assert response.json()["detail"] == "Intentional error for testing purposes"


def test_config_endpoint():
    """Test the config endpoint returns configuration"""
    response = client.get("/config")
    assert response.status_code == 200

    data = response.json()
    assert "environment" in data
    assert "log_level" in data
    assert "version" in data
    assert data["version"] == get_version()


def test_app_metadata():
    """Test that the app has correct metadata"""
    assert app.title == "Observer - Monitoring Practice"
    assert app.version == get_version()


def test_test_feature_endpoint():
    """Test the new test-feature endpoint."""
    response = client.get("/test-feature")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "timestamp" in data
    assert "feature" in data
    assert data["feature"] == "conventional-commits-demo"


if __name__ == "__main__":
    pytest.main([__file__])
