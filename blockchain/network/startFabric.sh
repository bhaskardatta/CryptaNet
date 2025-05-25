#!/bin/bash

# Exit on first error
set -e

# Start from the network directory
cd "$(dirname "$0")"

# Determine the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"

# Check if binaries exist
if [ ! -f "${BIN_DIR}/peer" ] || [ ! -f "${BIN_DIR}/configtxgen" ]; then
    echo "Fabric binaries not found in ${BIN_DIR}. Installing them now..."
    # Run install-fabric script if it exists
    if [ -f "${PROJECT_ROOT}/install-fabric.sh" ]; then
        (cd "${PROJECT_ROOT}" && ./install-fabric.sh)
    else
        echo "Error: install-fabric.sh script not found. Please install fabric binaries manually."
        exit 1
    fi
fi

# Verify bin directory is in PATH
echo "Using Fabric binaries from: ${BIN_DIR}"
echo "Current PATH: $PATH"

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
# Copy the channel block if it exists (for Fabric 2.x)
cp ./channel-artifacts/supplychainchannel.block ../docker/channel-artifacts/ 2>/dev/null || echo "Channel block not found, will be created later"

# Verify the files were copied correctly
echo "Verifying channel artifacts..."
ls -la ../docker/channel-artifacts/

# Start the network
cd ../docker
# Run the prepare_environment script
./prepare_environment.sh
docker-compose down -v 2>/dev/null || true
docker-compose up -d

# Check if all containers are properly started
echo "Checking if all containers are running..."
RETRY_COUNT=0
MAX_RETRIES=5
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  RUNNING_COUNT=$(docker ps --filter "network=cryptanet" --format "{{.Names}}" | wc -l)
  EXPECTED_COUNT=8  # Total expected containers
  
  if [ "$RUNNING_COUNT" -eq "$EXPECTED_COUNT" ]; then
    echo "All $EXPECTED_COUNT containers are running."
    break
  else
    echo "Only $RUNNING_COUNT out of $EXPECTED_COUNT containers are running. Waiting 30 seconds..."
    sleep 30
    RETRY_COUNT=$((RETRY_COUNT+1))
  fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "ERROR: Not all containers are running after multiple attempts."
  echo "Current container status:"
  docker ps
  exit 1
fi

# Wait for the containers to fully initialize
echo "Waiting for services to initialize (30 seconds)..."
sleep 30

# Check if containers are running
echo "Checking container status:"
docker ps

# Print Docker network info
echo "Docker network information:"
docker network inspect cryptanet | grep -A 20 "Containers"

# Print hosts file from CLI container to verify DNS resolution
echo "Checking hosts file in CLI container:"
docker exec cli cat /etc/hosts

# Check DNS resolution for all services
echo "Checking DNS resolution for all services:"
docker exec cli bash -c "getent hosts orderer.example.com || echo 'Error: Could not resolve orderer.example.com'"
docker exec cli bash -c "getent hosts peer0.org1.example.com || echo 'Error: Could not resolve peer0.org1.example.com'"
docker exec cli bash -c "getent hosts peer0.org2.example.com || echo 'Error: Could not resolve peer0.org2.example.com'"
docker exec cli bash -c "getent hosts peer0.org3.example.com || echo 'Error: Could not resolve peer0.org3.example.com'"

# Try to ping all services
echo "Attempting to ping services:"
docker exec cli bash -c "ping -c 2 orderer.example.com || echo 'Could not ping orderer'"
docker exec cli bash -c "ping -c 2 peer0.org1.example.com || echo 'Could not ping peer0.org1'"

