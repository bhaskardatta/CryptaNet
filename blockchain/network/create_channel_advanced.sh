#!/bin/bash

# Advanced channel creation using configtxlator and participation API
# This script converts channel.tx to the proper format for Fabric 2.x

CHANNEL_NAME="supplychainchannel"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"

echo "Creating channel ${CHANNEL_NAME} using configtxlator approach..."

# Create temporary directory
mkdir -p .tmp

# Step 1: Convert channel.tx (envelope) to JSON
echo "Step 1: Converting channel.tx to JSON..."
configtxlator proto_decode --input ./channel-artifacts/channel.tx --type common.Envelope --output .tmp/envelope.json

# Step 2: Extract the config from the envelope
echo "Step 2: Extracting config from envelope..."
jq .payload.data .tmp/envelope.json | jq . > .tmp/config_update.json

# Step 3: Decode the base64 config data
echo "Step 3: Decoding config data..."
jq -r .payload.data .tmp/envelope.json | base64 -d > .tmp/config_update.pb

# Step 4: Convert config update to JSON
echo "Step 4: Converting config update to JSON..."
configtxlator proto_decode --input .tmp/config_update.pb --type common.ConfigUpdate --output .tmp/config_update_decoded.json

# Step 5: Create the channel config envelope
echo "Step 5: Creating channel config envelope..."
echo '{"payload":{"header":{"channel_header":{"channel_id":"'${CHANNEL_NAME}'","type":2}},"data":{"config_update":'$(cat .tmp/config_update_decoded.json)'}}}' | jq . > .tmp/config_envelope.json

# Step 6: Convert back to protobuf
echo "Step 6: Converting back to protobuf..."
configtxlator proto_encode --input .tmp/config_envelope.json --type common.Envelope --output .tmp/config_envelope.pb

# Step 7: Submit using participation API
echo "Step 7: Submitting to orderer via participation API..."
curl -X POST http://localhost:9443/participation/v1/channels \
     --data-binary @.tmp/config_envelope.pb \
     -v

echo ""
echo "Step 8: Verifying channel creation..."
sleep 2
curl -s http://localhost:9443/participation/v1/channels | jq

# Cleanup
rm -rf .tmp

echo "Channel creation process completed."
