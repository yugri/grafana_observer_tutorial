#!/usr/bin/env python3
"""
Script to explore available metrics in Prometheus
"""

import requests


def get_metrics():
    """Get list of all available metrics"""
    try:
        response = requests.get("http://localhost:9090/api/v1/label/__name__/values")
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            print(f"Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error connecting to Prometheus: {e}")
        return []


def get_metric_values(metric_name):
    """Get current values for a specific metric"""
    try:
        response = requests.get(
            f"http://localhost:9090/api/v1/query?query={metric_name}"
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("result", [])
        else:
            print(f"Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error querying metric {metric_name}: {e}")
        return []


def main():
    print("🔍 Exploring Prometheus Metrics")
    print("=" * 50)

    # Get all available metrics
    metrics = get_metrics()

    if not metrics:
        print("❌ No metrics found. Make sure Prometheus is running and scraping data.")
        return

    print(f"📊 Found {len(metrics)} metrics:")
    print()

    # Filter and display relevant metrics
    relevant_metrics = [
        "up",
        "http_requests_total",
        "http_errors_total",
        "http_request_duration_seconds",
        "active_connections",
        "python_gc_collections_total",
        "process_cpu_seconds_total",
        "process_resident_memory_bytes",
    ]

    for metric in relevant_metrics:
        if metric in metrics:
            print(f"✅ {metric}")
            values = get_metric_values(metric)
            if values:
                print(f"   📈 Current values: {len(values)} series")
                # Show a sample
                if len(values) > 0:
                    sample = values[0]
                    if "metric" in sample:
                        labels = sample["metric"]
                        # Remove __name__ from labels for cleaner display
                        labels.pop("__name__", None)
                        print(f"   📋 Sample labels: {labels}")
            else:
                print("   ⚠️  No current values")
            print()

    print("🌐 To explore in Prometheus web UI:")
    print("   1. Go to http://localhost:9090")
    print("   2. Enter a query like: http_requests_total")
    print("   3. Set time range to 'Last 1 hour'")
    print("   4. Click 'Execute'")
    print()
    print("📝 Useful queries to try:")
    print("   • up")
    print("   • http_requests_total")
    print("   • rate(http_requests_total[5m])")
    print("   • http_errors_total")
    print("   • active_connections")
    print(
        "   • histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
    )


if __name__ == "__main__":
    main()
