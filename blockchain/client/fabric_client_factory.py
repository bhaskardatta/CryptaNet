import os
import json
import logging
from .fabric_client import FabricClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FabricClientFactory')

class FabricClientFactory:
    """
    Factory for creating and configuring Hyperledger Fabric clients.
    
    This class provides methods for creating and configuring Fabric clients
    for different organizations and users.
    """
    
    @staticmethod
    def create_client(org_id='Org1', user_id='Admin', channel_name='supplychainchannel', 
                     chaincode_name='supplychain', connection_profile=None):
        """
        Create a new Fabric client.
        
        Args:
            org_id (str): The ID of the organization (e.g., 'Org1', 'Org2').
            user_id (str): The ID of the user (e.g., 'Admin', 'User1').
            channel_name (str): The name of the channel to use.
            chaincode_name (str): The name of the chaincode to use.
            connection_profile (dict, optional): The connection profile for the Fabric network.
            
        Returns:
            FabricClient: A configured Fabric client.
        """
        try:
            # Load connection profile if provided
            if connection_profile is None:
                # Use default connection profile
                connection_profile = {
                    'org_id': org_id,
                    'user_id': user_id,
                    'channel_name': channel_name,
                    'chaincode_name': chaincode_name,
                    # Additional configuration would go here in a real implementation
                }
            
            # Create and configure the client
            client = FabricClient(config=connection_profile)
            
            # Connect to the network
            success = client.connect()
            if not success:
                logger.error(f"Failed to connect to Fabric network for {user_id}@{org_id}")
                return None
            
            return client
        
        except Exception as e:
            logger.error(f"Error creating Fabric client: {str(e)}")
            return None
    
    @staticmethod
    def create_client_from_wallet(wallet_path, identity_label, connection_profile_path):
        """
        Create a new Fabric client from a wallet.
        
        In a real implementation, this would use the Fabric SDK to create a client
        from a wallet containing identities and a connection profile.
        
        Args:
            wallet_path (str): Path to the wallet directory.
            identity_label (str): Label of the identity to use.
            connection_profile_path (str): Path to the connection profile JSON file.
            
        Returns:
            FabricClient: A configured Fabric client.
        """
        try:
            # In a real implementation, this would load the wallet and connection profile
            # For now, we just simulate this process
            logger.info(f"Creating Fabric client from wallet: {wallet_path}, identity: {identity_label}")
            
            # Load connection profile
            if os.path.exists(connection_profile_path):
                with open(connection_profile_path, 'r') as f:
                    connection_profile = json.load(f)
            else:
                logger.error(f"Connection profile not found: {connection_profile_path}")
                return None
            
            # Extract organization ID from connection profile
            org_id = connection_profile.get('client', {}).get('organization', 'Org1')
            
            # Create and configure the client
            client = FabricClient(config={
                'org_id': org_id,
                'user_id': identity_label,
                'wallet_path': wallet_path,
                'connection_profile': connection_profile
            })
            
            # Connect to the network
            success = client.connect()
            if not success:
                logger.error(f"Failed to connect to Fabric network for {identity_label}@{org_id}")
                return None
            
            return client
        
        except Exception as e:
            logger.error(f"Error creating Fabric client from wallet: {str(e)}")
            return None