import os
import json
import logging
from datetime import datetime

# Import the Fabric client factory
from .fabric_client_factory import FabricClientFactory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('BlockchainIntegration')

class BlockchainIntegration:
    """
    Integration layer between the CryptaNet data manager and the Hyperledger Fabric network.
    
    This class provides methods for storing and retrieving supply chain data from the blockchain,
    as well as querying the ledger for specific data points.
    """
    
    def __init__(self, org_id='Org1', user_id='Admin', channel_name='supplychainchannel', 
                 chaincode_name='supplychain'):
        """
        Initialize the blockchain integration.
        
        Args:
            org_id (str): The ID of the organization (e.g., 'Org1', 'Org2').
            user_id (str): The ID of the user (e.g., 'Admin', 'User1').
            channel_name (str): The name of the channel to use.
            chaincode_name (str): The name of the chaincode to use.
        """
        self.org_id = org_id
        self.user_id = user_id
        self.channel_name = channel_name
        self.chaincode_name = chaincode_name
        
        # Create a Fabric client
        self.client = FabricClientFactory.create_client(
            org_id=org_id,
            user_id=user_id,
            channel_name=channel_name,
            chaincode_name=chaincode_name
        )
        
        if not self.client:
            logger.error("Failed to create Fabric client. Blockchain integration will not work.")
    
    def store_data(self, data_id, organization_id, encrypted_data, data_hash, data_type, access_control=None):
        """
        Store encrypted supply chain data in the blockchain.
        
        Args:
            data_id (str): The ID of the data.
            organization_id (str): The ID of the organization submitting the data.
            encrypted_data (str): The encrypted supply chain data.
            data_hash (str): The hash of the original data for integrity verification.
            data_type (str): The type of supply chain data (e.g., shipment, inventory, production).
            access_control (list, optional): List of organizations that can access this data.
            
        Returns:
            dict: The transaction result.
        """
        if not self.client:
            logger.error("Fabric client is not available. Cannot store data in blockchain.")
            return {
                'success': False,
                'message': 'Blockchain client is not available'
            }
        
        try:
            # Prepare access control list
            if access_control is None:
                access_control = [organization_id]
            
            # Convert access control list to JSON string if it's a list
            if isinstance(access_control, list):
                access_control_str = json.dumps(access_control)
            else:
                access_control_str = access_control
            
            # Convert encrypted data to string if it's bytes
            if isinstance(encrypted_data, bytes):
                encrypted_data = encrypted_data.decode('utf-8')
            
            # Submit transaction to store data
            result = self.client.submit_transaction(
                self.channel_name,
                self.chaincode_name,
                'CreateSupplyChainData',
                [data_id, organization_id, encrypted_data, data_hash, data_type, access_control_str]
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error storing data in blockchain: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_anomaly_status(self, data_id, anomaly_detected, anomaly_score, explanation):
        """
        Update the anomaly status of a supply chain data point.
        
        Args:
            data_id (str): The ID of the data.
            anomaly_detected (bool): Whether an anomaly was detected.
            anomaly_score (float): The anomaly score.
            explanation (str): The explanation of the anomaly.
            
        Returns:
            dict: The transaction result.
        """
        if not self.client:
            logger.error("Fabric client is not available. Cannot update anomaly status.")
            return {
                'success': False,
                'message': 'Blockchain client is not available'
            }
        
        try:
            # Convert explanation to JSON string if it's a dict
            if isinstance(explanation, dict):
                explanation = json.dumps(explanation)
            
            # Submit transaction to update anomaly status
            result = self.client.submit_transaction(
                self.channel_name,
                self.chaincode_name,
                'UpdateAnomalyStatus',
                [data_id, str(anomaly_detected).lower(), str(anomaly_score), explanation]
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error updating anomaly status: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def retrieve_data(self, data_id):
        """
        Retrieve supply chain data from the blockchain.
        
        Args:
            data_id (str): The ID of the data to retrieve.
            
        Returns:
            dict: The retrieved data.
        """
        if not self.client:
            logger.error("Fabric client is not available. Cannot retrieve data from blockchain.")
            return {
                'success': False,
                'message': 'Blockchain client is not available'
            }
        
        try:
            # Query the ledger for the data
            result = self.client.query_ledger(
                self.channel_name,
                self.chaincode_name,
                'ReadSupplyChainData',
                [data_id]
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error retrieving data from blockchain: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def query_data_by_organization(self, organization_id):
        """
        Query supply chain data by organization.
        
        Args:
            organization_id (str): The ID of the organization.
            
        Returns:
            dict: The query result.
        """
        if not self.client:
            logger.error("Fabric client is not available. Cannot query data from blockchain.")
            return {
                'success': False,
                'message': 'Blockchain client is not available'
            }
        
        try:
            # Query the ledger for data by organization
            result = self.client.query_ledger(
                self.channel_name,
                self.chaincode_name,
                'QuerySupplyChainDataByOrg',
                [organization_id]
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error querying data by organization: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def query_data_by_type(self, data_type):
        """
        Query supply chain data by type.
        
        Args:
            data_type (str): The type of supply chain data.
            
        Returns:
            dict: The query result.
        """
        if not self.client:
            logger.error("Fabric client is not available. Cannot query data from blockchain.")
            return {
                'success': False,
                'message': 'Blockchain client is not available'
            }
        
        try:
            # Query the ledger for data by type
            result = self.client.query_ledger(
                self.channel_name,
                self.chaincode_name,
                'QuerySupplyChainDataByType',
                [data_type]
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error querying data by type: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def register_anomaly_event_listener(self, callback):
        """
        Register a listener for anomaly detection events.
        
        Args:
            callback (function): The callback function to invoke when an anomaly is detected.
            
        Returns:
            str: The registration ID.
        """
        if not self.client:
            logger.error("Fabric client is not available. Cannot register event listener.")
            return None
        
        try:
            # Register event listener for anomaly detection events
            reg_id = self.client.register_event_listener(
                self.channel_name,
                self.chaincode_name,
                'AnomalyDetected',
                callback
            )
            
            return reg_id
        
        except Exception as e:
            logger.error(f"Error registering anomaly event listener: {str(e)}")
            return None
    
    def close(self):
        """
        Close the blockchain integration and disconnect from the network.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        if not self.client:
            logger.warning("Fabric client is not available. Nothing to close.")
            return True
        
        try:
            # Disconnect from the network
            return self.client.disconnect()
        
        except Exception as e:
            logger.error(f"Error closing blockchain integration: {str(e)}")
            return False