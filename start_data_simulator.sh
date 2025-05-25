#!/bin/bash

# CryptaNet Data Simulator Startup Script
# =====================================

echo "🚀 CryptaNet Advanced Data Simulator"
echo "====================================="

# Check if CryptaNet services are running
echo "🔍 Checking CryptaNet services..."

# Check backend service
if curl -s http://localhost:5004/health > /dev/null 2>&1; then
    echo "✅ Backend service is running on port 5004"
else
    echo "❌ Backend service is not running!"
    echo "Please start CryptaNet services first:"
    echo "  ./start_services.sh"
    echo ""
    read -p "Do you want to start the simulator anyway? (y/n): " choice
    if [[ $choice != "y" && $choice != "Y" ]]; then
        exit 1
    fi
fi

# Check Python dependencies
echo "🔍 Checking Python dependencies..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Install dependencies if needed
if [ ! -f "simulator_requirements.txt" ]; then
    echo "⚠️ Requirements file not found, creating minimal requirements..."
    echo "requests>=2.25.0" > simulator_requirements.txt
    echo "numpy>=1.21.0" >> simulator_requirements.txt
fi

echo "📦 Installing simulator dependencies..."
python3 -m pip install -q -r simulator_requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    echo "You can install them manually:"
    echo "  python3 -m pip install requests numpy"
    echo ""
    read -p "Continue anyway? (y/n): " choice
    if [[ $choice != "y" && $choice != "Y" ]]; then
        exit 1
    fi
fi

echo "✅ Dependencies ready"

# Parse command line arguments
INTERVAL=10
CONFIG_FILE="simulator_config.json"
MAX_RECORDS=""
VERBOSE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--interval)
            INTERVAL="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -m|--max-records)
            MAX_RECORDS="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -i, --interval SECONDS     Data generation interval (default: 10)"
            echo "  -c, --config FILE          Configuration file (default: simulator_config.json)"
            echo "  -m, --max-records NUMBER   Maximum records to generate"
            echo "  -v, --verbose              Enable verbose logging"
            echo "  -h, --help                 Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                         # Run with default settings"
            echo "  $0 -i 5                    # Generate data every 5 seconds"
            echo "  $0 -m 100                  # Generate exactly 100 records"
            echo "  $0 -v                      # Enable verbose output"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Create default config if it doesn't exist
if [ ! -f "$CONFIG_FILE" ]; then
    echo "📄 Creating default configuration file..."
    cat > "$CONFIG_FILE" << 'EOF'
{
  "api_url": "http://localhost:5004",
  "organizations": ["Org1MSP", "Org2MSP", "Org3MSP"],
  "anomaly_rate": 0.15,
  "seasonal_effects": true,
  "time_based_variations": true,
  "authentication": {
    "username": "admin",
    "password": "admin123"
  }
}
EOF
    echo "✅ Configuration file created: $CONFIG_FILE"
fi

# Display configuration
echo ""
echo "⚙️ Simulation Configuration:"
echo "   📡 API URL: http://localhost:5004"
echo "   ⏱️ Interval: ${INTERVAL} seconds"
echo "   📋 Config: ${CONFIG_FILE}"
if [ -n "$MAX_RECORDS" ]; then
    echo "   🎯 Max Records: ${MAX_RECORDS}"
fi
if [ -n "$VERBOSE" ]; then
    echo "   🔍 Verbose Mode: Enabled"
fi

echo ""
echo "🎮 Control Commands:"
echo "   Ctrl+C: Stop the simulator"
echo "   Logs saved to: data_simulator.log"
echo ""

# Build command
CMD="python3 data_simulator.py --interval $INTERVAL --config $CONFIG_FILE"

if [ -n "$MAX_RECORDS" ]; then
    CMD="$CMD --max-records $MAX_RECORDS"
fi

if [ -n "$VERBOSE" ]; then
    CMD="$CMD $VERBOSE"
fi

# Wait a moment and then start
echo "🚀 Starting Data Simulator in 3 seconds..."
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
echo ""

# Start the simulator
echo "▶️ Starting simulator..."
exec $CMD
