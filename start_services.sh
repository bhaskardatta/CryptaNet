#!/bin/bash

# CryptaNet Services Startup Script

echo "Starting CryptaNet Services..."

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "Port $port is already in use"
        return 1
    else
        echo "Port $port is available"
        return 0
    fi
}

# Kill any existing processes
echo "Cleaning up existing processes..."
pkill -f "python.*api" 2>/dev/null || true
pkill -f "python.*server" 2>/dev/null || true  
pkill -f "python.*backend" 2>/dev/null || true
sleep 3

# Start Anomaly Detection Service (Port 5002) - Use simple API
echo "Starting Anomaly Detection Service on port 5002..."
cd /Users/bhaskar/Desktop/CryptaNet/anomaly_detection
PORT=5002 python3 simple_api_server.py &
ANOMALY_PID=$!
echo "Anomaly Detection started with PID: $ANOMALY_PID"

# Wait for service to start
sleep 5

# Start Privacy Layer Service (Port 5003)
echo "Starting Privacy Layer Service on port 5003..."
cd /Users/bhaskar/Desktop/CryptaNet/privacy_layer
PORT=5003 python3 privacy_server.py &
PRIVACY_PID=$!
echo "Privacy Layer started with PID: $PRIVACY_PID"

# Wait for service to start
sleep 5

# Start Backend Service (Port 5004)
echo "Starting Backend Service on port 5004..."
cd /Users/bhaskar/Desktop/CryptaNet/backend
python3 simple_backend.py &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait for service to start
sleep 5

# Test all services
echo "Testing services..."

echo "Testing Anomaly Detection Service:"
curl -s http://localhost:5002/health | python3 -m json.tool || echo "Anomaly Detection service not responding"

echo "Testing Privacy Layer Service:"
curl -s http://localhost:5003/health | python3 -m json.tool || echo "Privacy Layer service not responding"

echo "Testing Backend Service:"
curl -s http://localhost:5004/health | python3 -m json.tool || echo "Backend service not responding"

echo ""
echo "All services started!"
echo "Process IDs:"
echo "  Anomaly Detection: $ANOMALY_PID"
echo "  Privacy Layer: $PRIVACY_PID" 
echo "  Backend: $BACKEND_PID"
echo ""
echo "To stop all services, run:"
echo "  pkill -f 'python.*api'; pkill -f 'python.*server'; pkill -f 'python.*backend'"
echo ""
echo "You can now start the frontend with:"
echo "  cd /Users/bhaskar/Desktop/CryptaNet/frontend"
echo "  PORT=3001 npm start"
echo ""
echo "Test the system with:"
echo "  curl -X POST http://localhost:5004/api/supply-chain/submit -H 'Content-Type: application/json' -d '{\"organizationId\":\"Org1MSP\",\"dataType\":\"supply_chain\",\"data\":{\"product\":\"Coffee\",\"quantity\":100,\"temperature\":22.5}}'"