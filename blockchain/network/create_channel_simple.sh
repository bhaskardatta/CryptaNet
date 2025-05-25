#!/bin/bash

# Simple approach: Use the channel.tx directly with participation API
# Sometimes Fabric 3.x accepts channel transactions directly

CHANNEL_NAME="supplychainchannel"

echo "Attempting simple channel creation with channel.tx..."

# Try submitting the original channel.tx file
echo "Step 1: Submitting channel.tx directly..."
curl -X POST http://localhost:9443/participation/v1/channels \
     -F "config-block=@./channel-artifacts/channel.tx" \
     -v

echo ""
echo "Step 2: Verifying..."
sleep 2
curl -s http://localhost:9443/participation/v1/channels | jq

echo "Simple approach completed."
