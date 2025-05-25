#!/bin/bash
# CryptaNet System Shutdown Script
# This script stops all running CryptaNet services

echo "🛑 Stopping CryptaNet System"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kill all CryptaNet related processes
echo -e "${BLUE}🔍 Identifying CryptaNet processes...${NC}"

# Stop Python processes
echo -e "${BLUE}🐍 Stopping Python processes...${NC}"
pkill -f "python3 enhanced_data_simulator.py" 2>/dev/null
pkill -f "python3 simple_backend.py" 2>/dev/null
pkill -f "integrated_analytics" 2>/dev/null

# Stop Node.js processes
echo -e "${BLUE}🟢 Stopping Node.js processes...${NC}"
pkill -f "node.*react-scripts start" 2>/dev/null

# Check if any processes were stopped
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ CryptaNet processes successfully stopped${NC}"
else 
    echo -e "${YELLOW}⚠️ No active CryptaNet processes found${NC}"
fi

# Check ports to confirm shutdown
echo -e "${BLUE}🔍 Confirming all ports are released...${NC}"

ports_in_use=0
for port in 3000 5004 8001; do
    if lsof -i :$port >/dev/null 2>&1; then
        echo -e "${RED}❌ Port $port is still in use${NC}"
        ports_in_use=$((ports_in_use + 1))
    else
        echo -e "${GREEN}✅ Port $port is free${NC}"
    fi
done

if [ $ports_in_use -eq 0 ]; then
    echo -e "${GREEN}✅ All CryptaNet services have been successfully stopped${NC}"
else
    echo -e "${YELLOW}⚠️ Some services may still be running${NC}"
    echo "   To force kill them, you can use: lsof -ti:<port> | xargs kill -9"
fi

echo ""
echo -e "${GREEN}👋 CryptaNet shutdown complete${NC}"