# Try to connect to all services
echo "Checking if orderer and peers are reachable:"
docker exec cli bash -c "echo 'Testing orderer.example.com:7050' && nc -vz -w 5 orderer.example.com 7050 || echo 'Warning: orderer not reachable with nc'"
docker exec cli bash -c "echo 'Testing peer0.org1.example.com:7051' && nc -vz -w 5 peer0.org1.example.com 7051 || echo 'Warning: peer0.org1 not reachable with nc'"
docker exec cli bash -c "echo 'Testing peer0.org2.example.com:8051' && nc -vz -w 5 peer0.org2.example.com 8051 || echo 'Warning: peer0.org2 not reachable with nc'"
docker exec cli bash -c "echo 'Testing peer0.org3.example.com:9051' && nc -vz -w 5 peer0.org3.example.com 9051 || echo 'Warning: peer0.org3 not reachable with nc'"

# Try with curl for TLS services
echo "Testing TLS connections to orderer and peers:"
docker exec cli bash -c "curl -s -o /dev/null -w '%{http_code}' --insecure https://orderer.example.com:7050 || echo 'Orderer TLS handshake failed, but this might be expected'"

# Try Docker DNS lookup directly
echo "Attempting direct Docker DNS lookup:"
docker exec cli bash -c "nslookup orderer.example.com || echo 'nslookup failed'"

# Add explicit hosts entries as a backup
echo "Adding explicit IP addresses to CLI container hosts file as a backup measure:"
docker exec cli bash -c "docker_host_ip=\$(getent hosts host.docker.internal | awk '{ print \$1 }' || echo '172.17.0.1'); echo \"\$docker_host_ip host.docker.internal\" >> /etc/hosts"
for container in orderer.example.com peer0.org1.example.com peer0.org2.example.com peer0.org3.example.com; do
  container_ip=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $container 2>/dev/null || echo '')
  if [ -n "$container_ip" ]; then
    echo "Adding $container with IP $container_ip to hosts file"
    docker exec cli bash -c "echo \"$container_ip $container\" >> /etc/hosts"
  fi
done

echo "Waiting 10 more seconds before channel creation..."
sleep 10

# Create channel using channel participation API (Fabric 2.x method)
echo "Creating channel using channel participation API..."

# Use the participation API to join the channel - need to send the channel.tx as binary data
echo "Joining orderer to channel using participation API..."
docker exec cli bash -c "curl -X POST http://orderer.example.com:9443/participation/v1/channels -H 'Content-Type: application/octet-stream' --data-binary @/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/channel.tx"

# Wait a moment for the channel to be created
sleep 5

# Check if channel was created successfully by listing channels
echo "Checking if channel was created successfully..."
CHANNEL_LIST=$(docker exec cli bash -c "curl -s http://orderer.example.com:9443/participation/v1/channels" || echo "")
echo "Available channels: $CHANNEL_LIST"

# Now try to fetch genesis block
echo "Fetching genesis block from orderer..."
docker exec cli peer channel fetch 0 supplychainchannel.block -c supplychainchannel -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Check if the channel block was created
if docker exec cli test -f supplychainchannel.block; then
  echo "Channel genesis block obtained successfully!"
else
  echo "Failed to obtain channel genesis block. Checking orderer logs..."
  docker logs orderer.example.com --tail 20
  exit 1
fi

# Sleep to allow channel creation to complete
echo "Waiting for channel creation to complete..."
sleep 10

# Join peer0.org1 to the channel
echo "Joining peer0.org1 to the channel..."
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

# Check channel info
echo "Checking channel information..."
docker exec cli peer channel list
docker exec cli peer channel getinfo -c supplychainchannel

# Display orderer participation API status (should show the channel)
echo "Checking orderer channel participation status..."
docker exec cli bash -c "curl -s http://orderer.example.com:9443/participation/v1/channels | jq"

echo "Hyperledger Fabric network started successfully"
echo "Channel 'supplychainchannel' created and all peers joined"

# Display network health summary
echo ""
echo "========================================"
echo "NETWORK HEALTH SUMMARY"
echo "========================================"
echo "Running containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"
echo ""
echo "Channel Status:"
docker exec cli peer channel list
echo ""
echo "Connection Status:"
docker exec cli bash -c "curl -s http://orderer.example.com:9443/participation/v1/channels" | grep -o "supplychainchannel" || echo "WARNING: Channel not found in orderer"
echo "========================================"