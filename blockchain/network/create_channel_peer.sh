#!/bin/bash

# This script creates a channel using the traditional peer channel create command
# which works better with the current orderer setup

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"
export FABRIC_CFG_PATH="${PROJECT_ROOT}/network"

# Source the environment setup if it exists
if [ -f "${PROJECT_ROOT}/fabric-env.sh" ]; then
  source "${PROJECT_ROOT}/fabric-env.sh"
fi

# Set environment variables for Org1
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PROJECT_ROOT}/network/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PROJECT_ROOT}/network/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

# Set environment variables
CHANNEL_NAME="supplychainchannel"
ORDERER_CA=${PROJECT_ROOT}/network/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

echo "Creating channel using peer channel create command..."

# Check if configtxgen and peer are available
PEER="$(which peer 2>/dev/null || echo ${BIN_DIR}/peer)"
echo "Using peer from: ${PEER}"

# Step 1: Create the channel using peer channel create
${PEER} channel create \
    -o localhost:7050 \
    -c ${CHANNEL_NAME} \
    -f ./channel-artifacts/channel.tx \
    --outputBlock ./channel-artifacts/${CHANNEL_NAME}.block \
    --tls \
    --cafile ${ORDERER_CA}

# Check if the channel block was created
if [ -f "./channel-artifacts/${CHANNEL_NAME}.block" ]; then
    echo "✓ Channel ${CHANNEL_NAME} created successfully!"
    echo "Channel block saved to ./channel-artifacts/${CHANNEL_NAME}.block"
else
    echo "✗ Channel creation failed - block file not found"
    exit 1
fi

echo "Channel creation process complete"
