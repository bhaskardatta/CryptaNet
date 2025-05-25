#!/bin/bash

# Exit on first error
set -e

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"

# Set FABRIC_CFG_PATH to the current directory where configtx.yaml is located
export FABRIC_CFG_PATH="$(pwd)"
echo "Setting FABRIC_CFG_PATH to: $FABRIC_CFG_PATH"

# Check if binaries exist
if [ ! -f "${BIN_DIR}/cryptogen" ] || [ ! -f "${BIN_DIR}/configtxgen" ]; then
    echo "Fabric binaries not found in ${BIN_DIR}. Installing them now..."
    # Run install-fabric script if it exists
    if [ -f "${PROJECT_ROOT}/install-fabric.sh" ]; then
        (cd "${PROJECT_ROOT}" && ./install-fabric.sh)
    else
        echo "Error: install-fabric.sh script not found. Please install fabric binaries manually."
        exit 1
    fi
fi

# Verify binaries are now executable
if ! command -v cryptogen &> /dev/null; then
    echo "cryptogen command still not found in PATH: $PATH"
    echo "Using full path instead: ${BIN_DIR}/cryptogen"
    CRYPTOGEN="${BIN_DIR}/cryptogen"
    CONFIGTXGEN="${BIN_DIR}/configtxgen"
else
    CRYPTOGEN="cryptogen"
    CONFIGTXGEN="configtxgen"
fi

echo "Using binaries from: $(which ${CRYPTOGEN} 2>/dev/null || echo ${BIN_DIR}/cryptogen)"

# Remove previous crypto material and artifacts
rm -rf ./crypto-config
rm -rf ./channel-artifacts

# Generate crypto material
echo "Generating crypto material using ${CRYPTOGEN}..."
${CRYPTOGEN} generate --config=./crypto-config.yaml --output="./crypto-config"

# Create channel artifacts directory
mkdir -p ./channel-artifacts

# In Fabric 2.x with channel participation API enabled, we don't need a system channel genesis block
# Instead, we'll create an empty genesis.block file to maintain compatibility with scripts
# that might still reference it
touch ./channel-artifacts/genesis.block
echo "# Placeholder for Fabric 2.x - System channel no longer used" > ./channel-artifacts/genesis.block

# Generate channel configuration transaction
echo "Generating channel configuration transaction..."
${CONFIGTXGEN} -profile ThreeOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID supplychainchannel

# Generate anchor peer transactions for each org
echo "Generating anchor peer updates for Org1..."
${CONFIGTXGEN} -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID supplychainchannel -asOrg Org1MSP
echo "Generating anchor peer updates for Org2..."
${CONFIGTXGEN} -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID supplychainchannel -asOrg Org2MSP
echo "Generating anchor peer updates for Org3..."
${CONFIGTXGEN} -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org3MSPanchors.tx -channelID supplychainchannel -asOrg Org3MSP

echo "Generated crypto material and channel artifacts for Fabric 2.x"
echo "Note: System channel is not used in Fabric 2.x with channel participation API"
echo "Channel genesis block will be created dynamically by orderer when channel is created"