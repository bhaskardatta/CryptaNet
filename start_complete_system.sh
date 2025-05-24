#!/bin/bash

echo "🚀 Starting CryptaNet Complete System..."

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "Port $port is in use"
        return 1
    else
        echo "Port $port is available"
        return 0
    fi
}

# Kill existing services
echo "🔄 Cleaning up existing services..."
pkill -f "python.*api" 2>/dev/null || true
pkill -f "python.*server" 2>/dev/null || true
pkill -f "python.*backend" 2>/dev/null || true
pkill -f "npm.*start" 2>/dev/null || true
sleep 3

# Start backend services
echo "🔧 Starting Backend Services..."

# Start Privacy Layer
cd /Users/bhaskar/Desktop/CryptaNet/privacy_layer
python3 privacy_server.py &
PRIVACY_PID=$!
echo "Privacy Layer started (PID: $PRIVACY_PID)"

# Start Anomaly Detection
cd /Users/bhaskar/Desktop/CryptaNet/anomaly_detection
python3 simple_api_server.py &
ANOMALY_PID=$!
echo "Anomaly Detection started (PID: $ANOMALY_PID)"

# Start Backend API
cd /Users/bhaskar/Desktop/CryptaNet/backend
python3 simple_backend.py &
BACKEND_PID=$!
echo "Backend API started (PID: $BACKEND_PID)"

# Wait for services to start
sleep 5

# Start Frontend
echo "🌐 Starting Frontend..."
cd /Users/bhaskar/Desktop/CryptaNet/frontend
PORT=3000 npm start &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

# Wait for services to initialize
echo "⏳ Waiting for services to initialize..."
sleep 10

# Test services
echo "🧪 Testing Services..."
echo "Backend API: $(curl -s http://localhost:5004/health | jq -r '.status // "unhealthy"')"
echo "Privacy Layer: $(curl -s http://localhost:5003/health | jq -r '.status // "unhealthy"')"
echo "Anomaly Detection: $(curl -s http://localhost:5002/health | jq -r '.status // "unhealthy"')"

# Add sample data with anomalies
echo "📊 Adding sample data with anomalies..."
bash /Users/bhaskar/Desktop/CryptaNet/generate_sample_data_with_anomalies.sh

echo ""
echo "🎉 CryptaNet System Started Successfully!"
echo ""
echo "📋 Access Information:"
echo "   Frontend Dashboard: http://localhost:3000"
echo "   Backend API: http://localhost:5004"
echo "   Login Credentials: admin / admin123"
echo ""
echo "📊 Process IDs:"
echo "   Privacy Layer: $PRIVACY_PID"
echo "   Anomaly Detection: $ANOMALY_PID"  
echo "   Backend API: $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "🛑 To stop all services:"
echo "   pkill -f 'python.*api'; pkill -f 'python.*server'; pkill -f 'python.*backend'; pkill -f 'npm.*start'"
echo ""

