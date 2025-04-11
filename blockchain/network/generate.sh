#!/bin/bash

# Exit on first error
set -e

# Remove previous crypto material and artifacts
rm -rf ./crypto-config
rm -rf ./channel-artifacts

# Generate crypto material
cryptogen generate --config=./crypto-config.yaml --output="./crypto-config"

# Create channel artifacts directory
mkdir -p ./channel-artifacts

# Generate genesis block for orderer
configtxgen -profile ThreeOrgsOrdererGenesis -channelID system-channel -outputBlock ./channel-artifacts/genesis.block

# Generate channel configuration transaction
configtxgen -profile ThreeOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID supplychainchannel

# Generate anchor peer transactions for each org
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID supplychainchannel -asOrg Org1MSP
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID supplychainchannel -asOrg Org2MSP
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org3MSPanchors.tx -channelID supplychainchannel -asOrg Org3MSP

echo "Generated crypto material and channel artifacts"