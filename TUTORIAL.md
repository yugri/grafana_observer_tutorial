# Observer - Tutorial & Learning Guide

This tutorial will guide you through using the Observer observability project to learn modern monitoring and alerting practices.

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding the Architecture](#understanding-the-architecture)
3. [Using Prometheus](#using-prometheus)
4. [Using Grafana](#using-grafana)
5. [Load Testing & Monitoring](#load-testing--monitoring)
6. [Adding Custom Metrics](#adding-custom-metrics)
7. [Alerting & Notifications](#alerting--notifications)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Topics](#advanced-topics)

## 🚀 Getting Started

### Prerequisites

Before starting this tutorial, ensure you have:
- Docker and Docker Compose installed
- Basic understanding of Python and web APIs
- Familiarity with command line tools

### Initial Setup

1. **Start the observability stack:**
   ```bash
   ./start.sh
   ```

2. **Verify all services are running:**
   ```bash
   docker compose ps
   ```

3. **Test the application:**
   ```bash
   curl http://localhost:8000/
   ```

## 🏗️ Understanding the Architecture

### Components Overview

**FastAPI Application (`main.py`)**
- Web application that generates metrics
- Exposes `/metrics` endpoint for Prometheus scraping
- Simulates various workloads and errors

**Prometheus (`prometheus.yml`)**
- Time-series database for metrics storage
- Scrapes metrics from the application every 15 seconds
- Evaluates alerting rules

**Grafana (`grafana/provisioning/`)**
- Visualization platform for metrics
- Pre-configured dashboards and datasources
- Real-time monitoring interface

### Data Flow

```
User Request → FastAPI App → Metrics Collection → Prometheus → Grafana Dashboard
```

## 🔍 Using Prometheus

### Accessing Prometheus

1. **Open Prometheus UI:** http://localhost:9090
2. **Navigate to Query tab** (default view)

### Basic Queries

Start with these fundamental queries:

#### 1. Check Service Health
```promql
up
```
**What it shows:** Which targets are healthy (value = 1) or down (value = 0)

#### 2. View All HTTP Requests
```promql
http_requests_total
```
**What it shows:** Total count of HTTP requests by endpoint, method, and status

#### 3. Calculate Request Rate
```promql
rate(http_requests_total[5m])
```
**What it shows:** Requests per second over the last 5 minutes

#### 4. View Error Counts
```promql
http_errors_total
```
**What it shows:** Total number of errors by endpoint

#### 5. Check Active Connections
```promql
active_connections
```
**What it shows:** Current number of active connections

### Advanced Queries

#### Response Time Percentiles
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```
**What it shows:** 95th percentile response time

#### Error Rate by Endpoint
```promql
rate(http_errors_total[5m])
```
**What it shows:** Error rate per second by endpoint

#### Success Rate
```promql
rate(http_requests_total{status="200"}[5m]) / rate(http_requests_total[5m])
```
**What it shows:** Percentage of successful requests

### Using the Query Interface

1. **Enter your query** in the query box
2. **Set time range** (top right):
   - "Last 15 minutes" for recent activity
   - "Last 1 hour" for broader view
   - "Last 6 hours" for longer trends
3. **Click "Execute"** or press Enter
4. **View results** in table or graph format

### Tips for Effective Querying

- **Use time ranges** that match your data collection period
- **Start with simple queries** and build complexity
- **Use labels** to filter specific endpoints: `http_requests_total{endpoint="/simulate"}`
- **Combine queries** with operators: `rate(http_requests_total[5m]) * 60` (requests per minute)

## 📊 Using Grafana

### Accessing Grafana

1. **Open Grafana:** http://localhost:3000
2. **Login:** admin/admin
3. **Navigate to Dashboards**

### Application Overview Dashboard

The pre-configured dashboard includes:

#### Top Row - Key Metrics
- **Request Rate:** Current requests per second
- **Error Rate:** Current errors per second
- **Active Connections:** Real-time connection count
- **Response Time (95th percentile):** Performance indicator

#### Middle Row - Detailed Views
- **Request Rate by Endpoint:** Traffic distribution
- **Response Time Distribution:** Performance heatmap

#### Bottom Row - Error Analysis
- **Error Rate by Endpoint:** Error distribution

### Dashboard Features

#### Time Range Controls
- **Quick ranges:** Last 15m, 1h, 6h, 1d
- **Custom ranges:** Set specific start/end times
- **Auto-refresh:** Updates every 5 seconds

#### Panel Interactions
- **Hover tooltips:** Detailed metric information
- **Legend clicks:** Show/hide specific series
- **Panel options:** Fullscreen, inspect, edit

### Creating Custom Dashboards

1. **Click "+" → "Dashboard"**
2. **Add panels** with "Add panel"
3. **Configure data source** (Prometheus)
4. **Write queries** using PromQL
5. **Save dashboard**

## 🧪 Load Testing & Monitoring

### Understanding Load Test Modes

#### Normal Load
```bash
python load_test.py --mode normal --duration 30
```
- **Purpose:** Simulate regular traffic
- **Pattern:** Mix of endpoints with realistic distribution
- **Expected:** Low error rates, consistent response times

#### Error Load
```bash
python load_test.py --mode error --duration 20
```
- **Purpose:** Test error handling and monitoring
- **Pattern:** High percentage of error endpoints
- **Expected:** Elevated error rates, potential alerts

#### Burst Load
```bash
python load_test.py --mode burst --duration 10
```
- **Purpose:** Test system under high traffic
- **Pattern:** Sudden traffic spikes
- **Expected:** Increased response times, connection spikes

#### Mixed Load
```bash
python load_test.py --mode mixed --duration 60
```
- **Purpose:** Realistic traffic simulation
- **Pattern:** Combination of all modes
- **Expected:** Varied metrics, good for learning

### Monitoring During Load Tests

#### What to Watch

1. **Request Rate:** Should match your RPS setting
2. **Error Rate:** Should spike during error mode
3. **Response Time:** Should increase under load
4. **Active Connections:** Should reflect concurrent requests

#### Real-time Monitoring

1. **Open Grafana dashboard** in one window
2. **Run load test** in another terminal
3. **Observe metrics** updating in real-time
4. **Check Prometheus alerts** for triggered conditions

### Analyzing Results

#### Load Test Summary
The script provides:
- **Total requests** and success/error counts
- **Response time statistics** (avg, median, 95th percentile)
- **Endpoint breakdown** with success rates

#### Cross-referencing with Metrics
Compare script output with:
- **Prometheus queries** for the same time period
- **Grafana dashboard** trends
- **Alert history** in Prometheus

## 🔧 Adding Custom Metrics

### Understanding Metric Types

#### Counter
```python
from prometheus_client import Counter

# Counts events (only increases)
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
```

#### Gauge
```python
from prometheus_client import Gauge

# Current value (can increase or decrease)
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')
```

#### Histogram
```python
from prometheus_client import Histogram

# Measures distribution of values
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
```

### Adding a Custom Metric

1. **Define the metric** at module level:
   ```python
   CUSTOM_METRIC = Counter('custom_events_total', 'Custom events', ['event_type'])
   ```

2. **Update the metric** in your endpoint:
   ```python
   @app.get("/custom")
   async def custom_endpoint():
       CUSTOM_METRIC.labels(event_type="api_call").inc()
       return {"message": "Custom event recorded"}
   ```

3. **Test the metric**:
   ```bash
   curl http://localhost:8000/custom
   curl http://localhost:8000/metrics | grep custom_events_total
   ```

### Best Practices

- **Use descriptive names:** `user_login_attempts_total` not `counter1`
- **Add labels** for filtering: `['user_type', 'status']`
- **Include units** in names: `request_duration_seconds`
- **Document metrics** with help text

## 🔔 Alerting & Notifications

### Understanding Alert Rules

#### Rule Structure
```yaml
- alert: HighErrorRate
  expr: rate(http_errors_total[5m]) > 0.1
  for: 2m
  labels:
    severity: warning
  annotations:
    summary: "High error rate detected"
```

#### Components Explained
- **`alert`:** Unique name for the alert
- **`expr`:** PromQL expression that triggers the alert
- **`for`:** Duration the condition must be true
- **`labels`:** Metadata for alert routing
- **`annotations`:** Human-readable descriptions

### Current Alert Rules

#### HighErrorRate
- **Trigger:** Error rate > 0.1 req/s for 2 minutes
- **Purpose:** Detect application issues
- **Severity:** Warning

#### HighResponseTime
- **Trigger:** 95th percentile response time > 2s for 2 minutes
- **Purpose:** Detect performance degradation
- **Severity:** Warning

#### HighActiveConnections
- **Trigger:** Active connections > 20 for 1 minute
- **Purpose:** Detect resource exhaustion
- **Severity:** Warning

#### ServiceDown
- **Trigger:** Application down for 30 seconds
- **Purpose:** Detect service failures
- **Severity:** Critical

### Testing Alerts

1. **Generate error conditions:**
   ```bash
   python load_test.py --mode error --duration 30
   ```

2. **Check alert status:**
   - Go to http://localhost:9090/alerts
   - Look for "firing" alerts

3. **Monitor alert lifecycle:**
   - **Pending:** Condition met, waiting for `for` duration
   - **Firing:** Alert active and sending notifications
   - **Resolved:** Condition no longer met

### Customizing Alerts

#### Adding New Alerts
1. **Edit** `prometheus/alerts.yml`
2. **Add new rule** following the structure above
3. **Restart Prometheus:**
   ```bash
   docker compose restart prometheus
   ```

#### Example: Low Success Rate Alert
```yaml
- alert: LowSuccessRate
  expr: rate(http_requests_total{status="200"}[5m]) / rate(http_requests_total[5m]) < 0.95
  for: 1m
  labels:
    severity: warning
  annotations:
    summary: "Low success rate detected"
    description: "Success rate is {{ $value | humanizePercentage }}"
```

## 🐛 Troubleshooting

### Common Issues

#### Prometheus Can't Scrape Metrics
**Symptoms:** Target shows as "DOWN" in Prometheus
**Causes:**
- Application not running
- Network connectivity issues
- Incorrect metrics endpoint

**Solutions:**
```bash
# Check application status
curl http://localhost:8000/health

# Check metrics endpoint
curl http://localhost:8000/metrics

# Check Prometheus target
curl http://localhost:9090/api/v1/targets
```

#### No Data in Grafana
**Symptoms:** Dashboard shows "No data"
**Causes:**
- Prometheus not collecting data
- Time range too narrow
- Query syntax errors

**Solutions:**
```bash
# Check Prometheus data
curl "http://localhost:9090/api/v1/query?query=up"

# Verify time range in Grafana
# Check query syntax in dashboard panels
```

#### High Response Times
**Symptoms:** Response times > 2 seconds
**Causes:**
- Application overload
- Blocking operations
- Resource constraints

**Solutions:**
```bash
# Check application logs
docker compose logs app

# Monitor resource usage
docker stats

# Optimize application code
```

### Debugging Techniques

#### Check Application Logs
```bash
# Real-time logs
docker compose logs -f app

# Recent logs
docker compose logs --tail=100 app
```

#### Verify Metrics Collection
```bash
# Check raw metrics
curl http://localhost:8000/metrics

# Test specific metric
curl "http://localhost:9090/api/v1/query?query=http_requests_total"
```

#### Validate Configuration
```bash
# Check Prometheus config
docker compose exec prometheus cat /etc/prometheus/prometheus.yml

# Check Grafana config
docker compose exec grafana cat /etc/grafana/grafana.ini
```

## 🚀 Advanced Topics

### Custom Dashboards

#### Creating Application-Specific Dashboards
1. **Identify key metrics** for your use case
2. **Design panel layout** for effective monitoring
3. **Use appropriate visualizations:**
   - **Time series** for trends
   - **Stat panels** for current values
   - **Heatmaps** for distributions
   - **Tables** for detailed data

#### Dashboard Best Practices
- **Group related metrics** in panels
- **Use consistent time ranges** across panels
- **Add meaningful titles** and descriptions
- **Include thresholds** for visual alerts
- **Optimize refresh rates** for performance

### PromQL Advanced Queries

#### Aggregation Functions
```promql
# Sum across all instances
sum(rate(http_requests_total[5m]))

# Average response time
avg(rate(http_request_duration_seconds_sum[5m])) / avg(rate(http_request_duration_seconds_count[5m]))

# Top 3 endpoints by request rate
topk(3, rate(http_requests_total[5m]))
```

#### Conditional Logic
```promql
# Error rate only for specific endpoints
rate(http_errors_total{endpoint=~"/api/.*"}[5m])

# Success rate with condition
rate(http_requests_total{status="200"}[5m]) / rate(http_requests_total[5m]) > 0.95
```

### Performance Optimization

#### Application Level
- **Use async operations** instead of blocking calls
- **Implement connection pooling** for databases
- **Cache frequently accessed data**
- **Optimize metric collection** overhead

#### Monitoring Level
- **Adjust scrape intervals** based on needs
- **Use metric relabeling** to reduce cardinality
- **Implement metric filtering** for high-volume endpoints
- **Optimize query performance** with proper time ranges

### Integration with External Systems

#### Alert Manager
- **Install AlertManager** for notification routing
- **Configure notification channels** (email, Slack, PagerDuty)
- **Set up alert grouping** and silencing rules

#### Log Aggregation
- **Integrate with ELK stack** or similar
- **Correlate metrics with logs** for debugging
- **Set up log-based alerts** for critical events

#### CI/CD Integration
- **Add monitoring to deployment pipelines**
- **Implement health checks** for new deployments
- **Set up automated testing** of monitoring systems

## 📚 Additional Resources

### Documentation
- [Prometheus Query Language (PromQL)](https://prometheus.io/docs/prometheus/latest/querying/)
- [Grafana Dashboard Documentation](https://grafana.com/docs/grafana/latest/dashboards/)
- [FastAPI Monitoring Best Practices](https://fastapi.tiangolo.com/tutorial/middleware/)

### Learning Paths
1. **Start with basic queries** and dashboard navigation
2. **Practice load testing** and observe metric changes
3. **Experiment with custom metrics** and alerts
4. **Build custom dashboards** for specific use cases
5. **Explore advanced PromQL** and optimization techniques

### Community Resources
- [Prometheus Community](https://prometheus.io/community/)
- [Grafana Community](https://community.grafana.com/)
- [Observability Best Practices](https://sre.google/sre-book/monitoring-distributed-systems/)

---

**Happy Monitoring! 🚀**

This tutorial provides a foundation for understanding observability. Continue experimenting with different scenarios and configurations to deepen your knowledge.
