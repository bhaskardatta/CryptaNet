#!/bin/bash
# cryptanet.sh - Unified command wrapper for CryptaNet blockchain operations

# Determine script location and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
NETWORK_DIR="${PROJECT_ROOT}/network"
BIN_DIR="${PROJECT_ROOT}/bin"

# Source fabric environment setup
source "${PROJECT_ROOT}/fabric-env.sh"

# Make sure FABRIC_CFG_PATH is set correctly for all commands
# When running commands in the network directory, FABRIC_CFG_PATH should be the network directory
override_env_for_network() {
    if [ "$1" == "start" ] || [ "$1" == "reset" ] || [ "$1" == "channel" ]; then
        export FABRIC_CFG_PATH="${NETWORK_DIR}"
        echo "Setting FABRIC_CFG_PATH to network directory: ${FABRIC_CFG_PATH}"
    fi
}

# Command help function
show_help() {
    echo "CryptaNet Blockchain Network Management Tool"
    echo ""
    echo "Usage: ./cryptanet.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start      - Start the blockchain network"
    echo "  stop       - Stop the blockchain network"
    echo "  reset      - Reset the network (delete all data)"
    echo "  status     - Show network status"
    echo "  diagnose   - Run diagnostics"
    echo "  channel    - Create/manage channels"
    echo "  env        - Configure environment (add to shell profile)"
    echo "  help       - Show this help message"
    echo ""
}

# Function to check if the network directory exists
check_network_dir() {
    if [ ! -d "$NETWORK_DIR" ]; then
        echo "Error: Network directory not found at $NETWORK_DIR"
        exit 1
    fi
}

# Main command logic
case "$1" in
    start)
        check_network_dir
        override_env_for_network "start"
        cd "$NETWORK_DIR" && ./startFabric.sh
        ;;
    stop)
        check_network_dir
        cd "${PROJECT_ROOT}/docker" && docker-compose down
        ;;
    reset)
        check_network_dir
        override_env_for_network "reset"
        cd "$NETWORK_DIR" && ./reset_network.sh
        ;;
    status)
        check_network_dir
        echo "Network Status:"
        docker ps --filter "network=cryptanet" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ;;
    diagnose)
        check_network_dir
        cd "$NETWORK_DIR" && ./diagnostic.sh
        ;;
    channel)
        check_network_dir
        override_env_for_network "channel"
        cd "$NETWORK_DIR" && ./create_channel_manual.sh
        ;;
    env)
        # Add environment settings to shell profile
        "${PROJECT_ROOT}/fabric-env.sh" --add-to-profile
        ;;
    help|*)
        show_help
        ;;
esac
