# CryptaNet Blockchain Network

## Path Management and Environment Setup

The CryptaNet blockchain network uses Hyperledger Fabric, which requires various binary tools. This guide explains how to configure the environment to ensure the tools are always available.

## Quick Start

Use our new convenient wrapper script that handles all path management automatically:

```bash
cd /Users/bhaskar/Desktop/CryptaNet/blockchain
./cryptanet.sh start    # Start the network
./cryptanet.sh status   # Check network status
./cryptanet.sh stop     # Stop the network
```

## Setting Up Environment Permanently

To permanently add Fabric tools to your PATH and avoid "command not found" errors:

```bash
cd /Users/bhaskar/Desktop/CryptaNet/blockchain
./cryptanet.sh env
```

This will add the necessary environment variables to your .zshrc file. After running this command, restart your terminal or run:

```bash
source ~/.zshrc
```

## Manual Network Management

If needed, you can still use the individual scripts directly:

```bash
cd /Users/bhaskar/Desktop/CryptaNet/blockchain/network
./generate.sh        # Generate crypto material and artifacts
./startFabric.sh     # Start the network
./diagnostic.sh      # Run network diagnostics
./reset_network.sh   # Reset the network
```

## Troubleshooting

If you encounter "command not found" errors:

1. Run the environment setup script:
   ```bash
   cd /Users/bhaskar/Desktop/CryptaNet/blockchain
   source ./fabric-env.sh
   ```

2. Check if binaries exist:
   ```bash
   ls -l ./bin
   ```

3. Use the full path to binaries:
   ```bash
   ./bin/cryptogen --help
   ./bin/configtxgen --help
   ```

## Configuration Path Issues

If you encounter errors like "Could not find profile: ThreeOrgsChannel":

1. Check where your configuration files are:
   ```bash
   ./network/configcheck.sh
   ```

2. Ensure FABRIC_CFG_PATH is set correctly:
   ```bash
   export FABRIC_CFG_PATH=/Users/bhaskar/Desktop/CryptaNet/blockchain/network
   ```

3. Run commands from the network directory:
   ```bash
   cd /Users/bhaskar/Desktop/CryptaNet/blockchain/network
   ../bin/configtxgen -profile ThreeOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID supplychainchannel
   ```

## Technical Details

The path management solution includes:

1. A `fabric-env.sh` script that sets up the environment variables
2. Updated operational scripts that automatically locate and use the binaries
3. A unified `cryptanet.sh` wrapper script for all operations
4. Option to permanently add bin directory to PATH in your shell profile
