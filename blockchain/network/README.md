# CryptaNet Blockchain Network

## Network Configuration for Hyperledger Fabric 2.x

This directory contains the configuration files and scripts for running a Hyperledger Fabric 2.x blockchain network for the CryptaNet project.

## Important Changes

The network configuration has been updated to be compatible with Hyperledger Fabric 2.x. Key changes include:

1. Removed system channel dependency
2. Enabled the channel participation API for Fabric 2.x
3. Fixed DNS resolution between containers
4. Enhanced network configuration and container naming
5. Added diagnostic tools and scripts

## Directory Structure

- `docker/` - Docker Compose files and container configurations
- `network/` - Network setup and channel creation scripts
- `chaincode/` - Smart contracts for the supply chain application
- `client/` - Python client for interacting with the blockchain

## Getting Started

1. Start the network:
   ```
   cd network
   ./startFabric.sh
   ```

2. Check network status:
   ```
   cd network
   ./diagnostic.sh
   ```

## Troubleshooting

### Channel Creation Issues

If you encounter issues with channel creation, you can try the manual channel creation script:

```
cd network
./create_channel_manual.sh
```

### Container Connectivity Issues

If containers can't communicate, check network configuration:

1. Run the diagnostic script:
   ```
   ./diagnostic.sh
   ```
   
2. Check container DNS resolution:
   ```
   docker exec cli ping peer0.org1.example.com
   ```

3. Check if orderer admin API is accessible:
   ```
   docker exec cli curl -s http://orderer.example.com:9443/participation/v1/channels
   ```

### Complete Network Reset

If you need to reset everything and start from scratch:

```
cd docker
docker-compose down -v
cd ../network
./generate.sh
cd ../docker
./prepare_environment.sh clean
docker-compose up -d
```

## Fabric 2.x Channel Management

In Fabric 2.x, the system channel is removed, and channels are managed using the channel participation API. 

To create a channel:
1. Generate the channel configuration using configtxgen
2. Use the channel participation API to submit the channel configuration

To list existing channels:
```
curl -s http://localhost:9443/participation/v1/channels
```

## Logs and Debugging

To view container logs:
```
docker logs orderer.example.com
docker logs peer0.org1.example.com
```

For more detailed diagnostics, use the diagnostic script:
```
./diagnostic.sh
```
