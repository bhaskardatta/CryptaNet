#!/bin/bash

echo "Setting up CryptaNet Blockchain Channel..."

# Set environment variables
export CORE_PEER_ADDRESS=peer0.org1.example.com:7051
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

# Step 1: Check if channel configuration exists
echo "Checking channel configuration..."
if [ ! -f "/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/channel.tx" ]; then
    echo "Creating channel configuration..."
    configtxgen -profile TwoOrgsChannel -outputCreateChannelTx channel.tx -channelID supplychainchannel
fi

# Step 2: Create channel (ignore error if already exists)
echo "Creating channel supplychainchannel..."
peer channel create -o orderer.example.com:7050 -c supplychainchannel -f channel.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem 2>/dev/null || echo "Channel may already exist, continuing..."

# Step 3: Fetch genesis block
echo "Fetching genesis block..."
peer channel fetch 0 supplychainchannel.block -o orderer.example.com:7050 -c supplychainchannel --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Step 4: Join peer0.org1 to channel
echo "Joining peer0.org1 to channel..."
peer channel join -b supplychainchannel.block

# Step 5: Join peer0.org2 to channel
echo "Joining peer0.org2 to channel..."
export CORE_PEER_ADDRESS=peer0.org2.example.com:8051
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp

peer channel join -b supplychainchannel.block

# Step 6: Join peer0.org3 to channel
echo "Joining peer0.org3 to channel..."
export CORE_PEER_ADDRESS=peer0.org3.example.com:9051
export CORE_PEER_LOCALMSPID=Org3MSP
export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp

peer channel join -b supplychainchannel.block

# Step 7: Install chaincode on all peers
echo "Installing chaincode on peer0.org1..."
export CORE_PEER_ADDRESS=peer0.org1.example.com:7051
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

peer chaincode install -n supplychain -v 1.0 -p github.com/chaincode/supplychain

echo "Installing chaincode on peer0.org2..."
export CORE_PEER_ADDRESS=peer0.org2.example.com:8051
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp

peer chaincode install -n supplychain -v 1.0 -p github.com/chaincode/supplychain

# Step 8: Instantiate chaincode
echo "Instantiating chaincode..."
export CORE_PEER_ADDRESS=peer0.org1.example.com:7051
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

peer chaincode instantiate -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C supplychainchannel -n supplychain -v 1.0 -c '{"Args":["init"]}' -P "AND ('Org1MSP.peer','Org2MSP.peer')"

echo "Channel setup complete!"

# Step 9: Verify setup
echo "Verifying channel setup..."
peer channel list

echo "Testing chaincode..."
peer chaincode query -C supplychainchannel -n supplychain -c '{"function":"GetAllSupplyChainData","Args":[]}'

