#!/bin/bash

# This script prepares the environment for running the Fabric network
# It handles directory creation and permissions for volumes

# Create the orderer data directory if it doesn't exist
mkdir -p ./orderer-data

# Set appropriate permissions
chmod -R 777 ./orderer-data

# Clean existing channel artifacts if requested
if [ "$1" == "clean" ]; then
  echo "Cleaning previous channel artifacts and crypto material..."
  rm -rf ./channel-artifacts
  rm -rf ./crypto-config
  rm -rf ./orderer-data/*
fi

# Create empty directories if they don't exist
mkdir -p ./channel-artifacts
mkdir -p ./crypto-config
mkdir -p ./chaincode

echo "Environment prepared successfully."
