#!/bin/bash

# Exit on first error
set -e

# Define versions
FABRIC_VERSION=2.2.0
CA_VERSION=1.4.9

# Define download URLs
FABRIC_URL=https://github.com/hyperledger/fabric/releases/download/v${FABRIC_VERSION}/hyperledger-fabric-${OSTYPE}-amd64-${FABRIC_VERSION}.tar.gz

echo "===> Downloading Hyperledger Fabric binaries version ${FABRIC_VERSION}"

# Create bin directory if it doesn't exist
mkdir -p bin

# Download Fabric binaries
curl -sSL https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/bootstrap.sh | bash -s -- ${FABRIC_VERSION} ${CA_VERSION} -d -s

echo "===> Hyperledger Fabric binaries installed successfully"
echo "===> Please add the following to your PATH environment variable:"
echo "     export PATH=$PWD/bin:$PATH"