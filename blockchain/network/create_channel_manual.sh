#!/bin/bash

# This script helps manually create a channel using the Fabric 2.x channel participation API
# Usage: ./create_channel.sh

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"
export FABRIC_CFG_PATH="${PROJECT_ROOT}/config"

# Source the environment setup if it exists
if [ -f "${PROJECT_ROOT}/fabric-env.sh" ]; then
  source "${PROJECT_ROOT}/fabric-env.sh"
fi

# Set environment variables
CHANNEL_NAME="supplychainchannel"
ORDERER_ADMIN_URL="http://localhost:9443"

# Check if configtxlator is in PATH
CONFIGTXLATOR="$(which configtxlator 2>/dev/null || echo ${BIN_DIR}/configtxlator)"
echo "Using configtxlator from: ${CONFIGTXLATOR}"

# Step 1: Ensure we have the channel.tx file
if [ ! -f ./channel-artifacts/channel.tx ]; then
    echo "channel.tx file not found. Please run generate.sh first."
    exit 1
fi

# Step 2: Create the channel using the participation API with the channel.tx file
echo "Creating channel ${CHANNEL_NAME} via the participation API..."

# Try multiple approaches for channel creation
echo "Attempting approach 1: Direct binary upload..."
curl -v -X POST "${ORDERER_ADMIN_URL}/participation/v1/channels" \
     -H "Content-Type: application/x-protobuf" \
     --data-binary @./channel-artifacts/channel.tx

echo ""
echo "Attempting approach 2: Base64 encoded JSON..."
CHANNEL_TX_B64=$(base64 < ./channel-artifacts/channel.tx | tr -d '\n')
curl -v -X POST "${ORDERER_ADMIN_URL}/participation/v1/channels" \
     -H "Content-Type: application/json" \
     -d "{\"config-block\":\"${CHANNEL_TX_B64}\"}"

# Step 3: Verify the channel was created
echo "Verifying channel creation..."
sleep 2
CHANNELS_RESPONSE=$(curl -s "${ORDERER_ADMIN_URL}/participation/v1/channels")
echo "Channels on orderer: ${CHANNELS_RESPONSE}"

# Check if our channel was created
if echo "${CHANNELS_RESPONSE}" | grep -q "${CHANNEL_NAME}"; then
    echo "✓ Channel ${CHANNEL_NAME} created successfully!"
else
    echo "✗ Channel ${CHANNEL_NAME} creation may have failed"
    echo "Response: ${CHANNELS_RESPONSE}"
fi

echo "Manual channel creation process complete"
