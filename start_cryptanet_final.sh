#!/bin/bash

echo "🚀 Starting CryptaNet System - Final Version"

# Function to wait for service
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s $url > /dev/null 2>&1; then
            echo "✅ $name is ready"
            return 0
        fi
        echo "⏳ Waiting for $name... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "⚠️  $name failed to start after $max_attempts attempts"
    return 1
}

# Clean up existing processes
echo "🧹 Cleaning up existing services..."
pkill -f "python.*api" 2>/dev/null || true
pkill -f "python.*server" 2>/dev/null || true  
pkill -f "python.*backend" 2>/dev/null || true
pkill -f "npm.*start" 2>/dev/null || true
sleep 3

# Start Privacy Layer Service
echo "🔐 Starting Privacy Layer Service..."
cd /Users/bhaskar/Desktop/CryptaNet/privacy_layer
python3 privacy_server.py > /dev/null 2>&1 &
PRIVACY_PID=$!
echo "Privacy Layer started (PID: $PRIVACY_PID)"

# Start Anomaly Detection Service  
echo "🤖 Starting Anomaly Detection Service..."
cd /Users/bhaskar/Desktop/CryptaNet/anomaly_detection
python3 simple_api_server.py > /dev/null 2>&1 &
ANOMALY_PID=$!
echo "Anomaly Detection started (PID: $ANOMALY_PID)"

# Start Backend Service
echo "🖥️  Starting Backend Service..."
cd /Users/bhaskar/Desktop/CryptaNet/backend
python3 simple_backend.py > /dev/null 2>&1 &
BACKEND_PID=$!
echo "Backend Service started (PID: $BACKEND_PID)"

# Wait for backend services to be ready
echo "⏳ Waiting for services to initialize..."
wait_for_service "http://localhost:5003/health" "Privacy Layer"
wait_for_service "http://localhost:5002/health" "Anomaly Detection"  
wait_for_service "http://localhost:5004/health" "Backend API"

# Start Frontend
echo "🌐 Starting Frontend Dashboard..."
cd /Users/bhaskar/Desktop/CryptaNet/frontend
PORT=3000 npm start > /dev/null 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to initialize..."
wait_for_service "http://localhost:3000" "Frontend Dashboard"

# Add sample data to demonstrate functionality
echo "📊 Adding sample supply chain data..."

# Sample 1: Coffee Beans
curl -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "product": "Premium Coffee Beans",
      "quantity": 1000,
      "location": "Warehouse A - Section 1",
      "temperature": 22.5,
      "humidity": 65.0,
      "timestamp": "2025-05-24T22:00:00Z"
    }
  }' > /dev/null 2>&1

# Sample 2: Electronic Components
curl -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -d '{
    "organizationId": "Org1MSP", 
    "dataType": "supply_chain",
    "data": {
      "product": "Electronic Components",
      "quantity": 500,
      "location": "Warehouse B - Section 2",
      "temperature": 20.0,
      "humidity": 45.0,
      "timestamp": "2025-05-24T22:05:00Z"
    }
  }' > /dev/null 2>&1

# Sample 3: Pharmaceutical Products
curl -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain", 
    "data": {
      "product": "Pharmaceutical Products",
      "quantity": 250,
      "location": "Cold Storage - Section 3",
      "temperature": 18.0,
      "humidity": 40.0,
      "timestamp": "2025-05-24T22:10:00Z"
    }
  }' > /dev/null 2>&1

# Sample 4: Anomaly Test (High Temperature)
curl -X POST http://localhost:5004/api/supply-chain/submit \
  -H "Content-Type: application/json" \
  -d '{
    "organizationId": "Org1MSP",
    "dataType": "supply_chain",
    "data": {
      "product": "Temperature Sensitive Item",
      "quantity": 100,
      "location": "Warehouse C - Section 4",
      "temperature": 45.0,
      "humidity": 80.0,
      "timestamp": "2025-05-24T22:15:00Z"
    }
  }' > /dev/null 2>&1

sleep 3

# Verify system status
echo ""
echo "🔍 System Status Check:"
echo "----------------------------------------"

# Check all services
PRIVACY_STATUS=$(curl -s http://localhost:5003/health | jq -r '.status // "unhealthy"' 2>/dev/null || echo "unhealthy")
ANOMALY_STATUS=$(curl -s http://localhost:5002/health | jq -r '.status // "unhealthy"' 2>/dev/null || echo "unhealthy")
BACKEND_STATUS=$(curl -s http://localhost:5004/health | jq -r '.status // "unhealthy"' 2>/dev/null || echo "unhealthy")

echo "Privacy Layer: $PRIVACY_STATUS"
echo "Anomaly Detection: $ANOMALY_STATUS"
echo "Backend API: $BACKEND_STATUS"

# Check data count
DATA_COUNT=$(curl -s http://localhost:5004/api/supply-chain/query | jq -r '.count // 0' 2>/dev/null || echo "0")
echo "Sample Data Records: $DATA_COUNT"

echo ""
echo "🎉 CryptaNet System Successfully Started!"
echo "----------------------------------------"
echo "📋 Access Information:"
echo "   🌐 Frontend Dashboard: http://localhost:3000"
echo "   🔗 Backend API: http://localhost:5004" 
echo "   🔑 Login Credentials: admin / admin123"
echo ""
echo "📊 Process Information:"
echo "   Privacy Layer PID: $PRIVACY_PID"
echo "   Anomaly Detection PID: $ANOMALY_PID"
echo "   Backend API PID: $BACKEND_PID"
echo "   Frontend Dashboard PID: $FRONTEND_PID"
echo ""
echo "🛑 To stop all services:"
echo "   pkill -f 'python.*api'; pkill -f 'python.*server'; pkill -f 'python.*backend'; pkill -f 'npm.*start'"
echo ""
echo "✨ System is ready! Open http://localhost:3000 and login with admin/admin123"

