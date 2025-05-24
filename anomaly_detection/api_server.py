#!/usr/bin/env python3
"""
Flask API server for CryptaNet Anomaly Detection Service
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from pathlib import Path
import traceback
import logging

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from anomaly_detection_api import AnomalyDetectionAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize the anomaly detection API
try:
    model_path = current_dir / "saved_models" / "anomaly_detection_model.joblib"
    anomaly_api = AnomalyDetectionAPI(model_path=str(model_path))
    logger.info("Anomaly Detection API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Anomaly Detection API: {e}")
    traceback.print_exc()
    anomaly_api = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'anomaly-detection',
        'api_ready': anomaly_api is not None
    })

@app.route('/detect', methods=['POST'])
def detect_anomaly():
    """Detect anomalies in supply chain data"""
    try:
        if anomaly_api is None:
            return jsonify({'error': 'Anomaly detection API not initialized'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract supply chain data from request
        supply_chain_data = data.get('data')
        if not supply_chain_data:
            return jsonify({'error': 'No supply chain data provided'}), 400
        
        # Perform anomaly detection
        result = anomaly_api.detect_anomaly(supply_chain_data)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error in anomaly detection: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_anomaly():
    """Predict anomalies for new data"""
    try:
        if anomaly_api is None:
            return jsonify({'error': 'Anomaly detection API not initialized'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features for prediction
        features = data.get('features')
        if not features:
            return jsonify({'error': 'No features provided'}), 400
        
        # Make prediction
        prediction = anomaly_api.predict(features)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get service status and statistics"""
    try:
        if anomaly_api is None:
            return jsonify({'error': 'Anomaly detection API not initialized'}), 500
        
        return jsonify({
            'status': 'running',
            'service': 'anomaly-detection',
            'model_loaded': True,
            'endpoints': ['/health', '/detect', '/predict', '/status']
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Anomaly Detection API server on {host}:{port}")
    app.run(host=host, port=port, debug=True)
