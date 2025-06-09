#!/usr/bin/env bash

# CryptaNet Unified Service Startup Script
# Starts all core services on their designated ports:
# - Anomaly Detection: Port 5002
# - Privacy Layer: Port 5003  
# - Backend API: Port 5004
# - Blockchain: Port 5005
# - Enhanced Data Simulator: Port 8001
# - Frontend: Port 3000

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="/Users/bhaskar/Desktop/CryptaNet"
LOG_DIR="$PROJECT_ROOT/logs"
PID_DIR="$PROJECT_ROOT/pids"

# Create necessary directories
mkdir -p "$LOG_DIR" "$PID_DIR"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[$(date '+%H:%M:%S')] ERROR:${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] WARNING:${NC} $1"
}

print_info() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] INFO:${NC} $1"
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_info "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            print_status "$service_name is ready! ✅"
            return 0
        fi
        
        printf "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start within $((max_attempts * 2)) seconds"
    return 1
}

# Function to start a Python service
start_python_service() {
    local service_name=$1
    local script_path=$2
    local port=$3
    local working_dir=$4
    
    print_info "Starting $service_name on port $port..."
    
    # Check if port is available
    if ! check_port $port; then
        print_warning "Port $port is already in use. Attempting to kill existing process..."
        pkill -f ":$port" || true
        sleep 2
        
        if ! check_port $port; then
            print_error "Failed to free port $port for $service_name"
            return 1
        fi
    fi
    
    # Change to working directory and start service
    cd "$working_dir"
    local service_name_lower=$(echo "$service_name" | tr '[:upper:]' '[:lower:]' | tr -d ' ' | tr -d '-')
    nohup python3 "$script_path" > "$LOG_DIR/${service_name_lower}_$(date +%Y%m%d_%H%M%S).log" 2>&1 &
    echo $! > "$PID_DIR/${service_name_lower}.pid"
    
    print_status "$service_name started with PID $(cat "$PID_DIR/${service_name_lower}.pid")"
    cd "$PROJECT_ROOT"
}

# Function to start frontend
start_frontend() {
    print_info "Starting Frontend on port 3000..."
    
    # Check if port is available
    if ! check_port 3000; then
        print_warning "Port 3000 is already in use. Attempting to kill existing process..."
        pkill -f ":3000" || true
        sleep 2
    fi
    
    cd "$PROJECT_ROOT/frontend"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_info "Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend in background
    nohup npm start > "$LOG_DIR/frontend_$(date +%Y%m%d_%H%M%S).log" 2>&1 &
    echo $! > "$PID_DIR/frontend.pid"
    
    print_status "Frontend started with PID $(cat "$PID_DIR/frontend.pid")"
    cd "$PROJECT_ROOT"
}

# Function to stop all services
stop_all_services() {
    print_info "Stopping all CryptaNet services..."
    
    # Kill processes by PID files
    for pid_file in "$PID_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            local service=$(basename "$pid_file" .pid)
            
            if kill -0 $pid 2>/dev/null; then
                print_info "Stopping $service (PID: $pid)..."
                kill $pid 2>/dev/null || true
                sleep 1
                
                # Force kill if still running
                if kill -0 $pid 2>/dev/null; then
                    print_warning "Force killing $service..."
                    kill -9 $pid 2>/dev/null || true
                fi
            fi
            rm -f "$pid_file"
        fi
    done
    
    # Kill any remaining processes on specific ports
    for port in 3000 5002 5003 5004 5005 8001; do
        local pids=$(lsof -ti:$port 2>/dev/null || true)
        if [ -n "$pids" ]; then
            print_info "Killing remaining processes on port $port..."
            echo $pids | xargs kill -9 2>/dev/null || true
        fi
    done
    
    print_status "All services stopped"
}

# Function to show service status
show_status() {
    echo
    print_info "=== CryptaNet Service Status ==="
    echo
    
    local services=(
        "Anomaly Detection:5002:/health"
        "Privacy Layer:5003:/health"
        "Backend API:5004:/health"
        "Blockchain:5005:/health"
        "Data Simulator:8001:/status"
        "Frontend:3000:"
    )
    
    for service_info in "${services[@]}"; do
        local service_name=$(echo "$service_info" | cut -d':' -f1)
        local port=$(echo "$service_info" | cut -d':' -f2)
        local endpoint=$(echo "$service_info" | cut -d':' -f3)
        
        local url="http://localhost:$port$endpoint"
        local status="🔴 DOWN"
        
        if check_port $port; then
            status="🔴 PORT FREE"
        else
            if [ -n "$endpoint" ]; then
                if curl -s "$url" > /dev/null 2>&1; then
                    status="🟢 RUNNING"
                else
                    status="🟡 PORT USED"
                fi
            else
                status="🟡 PORT USED"
            fi
        fi
        
        printf "  %-20s %-10s %s\n" "$service_name" "Port $port" "$status"
    done
    echo
}

