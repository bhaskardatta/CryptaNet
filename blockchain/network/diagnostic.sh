#!/bin/bash
# Comprehensive diagnostics script for CryptaNet Hyperledger Fabric network

# Set color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"

# Source the environment setup if it exists
if [ -f "${PROJECT_ROOT}/fabric-env.sh" ]; then
  source "${PROJECT_ROOT}/fabric-env.sh"
fi

# Helper function to print section headers
print_header() {
    echo -e "\n${BLUE}======================================================${NC}"
    echo -e "${BLUE}== $1${NC}"
    echo -e "${BLUE}======================================================${NC}"
}

# Check if Docker is running
print_header "CHECKING DOCKER STATUS"
if docker info >/dev/null 2>&1; then
    echo -e "${GREEN}Docker is running.${NC}"
else
    echo -e "${RED}Docker is not running. Please start Docker.${NC}"
    exit 1
fi

# List all Docker networks
print_header "DOCKER NETWORKS"
docker network ls
echo -e "\nDetails of cryptanet network:"
docker network inspect cryptanet 2>/dev/null || echo -e "${YELLOW}cryptanet network not found${NC}"

# List all Docker containers related to Hyperledger Fabric
print_header "FABRIC CONTAINERS STATUS"
docker ps --filter "network=cryptanet" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check if all expected containers are running
print_header "CONTAINER EXISTENCE CHECK"
REQUIRED_CONTAINERS=("orderer.example.com" "peer0.org1.example.com" "peer0.org2.example.com" "peer0.org3.example.com" "cli")
MISSING=0

for CONTAINER in "${REQUIRED_CONTAINERS[@]}"; do
    if docker ps --format "{{.Names}}" | grep -q "$CONTAINER"; then
        echo -e "${GREEN}✓ $CONTAINER is running${NC}"
    else
        echo -e "${RED}✗ $CONTAINER is NOT running${NC}"
        MISSING=$((MISSING+1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo -e "${RED}There are $MISSING missing containers. Check docker-compose.yaml and restart the network.${NC}"
fi

# Check container logs for errors
print_header "CHECKING CONTAINER LOGS FOR ERRORS"
for CONTAINER in "${REQUIRED_CONTAINERS[@]}"; do
    if docker ps --format "{{.Names}}" | grep -q "$CONTAINER"; then
        ERROR_COUNT=$(docker logs "$CONTAINER" 2>&1 | grep -i -c -E "error|panic|fail|refused|cannot|unable|critical")
        if [ $ERROR_COUNT -gt 0 ]; then
            echo -e "${YELLOW}Found $ERROR_COUNT errors/warnings in $CONTAINER logs${NC}"
            echo "Last 5 errors:"
            docker logs "$CONTAINER" 2>&1 | grep -i -E "error|panic|fail|refused|cannot|unable|critical" | tail -5
        else
            echo -e "${GREEN}No critical errors found in $CONTAINER logs${NC}"
        fi
    fi
done

# Check network connectivity between containers
print_header "NETWORK CONNECTIVITY TESTS"
echo "Testing connections from CLI container..."

for TARGET in "orderer.example.com:7050" "peer0.org1.example.com:7051" "peer0.org2.example.com:8051" "peer0.org3.example.com:9051"; do
    echo -e "Testing connection to ${YELLOW}$TARGET${NC}..."
    RESULT=$(docker exec cli bash -c "nc -vz -w 3 $TARGET 2>&1" || echo "FAILED")
    if echo "$RESULT" | grep -q "open\|succeeded"; then
        echo -e "${GREEN}✓ Connection to $TARGET successful${NC}"
    else
        echo -e "${RED}✗ Connection to $TARGET failed: $RESULT${NC}"
    fi
done

# DNS resolution check
print_header "DNS RESOLUTION CHECK"
for HOST in "orderer.example.com" "peer0.org1.example.com" "peer0.org2.example.com" "peer0.org3.example.com"; do
    echo -e "Resolving ${YELLOW}$HOST${NC} from CLI container..."
    IP=$(docker exec cli getent hosts "$HOST" | awk '{ print $1 }' || echo "FAILED")
    if [ "$IP" != "FAILED" ]; then
        echo -e "${GREEN}✓ $HOST resolves to $IP${NC}"
    else
        echo -e "${RED}✗ Failed to resolve $HOST${NC}"
        # Try to investigate why resolution is failing
        echo "Checking /etc/hosts in CLI:"
        docker exec cli cat /etc/hosts | grep -i "$HOST" || echo "No entry in /etc/hosts"
    fi
done

# Check channel status
print_header "CHANNEL STATUS CHECK"
echo "Checking channel list on peer0.org1..."
docker exec cli peer channel list || echo -e "${RED}Failed to list channels${NC}"

echo -e "\nChecking if channel block exists..."
if docker exec cli test -f supplychainchannel.block; then
    echo -e "${GREEN}✓ Channel block file exists${NC}"
else
    echo -e "${RED}✗ Channel block file is missing${NC}"
fi

# Check channel participation API on orderer
print_header "ORDERER CHANNEL PARTICIPATION API"
echo "Querying orderer admin API for channels..."
docker exec cli bash -c "curl -s http://orderer.example.com:9443/participation/v1/channels" || echo -e "${RED}Failed to query orderer admin API${NC}"

# Check disk space
print_header "DISK SPACE"
echo "Checking available disk space..."
docker exec cli bash -c "df -h"

# Check MSP configuration
print_header "MSP CONFIGURATION"
echo "Checking MSP folder structure..."
docker exec cli bash -c "ls -la /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"

# Display potential fixes
print_header "POSSIBLE FIXES FOR COMMON ISSUES"
echo -e "1. ${YELLOW}Connection refused${NC}: Check if all services are running with 'docker ps' and check if ports are correctly mapped"
echo -e "2. ${YELLOW}Channel creation fails${NC}: Try running the manual channel creation script:"
echo -e "   ${BLUE}./create_channel_manual.sh${NC}"
echo -e "3. ${YELLOW}DNS resolution issues${NC}: Check container DNS settings and /etc/hosts files"
echo -e "4. ${YELLOW}Orderer can't find channel${NC}: For Fabric 2.x, ensure the channel participation API is enabled and working"
echo -e "5. ${YELLOW}Peer can't join channel${NC}: Ensure the channel block file exists and is accessible"
echo -e "6. ${YELLOW}Reset the entire network${NC}: Run:"
echo -e "   ${BLUE}cd /Users/bhaskar/Desktop/CryptaNet/blockchain/docker && docker-compose down -v && cd ../network && ./generate.sh && cd ../docker && ./prepare_environment.sh clean && docker-compose up -d${NC}"

# Final status
print_header "DIAGNOSTIC SUMMARY"
if [ $MISSING -eq 0 ] && docker exec cli peer channel list 2>/dev/null | grep -q "supplychainchannel"; then
    echo -e "${GREEN}Your Fabric network appears to be functioning correctly with the channel created.${NC}"
elif [ $MISSING -eq 0 ]; then
    echo -e "${YELLOW}All containers are running, but there may be issues with the channel configuration.${NC}"
    echo -e "Try running the ${BLUE}./create_channel_manual.sh${NC} script to create the channel."
else
    echo -e "${RED}There are issues with your Fabric network. Some containers are missing or not running.${NC}"
    echo -e "Please check the docker-compose.yaml file and restart the network."
fi

echo -e "\n${BLUE}Diagnostics completed.${NC}"
