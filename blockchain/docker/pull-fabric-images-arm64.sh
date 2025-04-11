#!/bin/bash

# Script to pull Hyperledger Fabric Docker images for Apple Silicon (ARM64) Macs
# This script uses the --platform flag to pull images for the correct architecture

set -e

# Define versions
FABRIC_VERSION="2.2.0"
CA_VERSION="1.4.9"

echo "===> Pulling Hyperledger Fabric Docker images with platform specification"

# Create an array of the images to pull
FABRIC_IMAGES=("peer" "orderer" "ccenv" "baseos")
CA_IMAGES=("ca")

# Pull Fabric images with platform specification
echo "===> Pulling Fabric Images with platform linux/amd64"
for image in "${FABRIC_IMAGES[@]}"; do
  echo "====> Pulling docker.io/hyperledger/fabric-$image:$FABRIC_VERSION"
  docker pull --platform linux/amd64 "docker.io/hyperledger/fabric-$image:$FABRIC_VERSION"
  # Tag the image without platform to ensure scripts work correctly
  docker tag "docker.io/hyperledger/fabric-$image:$FABRIC_VERSION" "hyperledger/fabric-$image:$FABRIC_VERSION"
done

# Pull Fabric CA images with platform specification
echo "===> Pulling Fabric CA Image with platform linux/amd64"
for image in "${CA_IMAGES[@]}"; do
  echo "====> Pulling docker.io/hyperledger/fabric-$image:$CA_VERSION"
  docker pull --platform linux/amd64 "docker.io/hyperledger/fabric-$image:$CA_VERSION"
  # Tag the image without platform to ensure scripts work correctly
  docker tag "docker.io/hyperledger/fabric-$image:$CA_VERSION" "hyperledger/fabric-$image:$CA_VERSION"
done

# List the pulled images
echo "===> List out hyperledger docker images"
docker images | grep hyperledger

echo "===> Successfully pulled Hyperledger Fabric images for ARM64 architecture"
echo "===> You can now proceed with running the test network"