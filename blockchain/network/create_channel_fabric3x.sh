#!/bin/bash

# Create channel for Fabric 3.x using the correct approach
# This script creates a configuration block and submits it via participation API

CHANNEL_NAME="supplychainchannel"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"
export FABRIC_CFG_PATH="${PROJECT_ROOT}/network"

echo "Creating channel ${CHANNEL_NAME} for Fabric 3.x..."

# Step 1: Create configuration block from the channel transaction
echo "Step 1: Creating configuration block from channel transaction..."
configtxgen -profile ThreeOrgsChannel \
    -outputCreateChannelTx ./channel-artifacts/${CHANNEL_NAME}_config.pb \
    -channelID ${CHANNEL_NAME}

# Check if the config was created
if [ ! -f "./channel-artifacts/${CHANNEL_NAME}_config.pb" ]; then
    echo "ERROR: Failed to create channel configuration"
    exit 1
fi

# Step 2: Submit to orderer via participation API without content type
echo "Step 2: Submitting channel configuration to orderer..."
curl -X POST http://localhost:9443/participation/v1/channels \
     --data-binary @./channel-artifacts/${CHANNEL_NAME}_config.pb \
     --max-time 30 \
     -v

echo ""
echo "Step 3: Verifying channel creation..."
sleep 3
CHANNELS_RESPONSE=$(curl -s http://localhost:9443/participation/v1/channels)
echo "Orderer channels: ${CHANNELS_RESPONSE}"

# Check if channel was created
if echo "${CHANNELS_RESPONSE}" | grep -q "${CHANNEL_NAME}"; then
    echo "✓ Channel ${CHANNEL_NAME} created successfully!"
    
    # Step 4: Fetch the channel genesis block
    echo "Step 4: Fetching channel genesis block..."
    docker exec -it cli bash -c "
    peer channel fetch 0 /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/${CHANNEL_NAME}.block \\
         -o orderer.example.com:7050 \\
         -c ${CHANNEL_NAME} \\
         --tls \\
         --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
    "
else
    echo "✗ Channel creation failed"
    echo "Response: ${CHANNELS_RESPONSE}"
fi

echo "Channel creation process completed."
