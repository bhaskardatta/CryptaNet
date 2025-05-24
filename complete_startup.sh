#!/bin/bash

# CryptaNet Complete System Startup Script
# This script starts all services and ensures they stay running

echo "🚀 Starting CryptaNet Complete System..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS") echo -e "${GREEN}✅ $message${NC}" ;;
        "ERROR") echo -e "${RED}❌ $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}⚠️ $message${NC}" ;;
        "INFO") echo -e "${BLUE}ℹ️ $message${NC}" ;;
    esac
}

# Function to check if a service is running
check_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "INFO" "Waiting for $service_name to start..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            print_status "SUCCESS" "$service_name is ready!"
            return 0
        fi
        echo "   Attempt $attempt/$max_attempts - waiting for $service_name..."
        sleep 2
        ((attempt++))
    done
    
    print_status "ERROR" "$service_name failed to start after $max_attempts attempts"
    return 1
}

# Function to start a service in background
start_service() {
    local service_dir=$1
    local service_command=$2
    local service_name=$3
    
    print_status "INFO" "Starting $service_name..."
    cd "$service_dir"
    $service_command &
    local pid=$!
    echo "$pid" > "/tmp/cryptanet_${service_name,,}_pid"
    print_status "SUCCESS" "$service_name started with PID $pid"
}

# Kill any existing processes on required ports
print_status "INFO" "Cleaning up existing processes..."
for port in 3000 5002 5003 5004; do
    if lsof -ti:$port > /dev/null 2>&1; then
        print_status "WARNING" "Killing existing process on port $port"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
    fi
done

# Check blockchain network
print_status "INFO" "Checking blockchain network..."
if ! docker ps | grep -q "peer0.org1.example.com"; then
    print_status "WARNING" "Starting blockchain network..."
    cd /Users/bhaskar/Desktop/CryptaNet/blockchain/docker
    docker-compose up -d
    sleep 15
else
    print_status "SUCCESS" "Blockchain network is already running"
fi

# Start Privacy Layer Service
start_service "/Users/bhaskar/Desktop/CryptaNet/privacy_layer" "python3 privacy_server.py" "Privacy_Layer"

# Start Anomaly Detection Service
start_service "/Users/bhaskar/Desktop/CryptaNet/anomaly_detection" "python3 simple_api_server.py" "Anomaly_Detection"

# Wait for dependencies to be ready
check_service "http://localhost:5003/health" "Privacy Layer" || exit 1
check_service "http://localhost:5002/health" "Anomaly Detection" || exit 1

# Start Backend Service
start_service "/Users/bhaskar/Desktop/CryptaNet/backend" "python3 simple_backend.py" "Backend"

# Wait for backend to be ready
check_service "http://localhost:5004/health" "Backend" || exit 1

# Start Frontend Service
print_status "INFO" "Starting Frontend Service..."
cd /Users/bhaskar/Desktop/CryptaNet/frontend
npm start &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "/tmp/cryptanet_frontend_pid"

# Wait for frontend to be ready
check_service "http://localhost:3000" "Frontend" || exit 1

echo ""
print_status "SUCCESS" "🎉 CryptaNet System Successfully Started!"
echo ""
echo "📊 Service Status:"
echo "   🔐 Privacy Layer:      http://localhost:5003/health"
echo "   🔍 Anomaly Detection:  http://localhost:5002/health"
echo "   🖥️ Backend API:        http://localhost:5004/health"
echo "   🌐 Frontend Dashboard: http://localhost:3000"
echo ""
echo "🔑 Login Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📝 Service PIDs saved in /tmp/cryptanet_*_pid files"
echo ""

# Add some test data to the system
print_status "INFO" "Adding sample data to the system..."

# Get authentication token
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:5004/api/auth/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin123"}')
TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"token": "[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    print_status "SUCCESS" "Authentication successful"
    
    # Add sample data
    curl -s -X POST http://localhost:5004/api/supply-chain/submit \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
        "productId": "LAPTOP001",
        "organizationId": "Org1MSP",
        "location": "Manufacturing Plant A",
        "temperature": 22.5,
        "humidity": 45.0,
        "timestamp": "2025-05-24T10:30:00Z",
        "batchNumber": "LP001",
        "quality": "A",
        "metadata": {
            "supplier": "TechCorp Manufacturing",
            "destination": "Electronics Store NYC",
            "weight": "2.1kg",
            "price": "$1299.99"
        }
    }' > /dev/null
    
    curl -s -X POST http://localhost:5004/api/supply-chain/submit \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
        "productId": "PHONE002",
        "organizationId": "Org2MSP",
        "location": "Warehouse B",
        "temperature": 24.0,
        "humidity": 50.5,
        "timestamp": "2025-05-24T11:15:00Z",
        "batchNumber": "PH002",
        "quality": "A",
        "metadata": {
            "supplier": "Mobile Solutions Inc",
            "destination": "Telecom Store LA",
            "weight": "0.18kg",
            "price": "$899.99"
        }
    }' > /dev/null
    
    curl -s -X POST http://localhost:5004/api/supply-chain/submit \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
        "productId": "TABLET003",
        "organizationId": "Org3MSP",
        "location": "Distribution Center C",
        "temperature": 35.0,
        "humidity": 75.2,
        "timestamp": "2025-05-24T12:00:00Z",
        "batchNumber": "TB003",
        "quality": "B",
        "metadata": {
            "supplier": "TabletMax Corp",
            "destination": "Computer Store Chicago",
            "weight": "0.6kg",
            "price": "$549.99"
        }
    }' > /dev/null
    
    print_status "SUCCESS" "Sample data added to the system"
else
    print_status "ERROR" "Failed to authenticate for adding sample data"
fi

echo ""
print_status "SUCCESS" "🎯 System is ready for use!"
echo ""
echo "🌐 Open your browser and navigate to: http://localhost:3000"
echo "🔑 Login with: admin / admin123"
echo ""
echo "🛑 To stop all services, run:"
echo "   kill \$(cat /tmp/cryptanet_*_pid) 2>/dev/null || true"
echo "   rm /tmp/cryptanet_*_pid 2>/dev/null || true"
echo ""

# Keep script running and monitor services
print_status "INFO" "Starting service monitoring (Press Ctrl+C to stop monitoring)..."
echo ""

while true; do
    sleep 30
    echo "📊 $(date): Service health check..."
    
    # Check each service
    services=("Privacy Layer:5003" "Anomaly Detection:5002" "Backend:5004" "Frontend:3000")
    all_healthy=true
    
    for service in "${services[@]}"; do
        name=$(echo $service | cut -d: -f1)
        port=$(echo $service | cut -d: -f2)
        
        if curl -s "http://localhost:$port" > /dev/null 2>&1; then
            echo "   ✅ $name: Healthy"
        else
            echo "   ❌ $name: Down"
            all_healthy=false
        fi
    done
    
    if [ "$all_healthy" = true ]; then
        echo "   🎯 All services operational"
    else
        echo "   ⚠️ Some services need attention"
    fi
    echo ""
done
