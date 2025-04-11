# Hyperledger Fabric Network Setup Guide

This guide provides step-by-step instructions for setting up the Hyperledger Fabric network for CryptaNet on Apple Silicon (M1/M2) Macs.

## Prerequisites

- Docker installed and running
- Git installed
- curl installed

## Setup Steps

### 1. Install Hyperledger Fabric Binaries

First, you need to install the Hyperledger Fabric binaries which include tools like `cryptogen` and `configtxgen` that are required for network setup.

```bash
# Navigate to the blockchain directory
cd /Users/bhaskar/Desktop/Mini_Project/CryptaNet/blockchain

# Run the installation script
./install-fabric.sh

# Add the binaries to your PATH
export PATH=$PWD/bin:$PATH
```

### 2. Pull Fabric Docker Images for ARM64

Since you're using an Apple Silicon Mac, you need to pull the Fabric Docker images with the correct platform specification.

```bash
# Navigate to the docker directory
cd /Users/bhaskar/Desktop/Mini_Project/CryptaNet/blockchain/docker

# Run the script to pull images
./pull-fabric-images-arm64.sh
```

### 3. Generate Network Artifacts

Now, generate the network artifacts including certificates and genesis block.

```bash
# Navigate to the network directory
cd /Users/bhaskar/Desktop/Mini_Project/CryptaNet/blockchain/network

# Run the generate script
./generate.sh
```

### 4. Start the Fabric Network

Start the Hyperledger Fabric network using Docker Compose.

```bash
# Run the start script
./startFabric.sh
```

### 5. Verify Network Status

Verify that the network is running correctly.

```bash
# Check running Docker containers
docker ps
```

You should see containers for peers, orderers, and CAs running.

## Troubleshooting

### Common Issues

1. **Command not found errors**: Make sure you've added the Fabric binaries to your PATH as shown in step 1.

2. **Docker errors**: Ensure Docker is running and has enough resources allocated.

3. **Network generation errors**: Check the logs for specific errors. You might need to clean up previous artifacts with:
   ```bash
   cd /Users/bhaskar/Desktop/Mini_Project/CryptaNet/blockchain/network
   rm -rf crypto-config channel-artifacts
   ```

4. **Docker image errors**: If you encounter Docker image issues, try running the pull script again or check Docker's platform settings.

## Next Steps

After setting up the network, you can:

1. Deploy chaincode (smart contracts) to the network
2. Interact with the network using the Fabric SDK
3. Develop applications that use the blockchain network

For more information, refer to the Hyperledger Fabric documentation: https://hyperledger-fabric.readthedocs.io/