# Observer - Observability Practice Project

A comprehensive observability practice project using FastAPI, Prometheus, and Grafana to demonstrate modern monitoring and alerting practices.

## 🚀 Features

- **FastAPI Application** with built-in Prometheus metrics
- **Prometheus** for metrics collection and alerting
- **Grafana** for visualization and dashboards
- **Docker Compose** for easy deployment
- **Pre-configured dashboards** and alerting rules
- **Simulated workloads** for testing monitoring

## 📊 Metrics Collected

- HTTP request rate and latency
- Error rates by endpoint
- Active connections
- Response time distributions
- Application health status

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI   │───▶│  Prometheus │───▶│   Grafana   │
│  (Port 8000)│    │ (Port 9090) │    │ (Port 3000) │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🛠️ Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd observer
   ```

2. **Start all services:**
   ```bash
   ./start.sh
   ```

3. **Access the services:**
   - **Application API**: http://localhost:8000
   - **Prometheus**: http://localhost:9090
   - **Grafana**: http://localhost:3000 (admin/admin)

## 📈 Application Endpoints

- `GET /` - Application info and available endpoints
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics endpoint
- `GET /simulate` - Simulate workload (with 10% error rate)
- `GET /error` - Trigger intentional error
- `GET /config` - Get current configuration

## 🔔 Alerting Rules

Prometheus is configured with the following alerting rules:

- **HighErrorRate**: Triggers when error rate > 0.1 req/s for 2 minutes
- **HighResponseTime**: Triggers when 95th percentile response time > 2s
- **HighActiveConnections**: Triggers when active connections > 20
- **ServiceDown**: Triggers when application is down for 30 seconds
- **NoRequests**: Triggers when no requests received for 5 minutes

## 📁 Project Structure

```
observer/
├── main.py                 # FastAPI application
├── docker-compose.yml      # Docker services configuration
├── Dockerfile             # Application container
├── prometheus.yml         # Prometheus configuration
├── pyproject.toml         # Python dependencies
├── README.md              # This file
├── TUTORIAL.md            # Detailed tutorial and guides
├── start.sh               # Startup script
├── load_test.py           # Load testing script
├── explore_metrics.py     # Metrics exploration script
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       │   ├── dashboard.yml
│       │   └── application-overview.json
│       └── datasources/
│           └── prometheus.yml
└── prometheus/
    └── alerts.yml         # Alerting rules
```

## 🔧 Configuration

### Environment Variables

- `ENVIRONMENT`: Application environment (default: development)
- `LOG_LEVEL`: Logging level (default: INFO)

### Prometheus Configuration

- Scrape interval: 15s
- Evaluation interval: 15s
- App-specific scrape interval: 15s
- Scrape timeout: 15s

### Grafana Configuration

- Default admin credentials: admin/admin
- Auto-provisioned Prometheus datasource
- Pre-configured "Application Overview" dashboard

## 🧪 Testing

### Load Testing

Generate various traffic patterns:

```bash
# Normal load
python load_test.py --mode normal --duration 30

# Error scenarios
python load_test.py --mode error --duration 20

# Burst traffic
python load_test.py --mode burst --duration 10

# Mixed scenarios
python load_test.py --mode mixed --duration 60
```

### Metrics Exploration

Explore available metrics:

```bash
python explore_metrics.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000, 9090, and 3000 are available
2. **Permission issues**: Run Docker commands with appropriate permissions
3. **Metrics not appearing**: Check that the app is running and accessible

### Logs

View logs for specific services:
```bash
# Application logs
docker compose logs app

# Prometheus logs
docker compose logs prometheus

# Grafana logs
docker compose logs grafana
```

## 📚 Documentation

- **[TUTORIAL.md](TUTORIAL.md)** - Detailed tutorial and usage guides
- **[Prometheus Documentation](https://prometheus.io/docs/)**
- **[Grafana Documentation](https://grafana.com/docs/)**
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
