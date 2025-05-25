#!/bin/bash

# CryptaNet System Health Monitor
# Monitors all services and provides comprehensive health reporting

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://localhost:5004"
FRONTEND_URL="http://localhost:3000"
PRIVACY_URL="http://localhost:5003"
ANOMALY_URL="http://localhost:5002"

LOG_FILE="system_health_monitor.log"
ALERT_THRESHOLD=3 # Number of consecutive failures before alert

# Initialize counters
declare -A failure_counts
failure_counts["backend"]=0
failure_counts["frontend"]=0
failure_counts["privacy"]=0
failure_counts["anomaly"]=0
failure_counts["blockchain"]=0

echo "🏥 CryptaNet System Health Monitor Starting..." | tee -a "$LOG_FILE"
echo "📅 $(date)" | tee -a "$LOG_FILE"
echo "=======================================" | tee -a "$LOG_FILE"

# Function to log with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to check HTTP service
check_http_service() {
    local service_name="$1"
    local url="$2"
    local expected_status="${3:-200}"
    
    log_message "🔍 Checking $service_name at $url"
    
    if response=$(curl -s -w "%{http_code}" -o /tmp/health_response "$url" --max-time 10); then
        if [ "$response" = "$expected_status" ]; then
            echo -e "✅ ${GREEN}$service_name: HEALTHY${NC} (HTTP $response)"
            failure_counts["$service_name"]=0
            return 0
        else
            echo -e "⚠️  ${YELLOW}$service_name: DEGRADED${NC} (HTTP $response)"
            ((failure_counts["$service_name"]++))
            return 1
        fi
    else
        echo -e "❌ ${RED}$service_name: UNHEALTHY${NC} (Connection failed)"
        ((failure_counts["$service_name"]++))
        return 1
    fi
}

# Function to check process
check_process() {
    local process_name="$1"
    local search_term="$2"
    
    if pgrep -f "$search_term" > /dev/null; then
        echo -e "✅ ${GREEN}$process_name: RUNNING${NC}"
        return 0
    else
        echo -e "❌ ${RED}$process_name: NOT RUNNING${NC}"
        return 1
    fi
}

# Function to check Docker containers
check_docker_containers() {
    log_message "🐳 Checking Docker containers"
    
    if ! command -v docker &> /dev/null; then
        echo -e "⚠️  ${YELLOW}Docker: NOT INSTALLED${NC}"
        return 1
    fi
    
    local running_containers=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep -c "Up" || echo "0")
    local total_containers=$(docker ps -a --format "table {{.Names}}" | wc -l)
    ((total_containers--)) # Remove header line
    
    if [ "$running_containers" -gt 0 ]; then
        echo -e "✅ ${GREEN}Docker: $running_containers/$total_containers containers running${NC}"
        failure_counts["blockchain"]=0
        return 0
    else
        echo -e "❌ ${RED}Docker: No containers running${NC}"
        ((failure_counts["blockchain"]++))
        return 1
    fi
}

# Function to check system resources
check_system_resources() {
    log_message "💻 Checking system resources"
    
    # CPU usage
    cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')
    echo "🖥️  CPU Usage: ${cpu_usage}%"
    
    # Memory usage
    memory_info=$(vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-16s % 16.2f Mi\n", "$1:", $2 * $size / 1048576);')
    echo "💾 Memory Info:"
    echo "$memory_info" | head -3
    
    # Disk usage
    disk_usage=$(df -h / | awk 'NR==2 {print $5}')
    echo "💽 Disk Usage: $disk_usage"
    
    # Network connectivity
    if ping -c 1 8.8.8.8 &> /dev/null; then
        echo -e "🌐 Network: ${GREEN}CONNECTED${NC}"
    else
        echo -e "🌐 Network: ${RED}DISCONNECTED${NC}"
    fi
}

# Function to test API endpoints
test_api_endpoints() {
    log_message "🔌 Testing API endpoints"
    
    # Test backend health endpoint
    if check_http_service "backend" "$BACKEND_URL/health"; then
        # Test supply chain query
        if curl -s "$BACKEND_URL/api/supply-chain/query" | jq -e '.success' > /dev/null 2>&1; then
            echo "  📊 Supply chain API: Working"
        else
            echo "  📊 Supply chain API: Issues detected"
        fi
    fi
    
    # Test privacy layer
    check_http_service "privacy" "$PRIVACY_URL/health"
    
    # Test anomaly detection
    check_http_service "anomaly" "$ANOMALY_URL/health"
    
    # Test frontend
    check_http_service "frontend" "$FRONTEND_URL" "200"
}

# Function to check data flow
check_data_flow() {
    log_message "🔄 Checking data flow"
    
    # Submit test data
    test_data='{
        "organizationId": "Org1MSP",
        "dataType": "supply_chain",
        "data": {
            "productId": "HEALTH-CHECK-001",
            "product": "Health Check Item",
            "temperature": 22.0,
            "humidity": 45.0
        }
    }'
    
    if response=$(curl -s -X POST "$BACKEND_URL/api/supply-chain/submit" \
        -H "Content-Type: application/json" \
        -d "$test_data"); then
        
        if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
            echo -e "✅ ${GREEN}Data Flow: WORKING${NC}"
            
            # Check if data was processed
            data_id=$(echo "$response" | jq -r '.data_id')
            anomaly_detected=$(echo "$response" | jq -r '.anomaly_detected')
            echo "  📋 Test record ID: $data_id"
            echo "  🔍 Anomaly detection: $anomaly_detected"
        else
            echo -e "❌ ${RED}Data Flow: FAILED${NC}"
            echo "  Error: $(echo "$response" | jq -r '.error // "Unknown error"')"
        fi
    else
        echo -e "❌ ${RED}Data Flow: CONNECTION FAILED${NC}"
    fi
}

