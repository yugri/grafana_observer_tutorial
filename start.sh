#!/bin/bash

# Observer - Observability Stack Startup Script

echo "🚀 Starting Observer - Observability Practice Project"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker compose ps

echo ""
echo "✅ Services are starting up!"
echo ""
echo "🌐 Access your services:"
echo "   Application API: http://localhost:8000"
echo "   Prometheus:      http://localhost:9090"
echo "   Grafana:         http://localhost:3000 (admin/admin)"
echo ""
echo "📊 To generate load for testing:"
echo "   python load_test.py --mode mixed --duration 120"
echo ""
echo "📋 To view logs:"
echo "   docker compose logs -f app"
echo ""
echo "🛑 To stop services:"
echo "   docker compose down"
