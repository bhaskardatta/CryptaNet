#!/bin/bash
# Enhanced CryptaNet System Startup with Integrated Analytics
# This script starts all components with the new analytics capabilities

echo "🚀 Starting Enhanced CryptaNet System with Integrated Analytics"
echo "================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $port is already in use (possibly $service)${NC}"
        return 0
    else
        return 1
    fi
}

# Function to start service in background
start_service() {
    local name=$1
    local command=$2
    local port=$3
    local logfile=$4
    
    echo -e "${BLUE}📡 Starting $name...${NC}"
    
    if check_port $port "$name"; then
        echo -e "${GREEN}✅ $name appears to be already running on port $port${NC}"
    else
        echo "   Command: $command"
        echo "   Log: $logfile"
        eval "$command" > "$logfile" 2>&1 &
        local pid=$!
        echo "   PID: $pid"
        
        # Wait a moment and check if service started
        sleep 2
        if ps -p $pid > /dev/null; then
            echo -e "${GREEN}✅ $name started successfully${NC}"
        else
            echo -e "${RED}❌ $name failed to start${NC}"
            echo "   Check log: $logfile"
        fi
    fi
    echo ""
}

# Create logs directory if it doesn't exist
mkdir -p logs

echo -e "${BLUE}🔍 Checking system prerequisites...${NC}"

# Check Python dependencies
python3 -c "import requests, flask, flask_cors, pandas, numpy, sklearn" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python dependencies available${NC}"
else
    echo -e "${RED}❌ Missing Python dependencies${NC}"
    echo "   Please run: pip install requests flask flask-cors pandas numpy scikit-learn"
    exit 1
fi

# Check Node.js for frontend
if command -v npm &> /dev/null; then
    echo -e "${GREEN}✅ Node.js/npm available${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js/npm not found - frontend may not work${NC}"
fi

echo ""

# Start Backend API Server
start_service "Backend API Server" \
    "cd backend && python3 simple_backend.py" \
    "5004" \
    "logs/backend.log"

# Start Enhanced Data Simulator
start_service "Enhanced Data Simulator" \
    "python3 enhanced_data_simulator.py" \
    "8001" \
    "logs/simulator.log"

# Start Integrated Analytics (standalone monitoring)
echo -e "${BLUE}📊 Starting Integrated Analytics System...${NC}"
python3 -c "
import integrated_analytics as ia
import time
import threading

def run_monitoring():
    system = ia.IntegratedAnalyticsSystem()
    print('🔬 Integrated Analytics System initialized')
    system.start_continuous_monitoring(interval_minutes=5)  # Every 5 minutes
    
    try:
        while True:
            time.sleep(30)  # Keep alive
    except KeyboardInterrupt:
        print('\\nStopping analytics system...')
        system.stop_monitoring()

# Run in background thread
analytics_thread = threading.Thread(target=run_monitoring, daemon=True)
analytics_thread.start()
print('📈 Analytics monitoring started (5-minute intervals)')
" &
echo "   Analytics PID: $!"
echo ""

# Start Frontend (if npm is available)
if command -v npm &> /dev/null; then
    start_service "React Frontend" \
        "cd frontend && npm start" \
        "3000" \
        "logs/frontend.log"
fi

echo "================================================================="
echo -e "${GREEN}🎉 Enhanced CryptaNet System Startup Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Service Status:${NC}"
echo "   🔧 Backend API:        http://localhost:5004"
echo "   📊 Data Simulator:     http://localhost:8001"
echo "   🌐 Frontend:           http://localhost:3000"
echo "   📈 Analytics:          Running in background"
echo ""
echo -e "${BLUE}🔗 Available API Endpoints:${NC}"
echo "   📊 Comprehensive Analytics: http://localhost:5004/api/analytics/comprehensive"
echo "   🔍 Anomaly Detection:      http://localhost:5004/api/analytics/anomalies"
echo "   🔮 Predictive Analytics:   http://localhost:5004/api/analytics/predictions"
echo "   🚨 Recent Alerts:          http://localhost:5004/api/analytics/alerts"
echo "   📦 Supply Chain Data:      http://localhost:5004/api/supply-chain/query"
echo ""
echo -e "${BLUE}📊 Analytics Features:${NC}"
echo "   ✅ Real-time anomaly detection with ML algorithms"
echo "   ✅ Predictive analytics with feature engineering"
echo "   ✅ Risk assessment and scoring (0-100 scale)"
echo "   ✅ Automated alerting system with database persistence"
echo "   ✅ Comprehensive dashboard integration"
echo "   ✅ Continuous monitoring every 5 minutes"
echo ""
echo -e "${YELLOW}💡 Quick Commands:${NC}"
echo "   • Test analytics:      python3 test_integrated_system.py"
echo "   • Check logs:          tail -f logs/*.log"
echo "   • Stop all:            ./stop_system.sh"
echo ""
echo -e "${GREEN}✨ System is now ready for advanced supply chain monitoring!${NC}"