# Function to generate alerts
check_alerts() {
    log_message "🚨 Checking for alerts"
    
    local alerts_generated=false
    
    for service in "${!failure_counts[@]}"; do
        if [ "${failure_counts[$service]}" -ge "$ALERT_THRESHOLD" ]; then
            echo -e "🚨 ${RED}ALERT: $service has failed ${failure_counts[$service]} consecutive times${NC}"
            alerts_generated=true
        fi
    done
    
    if [ "$alerts_generated" = false ]; then
        echo -e "✅ ${GREEN}No critical alerts${NC}"
    fi
}

# Function to display summary
display_summary() {
    echo ""
    echo "======================================="
    echo "📊 HEALTH CHECK SUMMARY"
    echo "======================================="
    
    local total_issues=0
    for service in "${!failure_counts[@]}"; do
        if [ "${failure_counts[$service]}" -gt 0 ]; then
            ((total_issues++))
        fi
    done
    
    if [ "$total_issues" -eq 0 ]; then
        echo -e "🎉 ${GREEN}All systems operational!${NC}"
    else
        echo -e "⚠️  ${YELLOW}$total_issues service(s) experiencing issues${NC}"
    fi
    
    echo "📈 System Status:"
    for service in "${!failure_counts[@]}"; do
        if [ "${failure_counts[$service]}" -eq 0 ]; then
            echo -e "  $service: ${GREEN}✅ Healthy${NC}"
        else
            echo -e "  $service: ${RED}❌ Issues (${failure_counts[$service]} failures)${NC}"
        fi
    done
    
    echo ""
    echo "📅 Health check completed at $(date)"
    echo "📝 Full log available in: $LOG_FILE"
}

# Main monitoring loop
main() {
    echo "🏥 Starting comprehensive health check..."
    echo ""
    
    # Check system resources
    check_system_resources
    echo ""
    
    # Check processes
    echo "🔍 Checking processes:"
    check_process "Backend" "simple_backend.py"
    check_process "Privacy Layer" "privacy_server.py"
    check_process "Anomaly Detection" "simple_api_server.py"
    check_process "Frontend" "react-scripts"
    echo ""
    
    # Check Docker containers
    check_docker_containers
    echo ""
    
    # Test API endpoints
    test_api_endpoints
    echo ""
    
    # Check data flow
    check_data_flow
    echo ""
    
    # Check for alerts
    check_alerts
    echo ""
    
    # Display summary
    display_summary
}

# Handle script arguments
case "${1:-check}" in
    "check")
        main
        ;;
    "monitor")
        echo "🔄 Starting continuous monitoring (Ctrl+C to stop)..."
        while true; do
            main
            echo ""
            echo "⏰ Waiting 60 seconds for next check..."
            sleep 60
            clear
        done
        ;;
    "alerts")
        check_alerts
        ;;
    "help")
        echo "CryptaNet System Health Monitor"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  check    - Run single health check (default)"
        echo "  monitor  - Run continuous monitoring"
        echo "  alerts   - Check only for alerts"
        echo "  help     - Show this help message"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
