#!/bin/bash

# Flask Container vs VM Performance Analysis - Setup Script
# This script helps beginners set up the project

echo "🚀 Flask Container vs VM Performance Analysis Setup"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   Visit: https://www.docker.com/get-started"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first:"
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Docker and Python 3 are installed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t flask-container-vm .

# Test the application
echo "🧪 Testing the application..."
docker run -d -p 5000:5000 --name flask-test flask-container-vm
sleep 5

# Check if the application is running
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 Open http://localhost:5000 in your browser"
    echo "📊 Health check: http://localhost:5000/health"
    echo "📈 Metrics: http://localhost:5000/metrics"
else
    echo "❌ Application failed to start"
    docker logs flask-test
    exit 1
fi

echo ""
echo "🎉 Setup complete! Your Flask application is running."
echo ""
echo "📋 Available endpoints:"
echo "   - http://localhost:5000 (main page)"
echo "   - http://localhost:5000/health (health check)"
echo "   - http://localhost:5000/cpu (CPU test)"
echo "   - http://localhost:5000/memory (memory test)"
echo "   - http://localhost:5000/metrics (Prometheus metrics)"
echo ""
echo "🛑 To stop the application:"
echo "   docker stop flask-test"
echo "   docker rm flask-test"
echo ""
echo "📚 Read the README.md for more information!"