# Main execution
case "${1:-start}" in
    "start")
        echo
        print_status "🚀 Starting CryptaNet Services..."
        echo
        
        # Start services in order
        start_python_service "Anomaly-Detection" "$PROJECT_ROOT/anomaly_detection/simple_api_server.py" 5002 "$PROJECT_ROOT/anomaly_detection"
        sleep 3
        
        start_python_service "Privacy-Layer" "$PROJECT_ROOT/privacy_layer/privacy_server.py" 5003 "$PROJECT_ROOT/privacy_layer"
        sleep 3
        
        start_python_service "Backend-API" "$PROJECT_ROOT/backend/simple_backend.py" 5004 "$PROJECT_ROOT/backend"
        sleep 3
        
        start_python_service "Blockchain" "$PROJECT_ROOT/blockchain/simple_blockchain_server.py" 5005 "$PROJECT_ROOT/blockchain"
        sleep 3
        
        start_python_service "Data-Simulator" "$PROJECT_ROOT/enhanced_data_simulator.py" 8001 "$PROJECT_ROOT"
        sleep 3
        
        start_frontend
        sleep 5
        
        echo
        print_status "=== Service Health Check ==="
        
        # Health checks
        wait_for_service "http://localhost:5002/health" "Anomaly Detection"
        wait_for_service "http://localhost:5003/health" "Privacy Layer"  
        wait_for_service "http://localhost:5004/health" "Backend API"
        wait_for_service "http://localhost:5005/health" "Blockchain"
        wait_for_service "http://localhost:8001/status" "Data Simulator"
        wait_for_service "http://localhost:3000" "Frontend"
        
        echo
        print_status "🎉 All CryptaNet services are running!"
        echo
        print_info "=== Access URLs ==="
        echo "  🌐 Frontend:           http://localhost:3000"
        echo "  🤖 Anomaly Detection:  http://localhost:5002"
        echo "  🔐 Privacy Layer:      http://localhost:5003"
        echo "  🔗 Backend API:        http://localhost:5004"
        echo "  ⛓️  Blockchain:         http://localhost:5005"
        echo "  📊 Data Simulator:     http://localhost:8001"
        echo
        print_info "Logs are stored in: $LOG_DIR"
        print_info "PID files are stored in: $PID_DIR"
        echo
        ;;
        
    "stop")
        stop_all_services
        ;;
        
    "restart")
        stop_all_services
        sleep 3
        exec "$0" start
        ;;
        
    "status")
        show_status
        ;;
        
    "logs")
        if [ -n "$2" ]; then
            # Show logs for specific service
            local service_logs=$(ls "$LOG_DIR/$2"*.log 2>/dev/null | head -1)
            if [ -n "$service_logs" ] && [ -f "$service_logs" ]; then
                print_info "Showing logs for $2..."
                tail -f "$LOG_DIR/$2"*.log
            else
                print_error "No logs found for service: $2"
                print_info "Available services: anomaly-detection, privacy-layer, backend-api, blockchain, data-simulator, frontend"
            fi
        else
            # Show all recent logs
            print_info "Showing recent logs from all services..."
            tail -f "$LOG_DIR"/*.log 2>/dev/null || echo "No logs found"
        fi
        ;;
        
    "help"|"-h"|"--help")
        echo
        print_info "CryptaNet Unified Service Manager"
        echo
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  start     Start all services (default)"
        echo "  stop      Stop all services"
        echo "  restart   Restart all services"
        echo "  status    Show service status"
        echo "  logs      Show logs from all services"
        echo "  logs [service]  Show logs from specific service"
        echo "  help      Show this help message"
        echo
        echo "Services managed:"
        echo "  - Anomaly Detection (Port 5002)"
        echo "  - Privacy Layer (Port 5003)"
        echo "  - Backend API (Port 5004)" 
        echo "  - Blockchain (Port 5005)"
        echo "  - Enhanced Data Simulator (Port 8001)"
        echo "  - Frontend (Port 3000)"
        echo
        ;;
        
    *)
        print_error "Unknown command: $1"
        print_info "Use '$0 help' for usage information"
        exit 1
        ;;
esac
