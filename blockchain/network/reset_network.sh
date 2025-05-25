#!/bin/bash
# Reset script for CryptaNet blockchain network

# Display warning
echo "⚠️  WARNING: This will reset the entire blockchain network and delete all data!"
echo "All ledger data, channel information, and container state will be lost."
read -p "Are you sure you want to proceed? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Reset canceled."
    exit 1
fi

# Set working directory to the script location
cd "$(dirname "$0")"

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

# Stop all containers and remove volumes
echo "Stopping all containers and removing volumes..."
cd ../docker
docker-compose down -v

# Remove generated artifacts
echo "Removing generated artifacts..."
rm -rf ./channel-artifacts
rm -rf ./crypto-config
rm -rf ./orderer-data

# Regenerate crypto material and artifacts
echo "Regenerating crypto material and channel artifacts..."
cd ../network
./generate.sh

# Prepare docker environment
echo "Preparing docker environment..."
cd ../docker
./prepare_environment.sh clean

# Start containers
echo "Starting containers..."
docker-compose up -d

# Wait for containers to start
echo "Waiting for containers to start..."
sleep 15

# Display network status
echo "Network reset complete. Checking status..."
docker ps --filter "network=cryptanet"

echo "Network has been reset. To create channels and join peers, run:"
echo "cd ../network && ./startFabric.sh"
