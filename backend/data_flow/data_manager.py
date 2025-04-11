import json
import pandas as pd
import numpy as np
import logging
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DataManager')

# Import CryptaNet components
sys.path.append('/Users/bhaskar/Desktop/Mini_Project/CryptaNet')
from privacy_layer.privacy_api import PrivacyAPI
from anomaly_detection.anomaly_detection_api import AnomalyDetectionAPI
from explainability.explanation_api.explanation_generator import ExplanationGenerator

class DataManager:
    """
    Manages the flow of data between different components of the CryptaNet system.
    
    This class provides methods for processing, encrypting, and storing data in the blockchain,
    as well as retrieving and decrypting data for analysis and visualization.
    """
    
    def __init__(self, privacy_api=None, anomaly_detection_api=None, explanation_generator=None, blockchain_client=None):
        """
        Initialize the data manager.
        
        Args:
            privacy_api (PrivacyAPI, optional): The privacy API for encryption and decryption.
            anomaly_detection_api (AnomalyDetectionAPI, optional): The anomaly detection API.
            explanation_generator (ExplanationGenerator, optional): The explanation generator.
            blockchain_client: The blockchain client for interacting with the Hyperledger Fabric network.
        """
        self.privacy_api = privacy_api or PrivacyAPI()
        self.anomaly_detection_api = anomaly_detection_api or AnomalyDetectionAPI()
        self.explanation_generator = explanation_generator or ExplanationGenerator()
        self.blockchain_client = blockchain_client
    
    def process_supply_chain_data(self, data, organization_id, data_type, access_control=None):
        """
        Process supply chain data through the CryptaNet pipeline.
        
        This method takes raw supply chain data, processes it through the privacy layer,
        anomaly detection, and explainability components, and stores it in the blockchain.
        
        Args:
            data (dict or DataFrame): The supply chain data to process.
            organization_id (str): The ID of the organization submitting the data.
            data_type (str): The type of supply chain data (e.g., shipment, inventory, production).
            access_control (list, optional): List of organizations that can access this data.
            
        Returns:
            dict: The processed data with anomaly detection results and blockchain transaction ID.
        """
        try:
            # Convert to DataFrame if it's a dictionary
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # Step 1: Detect anomalies
            anomaly_results = self._detect_anomalies(df)
            
            # Step 2: Generate explanations for anomalies
            explanations = self._generate_explanations(df, anomaly_results)
            
            # Step 3: Encrypt the data
            encrypted_data = self._encrypt_data(data)
            
            # Step 4: Store in blockchain
            blockchain_result = self._store_in_blockchain(
                encrypted_data,
                organization_id,
                data_type,
                access_control,
                anomaly_results,
                explanations
            )
            
            # Step 5: Return the results
            return {
                'original_data': data,
                'anomaly_results': anomaly_results,
                'explanations': explanations,
                'blockchain_transaction': blockchain_result
            }
        
        except Exception as e:
            logger.error(f"Error processing supply chain data: {str(e)}")
            raise
    
    def _detect_anomalies(self, data):
        """
        Detect anomalies in the supply chain data.
        
        Args:
            data (DataFrame): The supply chain data.
            
        Returns:
            dict: The anomaly detection results.
        """
        try:
            # Check if the model is fitted
            if not self.anomaly_detection_api.is_fitted:
                logger.warning("Anomaly detection model is not fitted. Skipping anomaly detection.")
                return {
                    'anomalies_detected': False,
                    'predictions': None,
                    'scores': None,
                    'anomaly_indices': []
                }
            
            # Detect anomalies
            predictions, scores = self.anomaly_detection_api.predict(data)
            
            # Find anomaly indices
            anomaly_indices = np.where(predictions == -1)[0].tolist()
            
            return {
                'anomalies_detected': len(anomaly_indices) > 0,
                'predictions': predictions.tolist() if isinstance(predictions, np.ndarray) else predictions,
                'scores': scores.tolist() if isinstance(scores, np.ndarray) else scores,
                'anomaly_indices': anomaly_indices
            }
        
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return {
                'anomalies_detected': False,
                'predictions': None,
                'scores': None,
                'anomaly_indices': [],
                'error': str(e)
            }
    
    def _generate_explanations(self, data, anomaly_results):
        """
        Generate explanations for detected anomalies.
        
        Args:
            data (DataFrame): The supply chain data.
            anomaly_results (dict): The anomaly detection results.
            
        Returns:
            list: The explanations for detected anomalies.
        """
        try:
            # Check if there are any anomalies to explain
            if not anomaly_results['anomalies_detected'] or not anomaly_results['anomaly_indices']:
                return []
            
            # Check if the explainer is fitted
            if not self.explanation_generator.is_fitted:
                logger.warning("Explanation generator is not fitted. Skipping explanation generation.")
                return []
            
            # Generate explanations for each anomaly
            explanations = []
            for idx in anomaly_results['anomaly_indices']:
                try:
                    explanation = self.explanation_generator.explain_anomaly(
                        data.iloc[idx] if isinstance(data, pd.DataFrame) else data[idx],
                        original_data=data,
                        include_visualizations=False
                    )
                    explanation['index'] = idx
                    explanations.append(explanation)
                except Exception as e:
                    logger.error(f"Error generating explanation for anomaly at index {idx}: {str(e)}")
            
            return explanations
        
        except Exception as e:
            logger.error(f"Error generating explanations: {str(e)}")
            return []
    
    def _encrypt_data(self, data):
        """
        Encrypt the supply chain data using the privacy layer.
        
        Args:
            data: The supply chain data to encrypt.
            
        Returns:
            dict: The encrypted data and its hash.
        """
        try:
            # Encrypt the data
            encrypted = self.privacy_api.encrypt_data(data)
            
            return {
                'encrypted_data': encrypted['encrypted_data'],
                'data_hash': encrypted['data_hash']
            }
        
        except Exception as e:
            logger.error(f"Error encrypting data: {str(e)}")
            raise
    
    def _store_in_blockchain(self, encrypted_data, organization_id, data_type, access_control, anomaly_results, explanations):
        """
        Store the encrypted data in the blockchain.
        
        Args:
            encrypted_data (dict): The encrypted data and its hash.
            organization_id (str): The ID of the organization submitting the data.
            data_type (str): The type of supply chain data.
            access_control (list): List of organizations that can access this data.
            anomaly_results (dict): The anomaly detection results.
            explanations (list): The explanations for detected anomalies.
            
        Returns:
            dict: The blockchain transaction result.
        """
        try:
            # Check if blockchain client is available
            if not self.blockchain_client:
                logger.warning("Blockchain client is not available. Skipping blockchain storage.")
                return {
                    'success': False,
                    'message': 'Blockchain client is not available'
                }
            
            # Prepare the data for blockchain storage
            blockchain_data = {
                'id': f"data_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'organizationId': organization_id,
                'timestamp': datetime.now().isoformat(),
                'encryptedData': encrypted_data['encrypted_data'].decode('utf-8') if isinstance(encrypted_data['encrypted_data'], bytes) else encrypted_data['encrypted_data'],
                'dataHash': encrypted_data['data_hash'],
                'dataType': data_type,
                'accessControl': access_control or [organization_id],
                'anomalyDetected': anomaly_results['anomalies_detected'],
                'anomalyScore': max(anomaly_results['scores']) if anomaly_results['scores'] else 0.0,
                'explanation': json.dumps(explanations[0]) if explanations else ""
            }
            
            # Store in blockchain (mock implementation)
            # In a real implementation, this would use the Hyperledger Fabric SDK
            logger.info(f"Storing data in blockchain: {blockchain_data['id']}")
            
            # Mock blockchain response
            blockchain_response = {
                'success': True,
                'transaction_id': f"tx_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'data_id': blockchain_data['id']
            }
            
            return blockchain_response
        
        except Exception as e:
            logger.error(f"Error storing data in blockchain: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def retrieve_data(self, data_id, organization_id):
        """
        Retrieve data from the blockchain and decrypt it.
        
        Args:
            data_id (str): The ID of the data to retrieve.
            organization_id (str): The ID of the organization requesting the data.
            
        Returns:
            dict: The retrieved and decrypted data.
        """
        try:
            # Check if blockchain client is available
            if not self.blockchain_client:
                logger.warning("Blockchain client is not available. Skipping blockchain retrieval.")
                return {
                    'success': False,
                    'message': 'Blockchain client is not available'
                }
            
            # Retrieve from blockchain (mock implementation)
            # In a real implementation, this would use the Hyperledger Fabric SDK
            logger.info(f"Retrieving data from blockchain: {data_id}")
            
            # Mock blockchain data
            blockchain_data = {
                'id': data_id,
                'organizationId': organization_id,
                'timestamp': datetime.now().isoformat(),
                'encryptedData': "mock_encrypted_data",
                'dataHash': "mock_data_hash",
                'dataType': "shipment",
                'accessControl': [organization_id],
                'anomalyDetected': False,
                'anomalyScore': 0.0,
                'explanation': ""
            }
            
            # Check access control
            if organization_id not in blockchain_data['accessControl'] and organization_id != blockchain_data['organizationId']:
                return {
                    'success': False,
                    'message': 'Access denied'
                }
            
            # Decrypt the data (mock implementation)
            # In a real implementation, this would use the privacy layer to decrypt the data
            decrypted_data = {
                'mock_decrypted_data': 'This is mock decrypted data'
            }
            
            return {
                'success': True,
                'data': decrypted_data,
                'metadata': {
                    'id': blockchain_data['id'],
                    'organizationId': blockchain_data['organizationId'],
                    'timestamp': blockchain_data['timestamp'],
                    'dataType': blockchain_data['dataType'],
                    'anomalyDetected': blockchain_data['anomalyDetected'],
                    'anomalyScore': blockchain_data['anomalyScore'],
                    'explanation': blockchain_data['explanation']
                }
            }
        
        except Exception as e:
            logger.error(f"Error retrieving data: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def query_data(self, organization_id, data_type=None, start_time=None, end_time=None, include_anomalies_only=False):
        """
        Query data from the blockchain based on various criteria.
        
        Args:
            organization_id (str): The ID of the organization requesting the data.
            data_type (str, optional): Filter by data type.
            start_time (str, optional): Filter by start time (ISO format).
            end_time (str, optional): Filter by end time (ISO format).
            include_anomalies_only (bool): Whether to include only anomalous data.
            
        Returns:
            list: The query results.
        """
        try:
            # Check if blockchain client is available
            if not self.blockchain_client:
                logger.warning("Blockchain client is not available. Skipping blockchain query.")
                return {
                    'success': False,
                    'message': 'Blockchain client is not available'
                }
            
            # Query blockchain (mock implementation)
            # In a real implementation, this would use the Hyperledger Fabric SDK
            logger.info(f"Querying blockchain data for organization: {organization_id}")
            
            # Mock query results
            query_results = [
                {
                    'id': f"data_2023010{i}000000",
                    'organizationId': organization_id,
                    'timestamp': f"2023-01-0{i}T00:00:00",
                    'dataType': "shipment" if i % 3 == 0 else "inventory" if i % 3 == 1 else "production",
                    'anomalyDetected': i % 5 == 0,
                    'anomalyScore': 0.8 if i % 5 == 0 else 0.0,
                    'explanation': "Unusual shipment delay" if i % 5 == 0 else ""
                } for i in range(1, 10)
            ]
            
            # Apply filters
            filtered_results = query_results
            
            if data_type:
                filtered_results = [r for r in filtered_results if r['dataType'] == data_type]
            
            if start_time:
                filtered_results = [r for r in filtered_results if r['timestamp'] >= start_time]
            
            if end_time:
                filtered_results = [r for r in filtered_results if r['timestamp'] <= end_time]
            
            if include_anomalies_only:
                filtered_results = [r for r in filtered_results if r['anomalyDetected']]
            
            return {
                'success': True,
                'results': filtered_results,
                'count': len(filtered_results)
            }
        
        except Exception as e:
            logger.error(f"Error querying data: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }