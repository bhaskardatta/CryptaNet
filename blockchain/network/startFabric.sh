#!/bin/bash

# Exit on first error
set -e

# Start from the network directory
cd "$(dirname "$0")"

# Check if crypto-config directory exists, if not generate crypto material
if [ ! -d "crypto-config" ]; then
  echo "Generating crypto material and channel artifacts..."
  ./generate.sh
fi

# Copy crypto-config and channel-artifacts to docker directory
echo "Copying crypto material and channel artifacts to docker directory..."

# Remove existing directories in docker directory if they exist
rm -rf ../docker/crypto-config
rm -rf ../docker/channel-artifacts

# Create the channel-artifacts directory in docker
mkdir -p ../docker/channel-artifacts

# Copy the crypto-config directory
cp -r ./crypto-config ../docker/

# Copy individual channel artifact files instead of the whole directory
cp ./channel-artifacts/genesis.block ../docker/channel-artifacts/
cp ./channel-artifacts/channel.tx ../docker/channel-artifacts/
cp ./channel-artifacts/Org1MSPanchors.tx ../docker/channel-artifacts/
cp ./channel-artifacts/Org2MSPanchors.tx ../docker/channel-artifacts/
cp ./channel-artifacts/Org3MSPanchors.tx ../docker/channel-artifacts/

# Verify the files were copied correctly
echo "Verifying channel artifacts..."
ls -la ../docker/channel-artifacts/

# Start the network
cd ../docker
docker-compose down -v 2>/dev/null || true
docker-compose up -d

# Wait for the network to start
sleep 20

# Check if orderer is reachable
echo "Checking if orderer is reachable..."
docker exec cli ping -c 2 orderer.example.com || echo "Warning: orderer.example.com not reachable yet, but continuing..."

# Create channel
echo "Creating channel..."
docker exec cli peer channel create -o orderer.example.com:7050 -c supplychainchannel -f /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/channel.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Join peer0.org1 to the channel
docker exec cli peer channel join -b supplychainchannel.block

# Update anchor peers for Org1
docker exec cli peer channel update -o orderer.example.com:7050 -c supplychainchannel -f /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/Org1MSPanchors.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Join peer0.org2 to the channel
docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp -e CORE_PEER_ADDRESS=peer0.org2.example.com:8051 -e CORE_PEER_LOCALMSPID="Org2MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt cli peer channel join -b supplychainchannel.block

# Update anchor peers for Org2
docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp -e CORE_PEER_ADDRESS=peer0.org2.example.com:8051 -e CORE_PEER_LOCALMSPID="Org2MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt cli peer channel update -o orderer.example.com:7050 -c supplychainchannel -f /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/Org2MSPanchors.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Join peer0.org3 to the channel
docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp -e CORE_PEER_ADDRESS=peer0.org3.example.com:9051 -e CORE_PEER_LOCALMSPID="Org3MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt cli peer channel join -b supplychainchannel.block

# Update anchor peers for Org3
docker exec -e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp -e CORE_PEER_ADDRESS=peer0.org3.example.com:9051 -e CORE_PEER_LOCALMSPID="Org3MSP" -e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt cli peer channel update -o orderer.example.com:7050 -c supplychainchannel -f /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/Org3MSPanchors.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

echo "Hyperledger Fabric network started successfully"
echo "Channel 'supplychainchannel' created and all peers joined"