#!/bin/bash

# Create channel using CLI container and channel participation API
# This script works with Fabric 2.x orderer setup

CHANNEL_NAME="supplychainchannel"

echo "Creating channel ${CHANNEL_NAME} using Fabric 2.x approach..."

# Step 1: Use the CLI container to access the channel.tx file and create the channel via participation API
docker exec -it cli bash -c "
set -e

echo 'Step 1: Checking if channel.tx exists...'
if [ ! -f /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/channel.tx ]; then
    echo 'ERROR: channel.tx file not found'
    exit 1
fi

echo 'Step 2: Converting channel.tx to base64 for participation API...'
CHANNEL_TX_B64=\$(base64 < /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/channel.tx | tr -d '\n')

echo 'Step 3: Creating channel via participation API...'
curl -X POST http://orderer.example.com:9443/participation/v1/channels \\
     -H 'Content-Type: application/json' \\
     -d '{\"config-block\":\"\${CHANNEL_TX_B64}\"}' \\
     -v

echo ''
echo 'Step 4: Waiting for channel creation...'
sleep 3

echo 'Step 5: Verifying channel creation...'
curl -s http://orderer.example.com:9443/participation/v1/channels | jq

echo 'Step 6: Now creating the channel block using peer channel fetch...'
peer channel fetch 0 /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/${CHANNEL_NAME}.block \\
     -o orderer.example.com:7050 \\
     -c ${CHANNEL_NAME} \\
     --tls \\
     --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
"

echo "Channel creation process completed."
