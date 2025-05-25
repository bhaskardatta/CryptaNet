#!/bin/bash
# configcheck.sh - Check Hyperledger Fabric configuration files

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NETWORK_DIR="${PROJECT_ROOT}/network"
CONFIG_DIR="${PROJECT_ROOT}/config"
BIN_DIR="${PROJECT_ROOT}/bin"

# Add the bin directory to PATH
export PATH="${BIN_DIR}:$PATH"

# Text formatting
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check for configtx.yaml in network directory
echo -e "${BOLD}Checking for configtx.yaml in network directory:${NC}"
if [ -f "${NETWORK_DIR}/configtx.yaml" ]; then
    echo -e "${GREEN}✓ Found configtx.yaml in network directory${NC}"
    export FABRIC_CFG_PATH="${NETWORK_DIR}"
    
    # Check profiles in the configtx.yaml file
    echo -e "\n${BOLD}Checking profiles in ${NETWORK_DIR}/configtx.yaml:${NC}"
    PROFILES=$(grep -o "^\s*[A-Za-z0-9]*:" "${NETWORK_DIR}/configtx.yaml" | grep -v "^#" | sed 's/://g' | sed 's/^[[:space:]]*//')
    echo "Found profiles:"
    
    # Check specific profiles
    if echo "$PROFILES" | grep -q "ThreeOrgsOrdererGenesis"; then
        echo -e "${GREEN}✓ Found ThreeOrgsOrdererGenesis profile${NC}"
    else
        echo -e "${RED}✗ Missing ThreeOrgsOrdererGenesis profile${NC}"
    fi
    
    if echo "$PROFILES" | grep -q "ThreeOrgsChannel"; then
        echo -e "${GREEN}✓ Found ThreeOrgsChannel profile${NC}"
    else
        echo -e "${RED}✗ Missing ThreeOrgsChannel profile${NC}"
    fi
    
    # Test with configtxgen
    echo -e "\n${BOLD}Testing configtxgen with FABRIC_CFG_PATH=${FABRIC_CFG_PATH}:${NC}"
    CONFIG_TEST=$(${BIN_DIR}/configtxgen -version 2>&1)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ configtxgen works correctly${NC}"
    else
        echo -e "${RED}✗ configtxgen error: $CONFIG_TEST${NC}"
    fi
    
    # List channel profiles
    echo -e "\n${BOLD}Testing profile access:${NC}"
    CHANNEL_TEST=$(${BIN_DIR}/configtxgen -inspectChannelCreateTx "${NETWORK_DIR}/channel-artifacts/channel.tx" 2>&1 || echo "Failed to inspect channel tx")
    echo "$CHANNEL_TEST" | head -n 5
else
    echo -e "${RED}✗ Missing configtx.yaml in network directory${NC}"
fi

# Check for configtx.yaml in config directory
echo -e "\n${BOLD}Checking for configtx.yaml in config directory:${NC}"
if [ -f "${CONFIG_DIR}/configtx.yaml" ]; then
    echo -e "${GREEN}✓ Found configtx.yaml in config directory${NC}"
    
    # Compare the files if both exist
    if [ -f "${NETWORK_DIR}/configtx.yaml" ]; then
        echo -e "\n${BOLD}Comparing configtx.yaml files:${NC}"
        if diff "${NETWORK_DIR}/configtx.yaml" "${CONFIG_DIR}/configtx.yaml" >/dev/null; then
            echo -e "${GREEN}✓ configtx.yaml files are identical${NC}"
        else
            echo -e "${RED}✗ configtx.yaml files are different${NC}"
            echo -e "${YELLOW}This may cause inconsistent behavior depending on FABRIC_CFG_PATH${NC}"
        fi
    fi
else
    echo -e "${YELLOW}! No configtx.yaml in config directory${NC}"
fi

# Summary
echo -e "\n${BOLD}Environment Variables:${NC}"
echo "FABRIC_CFG_PATH=$FABRIC_CFG_PATH"
echo "PATH=$PATH"

echo -e "\n${BOLD}Recommendations:${NC}"
echo -e "1. Always set ${YELLOW}export FABRIC_CFG_PATH=${NETWORK_DIR}${NC} before running configtxgen"
echo -e "2. Make sure profiles in configtx.yaml match what your scripts are looking for"
echo -e "3. Consider creating a symlink: ${YELLOW}ln -sf ${NETWORK_DIR}/configtx.yaml ${CONFIG_DIR}/configtx.yaml${NC}"
