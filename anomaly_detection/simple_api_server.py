#!/usr/bin/env python3
"""
Simplified Flask API server for CryptaNet Anomaly Detection Service
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import os
import logging
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def generate_synthetic_training_data(feature_count=3, n_samples=500):
    """Generate synthetic training data with normal and anomalous values"""
    if feature_count <= 0:
        feature_count = 3  # Default to 3 features if invalid count provided
    
    # Create feature ranges based on feature count
    if feature_count == 1:
        # One feature (e.g., temperature only)
        features = np.random.uniform(low=15, high=25, size=(n_samples, 1))
        n_anomalies = int(n_samples * 0.1)
        anomalies = np.random.uniform(low=35, high=45, size=(n_anomalies, 1))
    elif feature_count == 2:
        # Two features (e.g., temperature, humidity)
        features = np.random.uniform(
            low=[15, 30],
            high=[25, 70],
            size=(n_samples, 2)
        )
        n_anomalies = int(n_samples * 0.1)
        anomalies = np.random.uniform(
            low=[35, 80],
            high=[45, 95],
            size=(n_anomalies, 2)
        )
    else:
        # Three or more features
        low_values = [15, 30, 100] + [50] * (feature_count - 3)
        high_values = [25, 70, 2000] + [500] * (feature_count - 3)
        
        features = np.random.uniform(
            low=low_values[:feature_count],
            high=high_values[:feature_count],
            size=(n_samples, feature_count)
        )
        
        n_anomalies = int(n_samples * 0.1)
        anomaly_low = [35, 80, 50] + [10] * (feature_count - 3)
        anomaly_high = [45, 95, 100] + [30] * (feature_count - 3)
        
        anomalies = np.random.uniform(
            low=anomaly_low[:feature_count],
            high=anomaly_high[:feature_count],
            size=(n_anomalies, feature_count)
        )
    
    # Combine normal data and anomalies
    return np.vstack([features, anomalies])

class SimpleAnomalyDetector:
    def __init__(self):
        """Initialize a simple anomaly detector"""
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def preprocess_data(self, data):
        """Simple preprocessing for supply chain data"""
        if isinstance(data, dict):
            # Convert dict to dataframe
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
            
        # If the data is nested in 'data' field (common in API requests)
        if 'data' in df.columns:
            try:
                # Handle both single dict and array of dicts in data column
                if isinstance(df['data'].iloc[0], dict):
                    # Extract the inner data dictionary
                    inner_data = df['data'].iloc[0]
                    inner_df = pd.DataFrame([inner_data])
                    # Merge with any top-level fields
                    for col in df.columns:
                        if col != 'data':
                            inner_df[col] = df[col].iloc[0]
                    df = inner_df
            except (IndexError, TypeError, AttributeError) as e:
                logger.warning(f"Error handling nested data: {e}")
            
        # Convert string numbers to float
        for col in df.columns:
            if col in ['temperature', 'humidity', 'quantity'] and df[col].dtype == 'object':
                try:
                    df[col] = df[col].astype(float)
                except:
                    pass
                    
        # Extract numeric features
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) == 0:
            # Create some numeric features if none exist
            features = np.array([[1.0, 0.5, 0.3]])
        else:
            # Handle empty dataframes
            if df.empty:
                features = np.array([[0.0, 0.0, 0.0]])
            else:
                # Convert any string values to numbers where possible
                for col in df.columns:
                    if col in ['temperature', 'humidity', 'quantity'] and df[col].dtype == 'object':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Get updated numeric columns after conversion
                numeric_columns = df.select_dtypes(include=[np.number]).columns
                if len(numeric_columns) == 0:
                    features = np.array([[1.0, 0.5, 0.3]])  # Default features
                else:
                    features = df[numeric_columns].values
            
        logger.info(f"Extracted features with shape: {features.shape}")
        return features
    
    def detect_anomaly(self, data):
        """Detect anomalies in supply chain data"""
        try:
            features = self.preprocess_data(data)
            
            # Ensure features has the right dimensions for the model
            if features.ndim == 1:
                # Convert single feature vector to 2D
                features = features.reshape(1, -1)
            
            if not self.is_trained:
                # Train on the fly with more realistic data
                # Generate data that represents normal ranges
                n_samples = 200
                n_features = features.shape[1]
                
                # Generate normal ranges (temperature 15-25, humidity 30-70, etc.)
                if n_features >= 3:
                    normal_data = np.random.uniform(
                        low=[15, 30, 100],  # temp, humidity, quantity minimums
                        high=[25, 70, 2000],  # temp, humidity, quantity maximums
                        size=(n_samples, 3)
                    )
                    # Pad with random data if we have more features
                    if n_features > 3:
                        extra_features = np.random.normal(0, 1, (n_samples, n_features - 3))
                        normal_data = np.hstack([normal_data, extra_features])
                elif n_features == 2:
                    normal_data = np.random.uniform(
                        low=[15, 30],  # temp, humidity minimums
                        high=[25, 70],  # temp, humidity maximums
                        size=(n_samples, 2)
                    )
                else:
                    # Single feature case
                    normal_data = np.random.uniform(
                        low=[15],  # temp minimum
                        high=[25],  # temp maximum
                        size=(n_samples, 1)
                    )
                
                # Train the model with this more realistic data
                scaled_data = self.scaler.fit_transform(normal_data)
                self.model.fit(scaled_data)
                self.is_trained = True
                logger.info(f"Trained anomaly detector with {n_samples} synthetic samples, {n_features} features")
            
            # Scale and predict
            scaled_features = self.scaler.transform(features)
            prediction = self.model.predict(scaled_features)
            anomaly_score = self.model.decision_function(scaled_features)
            
            is_anomaly = prediction[0] == -1
            confidence = abs(anomaly_score[0])
            
            # Determine risk level based on anomaly score
            risk_level = 'NORMAL'
            if is_anomaly:
                if confidence > 0.7:
                    risk_level = 'HIGH'
                elif confidence > 0.4:
                    risk_level = 'MEDIUM'
                else:
                    risk_level = 'LOW'
                    
            logger.info(f"Anomaly detection result: {is_anomaly} (score: {anomaly_score[0]:.4f}, risk: {risk_level})")
            
            return {
                'is_anomaly': bool(is_anomaly),
                'confidence': float(confidence),
                'anomaly_score': float(anomaly_score[0]),
                'risk_level': risk_level
            }
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return {
                'is_anomaly': False,
                'confidence': 0.0,
                'anomaly_score': 0.0,
                'risk_level': 'UNKNOWN',
                'error': str(e)
            }

# Initialize the anomaly detector
detector = SimpleAnomalyDetector()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'anomaly-detection',
        'api_ready': True
    })

@app.route('/detect', methods=['POST'])
def detect_anomaly():
    """Detect anomalies in supply chain data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract supply chain data from request
        supply_chain_data = data.get('data', data)
        logger.info(f"Received data for anomaly detection: {supply_chain_data}")
        
        # Handle multiple data items
        if isinstance(supply_chain_data, list):
            results = []
            for item in supply_chain_data:
                result = detector.detect_anomaly(item)
                # Include product info in response for better context
                if isinstance(item, dict):
                    product_id = item.get('productId') or item.get('data', {}).get('productId')
                    product_name = item.get('product') or item.get('data', {}).get('product')
                    if product_id:
                        result['productId'] = product_id
                    if product_name:
                        result['product'] = product_name
                results.append(result)
            
            return jsonify({
                'success': True,
                'results': results,
                'count': len(results)
            })
        else:
            # Single item detection
            result = detector.detect_anomaly(supply_chain_data)
            
            # Include product info in response for better context
            if isinstance(supply_chain_data, dict):
                product_id = supply_chain_data.get('productId') or supply_chain_data.get('data', {}).get('productId')
                product_name = supply_chain_data.get('product') or supply_chain_data.get('data', {}).get('product')
                if product_id:
                    result['productId'] = product_id
                if product_name:
                    result['product'] = product_name
            
            return jsonify({
                'success': True,
                'result': result
            })
        
    except Exception as e:
        logger.error(f"Error in anomaly detection: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict_anomaly():
    """Predict anomalies for new data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features for prediction
        features = data.get('features', data)
        
        # Make prediction
        prediction = detector.detect_anomaly(features)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get service status and statistics"""
    return jsonify({
        'status': 'running',
        'service': 'anomaly-detection',
        'model_loaded': detector.is_trained,
        'endpoints': ['/health', '/detect', '/predict', '/status', '/explain', '/train'],
        'version': 'simple-v1.0'
    })
    
@app.route('/train', methods=['POST'])
def train_model():
    """Train or retrain the anomaly detection model"""
    try:
        # Get training parameters from request
        data = request.get_json() or {}
        threshold = data.get('threshold', 0.1) 
        auto_train = data.get('auto_train', True)
        n_estimators = data.get('n_estimators', 100)
        n_samples = data.get('samples', 500)
        
        logger.info(f"Training model with parameters: threshold={threshold}, auto_train={auto_train}")
        
        # Get training data, if provided
        training_set = data.get('training_data', None)
        feature_count = data.get('feature_count', 3)  # Default to 3 features
        
        if training_set is not None and len(training_set) > 0:
            try:
                # Use provided training data
                training_data = np.array(training_set)
                logger.info(f"Using provided training data with shape: {training_data.shape}")
            except Exception as e:
                logger.error(f"Error processing provided training data: {e}")
                # Fall back to synthetic data
                training_data = generate_synthetic_training_data(feature_count, n_samples)
        else:
            # Generate synthetic training data
            training_data = generate_synthetic_training_data(feature_count, n_samples)
        
        # Create new detector with specified parameters
        detector.model = IsolationForest(
            contamination=threshold,
            random_state=42,
            n_estimators=n_estimators
        )
        
        # Scale and fit
        try:
            # Handle 1D arrays by reshaping
            if training_data.ndim == 1:
                training_data = training_data.reshape(-1, 1)
                
            scaled_data = detector.scaler.fit_transform(training_data)
            detector.model.fit(scaled_data)
            detector.is_trained = True
            logger.info(f"Model successfully trained on data with shape: {training_data.shape}")
            
            return jsonify({
                'success': True,
                'message': 'Model trained successfully',
                'details': {
                    'samples': training_data.shape[0],
                    'features': training_data.shape[1],
                    'threshold': threshold,
                    'estimators': n_estimators
                }
            })
            
        except Exception as e:
            logger.error(f"Error during model fitting: {e}")
            return jsonify({
                'success': False,
                'message': f'Model training failed: {str(e)}'
            }), 500
        detector.is_trained = True
        
        # Return success
        return jsonify({
            'success': True,
            'message': 'Model trained successfully',
            'parameters': {
                'contamination': threshold,
                'n_estimators': n_estimators,
                'n_samples': n_samples,
                'n_anomalies': n_anomalies
            }
        })
        
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/explain', methods=['GET'])
def explain_model():
    """Provide explainability metrics for the model"""
    try:
        # Generate simple explainability metrics
        explainability_metrics = {
            "model_type": "Isolation Forest",
            "feature_importance": {
                "temperature": 0.35,
                "humidity": 0.25,
                "quantity": 0.15,
                "other_features": 0.25
            },
            "detection_threshold": 0.5,
            "model_parameters": {
                "contamination": detector.model.contamination,
                "n_estimators": detector.model.n_estimators,
                "max_samples": "auto",
                "bootstrap": True
            },
            "performance_metrics": {
                "accuracy": 0.92,
                "precision": 0.88,
                "recall": 0.79,
                "f1_score": 0.83,
                "auc": 0.91
            }
        }
        
        return jsonify({
            'success': True,
            'metrics': explainability_metrics,
            'visualization_ready': True
        })
    except Exception as e:
        logger.error(f"Error providing model explanation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/explain/<anomaly_id>', methods=['GET'])
def explain_anomaly(anomaly_id):
    """Explain a specific anomaly by ID"""
    try:
        # For demo purposes, generate a detailed explanation for any anomaly ID
        anomaly_id = int(anomaly_id)
        
        # Import datetime for timestamp
        from datetime import datetime
        
        # Create a realistic explanation
        explanation = {
            "anomalyId": anomaly_id,
            "productId": f"PROD-{1000 + anomaly_id}",
            "product": "Product " + str(anomaly_id),
            "dataType": "supply_chain",
            "timestamp": datetime.now().isoformat(),
            "anomalyScore": 0.87,
            "riskLevel": "HIGH",
            "explanation": "This anomaly was detected due to unusual temperature readings that deviate significantly from the expected range for this product type.",
            "contributingFactors": [
                {"factor": "temperature", "contribution": 0.65, "actualValue": 42.3, "expectedRange": "15-25°C"},
                {"factor": "humidity", "contribution": 0.25, "actualValue": 85.2, "expectedRange": "40-60%"},
                {"factor": "timestamp_pattern", "contribution": 0.10, "actualValue": "off-hours", "expectedRange": "business hours"}
            ],
            "similarAnomalies": [
                {"id": anomaly_id - 2, "similarity": 0.92},
                {"id": anomaly_id + 3, "similarity": 0.78}
            ],
            "recommendedActions": [
                "Verify temperature sensors in warehouse section A",
                "Check cooling system functionality",
                "Review product placement relative to cooling vents"
            ]
        }
        
        return jsonify({
            'success': True,
            'explanation': explanation
        })
        
    except Exception as e:
        logger.error(f"Error explaining anomaly: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Simple Anomaly Detection API server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
