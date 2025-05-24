#!/bin/bash

# CryptaNet System Stop Script
# This script stops all CryptaNet services

echo "🛑 Stopping CryptaNet System..."
echo "==============================="

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

# Stop services by PID files
if ls /tmp/cryptanet_*_pid > /dev/null 2>&1; then
    print_status "INFO" "Stopping services using PID files..."
    for pid_file in /tmp/cryptanet_*_pid; do
        if [ -f "$pid_file" ]; then
            service_name=$(basename "$pid_file" | sed 's/cryptanet_//; s/_pid//')
            pid=$(cat "$pid_file")
            if kill "$pid" 2>/dev/null; then
                print_status "SUCCESS" "Stopped $service_name (PID: $pid)"
            else
                print_status "WARNING" "$service_name (PID: $pid) was not running"
            fi
            rm "$pid_file"
        fi
    done
else
    print_status "WARNING" "No PID files found, trying port-based cleanup..."
fi

# Kill processes on known ports
print_status "INFO" "Stopping processes on CryptaNet ports..."
for port in 3000 5002 5003 5004; do
    if lsof -ti:$port > /dev/null 2>&1; then
        print_status "INFO" "Stopping process on port $port"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
    fi
done

# Optional: Stop blockchain network
read -p "Do you want to stop the blockchain network as well? (y/N): " stop_blockchain
if [[ $stop_blockchain =~ ^[Yy]$ ]]; then
    print_status "INFO" "Stopping blockchain network..."
    cd /Users/bhaskar/Desktop/CryptaNet/blockchain/docker
    docker-compose down
    print_status "SUCCESS" "Blockchain network stopped"
fi

print_status "SUCCESS" "🎯 CryptaNet system stopped successfully!"
echo ""
echo "To restart the system, run:"
echo "   cd /Users/bhaskar/Desktop/CryptaNet"
echo "   ./complete_startup.sh"
