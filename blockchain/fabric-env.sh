#!/bin/bash
# fabric-env.sh - Environment setup script for Hyperledger Fabric

# Determine script location and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}" && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"

# Export PATH to include the Fabric binaries
export PATH="${BIN_DIR}:$PATH"

# Export environment variables - configtx.yaml is in the network directory
export FABRIC_CFG_PATH="${PROJECT_ROOT}/network"

# Check for required binaries
REQUIRED_BINS=("cryptogen" "configtxgen" "configtxlator" "peer" "orderer")
MISSING_BINS=0

echo "Checking Hyperledger Fabric binary availability..."
for BIN in "${REQUIRED_BINS[@]}"; do
    if [ ! -f "${BIN_DIR}/${BIN}" ]; then
        echo "Missing binary: ${BIN}"
        MISSING_BINS=$((MISSING_BINS+1))
    else
        # Make sure it's executable
        chmod +x "${BIN_DIR}/${BIN}"
    fi
done

# If binaries are missing, offer to download them
if [ $MISSING_BINS -gt 0 ]; then
    echo "One or more required binaries are missing."
    
    if [ -f "${PROJECT_ROOT}/install-fabric.sh" ]; then
        echo "Would you like to download the missing binaries? (y/n)"
        read -r RESPONSE
        if [[ "$RESPONSE" =~ ^[Yy]$ ]]; then
            (cd "${PROJECT_ROOT}" && ./install-fabric.sh)
        else
            echo "Please install the missing binaries manually."
        fi
    else
        echo "Error: install-fabric.sh script not found. Please install binaries manually."
    fi
else
    echo "All required binaries found in ${BIN_DIR}"
fi

# Display environment information
echo ""
echo "=== Hyperledger Fabric Environment ==="
echo "PROJECT_ROOT: ${PROJECT_ROOT}"
echo "BIN_DIR: ${BIN_DIR}"
echo "PATH: $PATH"
echo "FABRIC_CFG_PATH: ${FABRIC_CFG_PATH}"
echo ""

# Optional: add this to user's zsh profile
if [[ "$1" == "--add-to-profile" ]]; then
    PROFILE_FILE="$HOME/.zshrc"
    
    # Check if the profile already contains our settings
    if grep -q "# Hyperledger Fabric Environment" "$PROFILE_FILE"; then
        echo "Environment settings already exist in $PROFILE_FILE"
    else
        echo "Adding environment settings to $PROFILE_FILE"
        echo "" >> "$PROFILE_FILE"
        echo "# Hyperledger Fabric Environment" >> "$PROFILE_FILE"
        echo "export PATH=\"${BIN_DIR}:\$PATH\"" >> "$PROFILE_FILE"
        echo "export FABRIC_CFG_PATH=\"${FABRIC_CFG_PATH}\"" >> "$PROFILE_FILE"
        echo "Environment settings added to $PROFILE_FILE"
        echo "Please run 'source $PROFILE_FILE' or start a new terminal to apply changes"
    fi
fi

echo "Fabric environment setup complete."
