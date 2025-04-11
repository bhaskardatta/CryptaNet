# Hyperledger Fabric on Apple Silicon (M1/M2) Macs

## Problem

When trying to run Hyperledger Fabric on Apple Silicon (M1/M2) Macs, you may encounter errors like:

```
Error response from daemon: no matching manifest for linux/arm64/v8 in the manifest list entries: no match for platform in manifest: not found
```

This happens because the official Hyperledger Fabric Docker images don't have native support for the ARM64 architecture used by Apple Silicon chips.

## Solution

The solution is to use Docker's platform flag to pull the AMD64 images and run them using emulation. This repository includes a script that automates this process.

### Using the provided script

1. Make sure Docker is running on your Mac
2. Run the script to pull the correct images:

```bash
./pull-fabric-images-arm64.sh
```

This script will:
- Pull the Hyperledger Fabric images with the `--platform linux/amd64` flag
- Tag them appropriately so they can be used by the Fabric scripts
- List the successfully pulled images

### What's happening behind the scenes

The script uses Docker's multi-architecture support to pull AMD64 images and run them on ARM64 using emulation. While this works, be aware that:

1. Performance may be slower than native ARM64 images
2. Some operations might consume more memory
3. The emulation layer adds some overhead

### Alternative approaches

If you encounter issues with the emulation approach, you can also:

1. Use a remote Docker environment on an x86_64 machine
2. Use a virtual machine running Linux on x86_64 architecture
3. Wait for official ARM64 support from Hyperledger Fabric

## Troubleshooting

If you still encounter issues after running the script:

1. Make sure Docker has enough resources allocated (memory and CPU)
2. Try restarting Docker
3. Check if there are newer versions of Fabric that might have ARM64 support