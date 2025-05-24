#!/bin/bash

# CryptaNet System Startup Script
# This script starts all components of the CryptaNet system in the correct order

echo "🚀 Starting CryptaNet Blockchain Supply Chain Management System..."

# Function to check if a service is running
check_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to start..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        echo "   Attempt $attempt/$max_attempts - waiting for $service_name..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to start after $max_attempts attempts"
    return 1
}

# Kill any existing processes on required ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:5002 | xargs kill -9 2>/dev/null || true
lsof -ti:5003 | xargs kill -9 2>/dev/null || true
lsof -ti:5004 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start Blockchain Network (if not already running)
echo "⛓️ Checking blockchain network..."
if ! docker ps | grep -q "peer0.org1.example.com"; then
    echo "Starting blockchain network..."
    cd /Users/bhaskar/Desktop/CryptaNet/blockchain/docker
    docker-compose up -d
    sleep 10
else
    echo "✅ Blockchain network is already running"
fi

# Start Privacy Layer Service
echo "🔐 Starting Privacy Layer Service (Port 5003)..."
cd /Users/bhaskar/Desktop/CryptaNet/privacy_layer
python3 privacy_server.py &
PRIVACY_PID=$!

# Start Anomaly Detection Service
echo "🔍 Starting Anomaly Detection Service (Port 5002)..."
cd /Users/bhaskar/Desktop/CryptaNet/anomaly_detection
python3 simple_api_server.py &
ANOMALY_PID=$!

# Wait for privacy layer and anomaly detection to be ready
check_service "http://localhost:5003/health" "Privacy Layer"
check_service "http://localhost:5002/health" "Anomaly Detection"

# Start Backend Service
echo "🖥️ Starting Backend Service (Port 5004)..."
cd /Users/bhaskar/Desktop/CryptaNet/backend
python3 simple_backend.py &
BACKEND_PID=$!

# Wait for backend to be ready
check_service "http://localhost:5004/health" "Backend"

# Start Frontend Service
echo "🌐 Starting Frontend Service (Port 3000)..."
cd /Users/bhaskar/Desktop/CryptaNet/frontend
npm start &
FRONTEND_PID=$!

# Wait for frontend to be ready
check_service "http://localhost:3000" "Frontend"

echo ""
echo "🎉 CryptaNet System Successfully Started!"
echo ""
echo "📊 Service Status:"
echo "   🔐 Privacy Layer:      http://localhost:5003/health"
echo "   🔍 Anomaly Detection:  http://localhost:5002/health"
echo "   🖥️ Backend API:        http://localhost:5004/health"
echo "   🌐 Frontend Dashboard: http://localhost:3000"
echo ""
echo "🔑 Test Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📝 Process IDs:"
echo "   Privacy Layer: $PRIVACY_PID"
echo "   Anomaly Detection: $ANOMALY_PID"
echo "   Backend: $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "🛑 To stop all services, run:"
echo "   kill $PRIVACY_PID $ANOMALY_PID $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop monitoring, or run 'jobs' to see running background processes"

# Keep script running and monitor services
while true; do
    sleep 30
    echo "📊 $(date): Services monitoring..."
    
    # Check if services are still running
    if ! curl -s http://localhost:5003/health > /dev/null; then
        echo "⚠️ Privacy Layer service down!"
    fi
    
    if ! curl -s http://localhost:5002/health > /dev/null; then
        echo "⚠️ Anomaly Detection service down!"
    fi
    
    if ! curl -s http://localhost:5004/health > /dev/null; then
        echo "⚠️ Backend service down!"
    fi
    
    if ! curl -s http://localhost:3000 > /dev/null; then
        echo "⚠️ Frontend service down!"
    fi
done
