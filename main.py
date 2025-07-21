import asyncio
import os
import random
import time
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# Load environment variables
load_dotenv()

app = FastAPI(title="Observer - Monitoring Practice", version="1.0.0")

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency")
ACTIVE_CONNECTIONS = Gauge("active_connections", "Number of active connections")
ERROR_RATE = Counter("http_errors_total", "Total HTTP errors", ["endpoint"])

# Simulated application state
active_connections = 0


@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()

    # Increment active connections
    global active_connections
    active_connections += 1
    ACTIVE_CONNECTIONS.set(active_connections)

    try:
        response = await call_next(request)

        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        # Track errors based on HTTP status codes (4xx and 5xx)
        if response.status_code >= 400:
            ERROR_RATE.labels(endpoint=request.url.path).inc()

        REQUEST_LATENCY.observe(time.time() - start_time)

        return response
    except Exception:
        # Track errors from exceptions
        ERROR_RATE.labels(endpoint=request.url.path).inc()

        # Still record the request as an error
        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.url.path, status=500
        ).inc()

        REQUEST_LATENCY.observe(time.time() - start_time)
        raise
    finally:
        # Decrement active connections
        active_connections -= 1
        ACTIVE_CONNECTIONS.set(active_connections)


@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "Observer - Monitoring Practice API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "simulate": "/simulate",
            "error": "/error",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "active_connections": active_connections,
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/simulate")
async def simulate_workload():
    """Simulate various workloads for testing monitoring"""
    # Simulate some processing time
    await asyncio.sleep(random.uniform(0.1, 0.5))

    # 10% chance of error
    if random.random() < 0.1:
        raise HTTPException(status_code=500, detail="Simulated error")

    return {
        "message": "Workload simulation completed",
        "duration": random.uniform(0.1, 0.5),
        "timestamp": time.time(),
    }


@app.get("/error")
async def trigger_error():
    """Intentionally trigger an error for testing error monitoring"""
    raise HTTPException(status_code=500, detail="Intentional error for testing")


@app.get("/config")
async def get_config():
    """Get current application configuration"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "version": "1.0.0",
    }


@app.get("/test-feature")
async def test_feature():
    """Test endpoint for conventional commits demo."""
    return {
        "message": "This is a test feature for conventional commits!",
        "timestamp": datetime.now().isoformat(),
        "feature": "conventional-commits-demo",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
