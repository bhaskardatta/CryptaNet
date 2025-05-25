#!/bin/bash

# Create channel for Fabric 3.x using the correct configuration block format
# This script creates a proper config block and submits it via participation API

CHANNEL_NAME="supplychainchannel"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"
export FABRIC_CFG_PATH="${PROJECT_ROOT}/network"

echo "Creating channel ${CHANNEL_NAME} for Fabric 3.x with proper config block..."

# Step 1: Create the channel configuration from configtx.yaml
echo "Step 1: Generating channel configuration..."
configtxgen -profile ThreeOrgsChannel -outputCreateChannelTx ./channel-artifacts/${CHANNEL_NAME}.tx -channelID ${CHANNEL_NAME}

if [ ! -f "./channel-artifacts/${CHANNEL_NAME}.tx" ]; then
    echo "ERROR: Failed to create channel transaction"
    exit 1
fi

# Step 2: Convert the channel transaction to a configuration block
echo "Step 2: Converting channel transaction to configuration block..."

# Create temporary directory
mkdir -p .tmp

# Extract the configuration from the channel transaction
configtxlator proto_decode --input ./channel-artifacts/${CHANNEL_NAME}.tx --type common.Envelope --output .tmp/envelope.json

# Extract the config update
jq -r .payload.data .tmp/envelope.json | base64 -d > .tmp/config_update.pb

# Decode the config update
configtxlator proto_decode --input .tmp/config_update.pb --type common.ConfigUpdate --output .tmp/config_update.json

# Extract the write set (new configuration)
jq .write_set .tmp/config_update.json > .tmp/config.json

# Create a configuration block structure
echo '{
  "header": {
    "number": "0",
    "previous_hash": "",
    "data_hash": ""
  },
  "metadata": {
    "metadata": ["", "", "", ""]
  },
  "data": {
    "data": []
  }
}' > .tmp/block.json

# Encode the configuration
configtxlator proto_encode --input .tmp/config.json --type common.Config --output .tmp/config.pb

# Create the block data
jq --argjson config "$(base64 < .tmp/config.pb | tr -d '\n')" '.data.data[0] = $config' .tmp/block.json > .tmp/block_with_config.json

# Encode the block
configtxlator proto_encode --input .tmp/block_with_config.json --type common.Block --output .tmp/${CHANNEL_NAME}_config_block.pb

echo "Step 3: Submitting configuration block to orderer..."
curl -X POST http://localhost:9443/participation/v1/channels \
     -F "config-block=@.tmp/${CHANNEL_NAME}_config_block.pb" \
     -v

echo ""
echo "Step 4: Verifying channel creation..."
sleep 3
CHANNELS_RESPONSE=$(curl -s http://localhost:9443/participation/v1/channels)
echo "Orderer channels: ${CHANNELS_RESPONSE}"

# Check if channel was created
if echo "${CHANNELS_RESPONSE}" | grep -q "${CHANNEL_NAME}"; then
    echo "✓ Channel ${CHANNEL_NAME} created successfully!"
    
    # Step 5: Fetch the channel genesis block for peer operations
    echo "Step 5: Fetching channel genesis block..."
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

# Cleanup
rm -rf .tmp

echo "Channel creation process completed."
