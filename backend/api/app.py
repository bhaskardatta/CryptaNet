from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import os
import json
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime

# Import CryptaNet components
import sys
sys.path.append('/Users/bhaskar/Desktop/Mini_Project/CryptaNet')
from privacy_layer.privacy_api import PrivacyAPI
from anomaly_detection.anomaly_detection_api import AnomalyDetectionAPI
from explainability.explanation_api.explanation_generator import ExplanationGenerator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'cryptanet-secret-key'
app.config['MODEL_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'anomaly_detection', 'models', 'saved_model.joblib')
app.config['PREPROCESSOR_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'anomaly_detection', 'preprocessing', 'saved_preprocessor.joblib')
app.config['EXPLAINER_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'explainability', 'shap', 'saved_explainer.joblib')

# Initialize components
privacy_api = PrivacyAPI()

# Load anomaly detection model if it exists
anomal_detection_api = None
if os.path.exists(app.config['MODEL_PATH']):
    anomaly_detection_api = AnomalyDetectionAPI.load_model(
        app.config['MODEL_PATH'],
        app.config['PREPROCESSOR_PATH'] if os.path.exists(app.config['PREPROCESSOR_PATH']) else None
    )
else:
    anomaly_detection_api = AnomalyDetectionAPI()

# Load explainer if it exists
explanation_generator = None
if os.path.exists(app.config['EXPLAINER_PATH']) and anomaly_detection_api is not None:
    explanation_generator = ExplanationGenerator.load(
        app.config['EXPLAINER_PATH'],
        model=anomaly_detection_api.model
    )
else:
    explanation_generator = ExplanationGenerator()

# Mock user database for demonstration
users_db = {
    'admin': {
        'password': generate_password_hash('admin'),
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('user'),
        'role': 'user'
    }
}

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Role-based access control decorator
def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if users_db.get(current_user, {}).get('role') != 'admin':
            return jsonify({'message': 'Admin privileges required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic realm="Login required!"'}), 401

    username = auth.get('username')
    password = auth.get('password')

    if username not in users_db:
        return jsonify({'message': 'User not found!'}), 401

    if check_password_hash(users_db[username]['password'], password):
        token = jwt.encode({
            'username': username,
            'role': users_db[username]['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'token': token,
            'username': username,
            'role': users_db[username]['role']
        })

    return jsonify({'message': 'Invalid credentials!'}), 401

# Privacy Layer API
@app.route('/api/privacy/encrypt', methods=['POST'])
@token_required
def encrypt_data(current_user):
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        encrypted = privacy_api.encrypt_data(data)
        return jsonify({
            'encrypted_data': encrypted['encrypted_data'].decode('utf-8'),
            'data_hash': encrypted['data_hash']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/privacy/decrypt', methods=['POST'])
@token_required
def decrypt_data(current_user):
    encrypted_data = request.json.get('encrypted_data')
    data_hash = request.json.get('data_hash')
    
    if not encrypted_data or not data_hash:
        return jsonify({'error': 'Encrypted data and hash required'}), 400

    try:
        # Convert string back to bytes
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
            
        decrypted, is_valid = privacy_api.decrypt_data({
            'encrypted_data': encrypted_data,
            'data_hash': data_hash
        })
        
        return jsonify({
            'decrypted_data': decrypted,
            'is_valid': is_valid
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/privacy/selective-disclosure', methods=['POST'])
@token_required
def selective_disclosure(current_user):
    data = request.json.get('data')
    fields_to_disclose = request.json.get('fields_to_disclose')
    
    if not data or not fields_to_disclose:
        return jsonify({'error': 'Data and fields to disclose required'}), 400

    try:
        disclosed = privacy_api.selective_disclosure(data, fields_to_disclose)
        return jsonify(disclosed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Anomaly Detection API
@app.route('/api/anomaly-detection/detect', methods=['POST'])
@token_required
def detect_anomalies(current_user):
    data = request.json.get('data')
    threshold = request.json.get('threshold')
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Convert to DataFrame if it's a list of dictionaries
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        # Detect anomalies
        predictions, scores = anomaly_detection_api.predict(data, threshold)
        
        # Generate explanations for anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        explanations = []
        
        if explanation_generator.is_fitted and len(anomaly_indices) > 0:
            for idx in anomaly_indices:
                explanation = explanation_generator.explain_anomaly(
                    data.iloc[idx] if isinstance(data, pd.DataFrame) else data[idx],
                    original_data=data,
                    include_visualizations=False
                )
                explanation['index'] = int(idx)
                explanations.append(explanation)
        
        return jsonify({
            'predictions': predictions.tolist(),
            'scores': scores.tolist(),
            'anomalies': anomaly_indices.tolist(),
            'explanations': explanations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/anomaly-detection/train', methods=['POST'])
@token_required
@admin_required
def train_model(current_user):
    data = request.json.get('data')
    numerical_features = request.json.get('numerical_features')
    categorical_features = request.json.get('categorical_features')
    timestamp_col = request.json.get('timestamp_col')
    value_cols = request.json.get('value_cols')
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Convert to DataFrame if it's a list of dictionaries
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        # Train the model
        anomaly_detection_api.fit(
            data,
            numerical_features,
            categorical_features,
            timestamp_col,
            value_cols
        )
        
        # Save the model
        os.makedirs(os.path.dirname(app.config['MODEL_PATH']), exist_ok=True)
        anomaly_detection_api.save_model(
            app.config['MODEL_PATH'],
            app.config['PREPROCESSOR_PATH']
        )
        
        # Train the explainer
        if not explanation_generator.is_fitted:
            explanation_generator.fit(data)
            os.makedirs(os.path.dirname(app.config['EXPLAINER_PATH']), exist_ok=True)
            explanation_generator.save(app.config['EXPLAINER_PATH'])
        
        return jsonify({'message': 'Model trained successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Explainability API
@app.route('/api/explainability/explain', methods=['POST'])
@token_required
def explain_anomaly(current_user):
    data_point = request.json.get('data_point')
    original_data = request.json.get('original_data')
    include_visualizations = request.json.get('include_visualizations', True)
    
    if not data_point:
        return jsonify({'error': 'No data point provided'}), 400

    try:
        # Convert to DataFrame if it's a list of dictionaries
        if original_data and isinstance(original_data, list):
            original_data = pd.DataFrame(original_data)
        
        # Generate explanation
        explanation = explanation_generator.explain_anomaly(
            data_point,
            original_data=original_data,
            include_visualizations=include_visualizations
        )
        
        return jsonify(explanation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Blockchain API (Mock implementation)
@app.route('/api/blockchain/submit-data', methods=['POST'])
@token_required
def submit_data_to_blockchain(current_user):
    data = request.json.get('data')
    organization_id = request.json.get('organization_id')
    data_type = request.json.get('data_type')
    access_control = request.json.get('access_control', [])
    
    if not data or not organization_id or not data_type:
        return jsonify({'error': 'Data, organization ID, and data type required'}), 400

    try:
        # Encrypt the data
        encrypted = privacy_api.encrypt_data(data)
        
        # Mock blockchain submission
        # In a real implementation, this would interact with the Hyperledger Fabric SDK
        blockchain_response = {
            'id': f"data_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'organizationId': organization_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'encryptedData': encrypted['encrypted_data'].decode('utf-8'),
            'dataHash': encrypted['data_hash'],
            'dataType': data_type,
            'accessControl': access_control,
            'anomalyDetected': False,
            'anomalyScore': 0.0,
            'explanation': ""
        }
        
        return jsonify(blockchain_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/query-data', methods=['GET'])
@token_required
def query_blockchain_data(current_user):
    organization_id = request.args.get('organization_id')
    
    if not organization_id:
        return jsonify({'error': 'Organization ID required'}), 400

    try:
        # Mock blockchain query
        # In a real implementation, this would interact with the Hyperledger Fabric SDK
        mock_data = [
            {
                'id': f"data_20230101{i:02d}0000",
                'organizationId': organization_id,
                'timestamp': f"2023-01-01T{i:02d}:00:00",
                'encryptedData': "encrypted_data_placeholder",
                'dataHash': "data_hash_placeholder",
                'dataType': "shipment" if i % 3 == 0 else "inventory" if i % 3 == 1 else "production",
                'accessControl': [organization_id],
                'anomalyDetected': i % 5 == 0,
                'anomalyScore': 0.8 if i % 5 == 0 else 0.0,
                'explanation': "Unusual shipment delay" if i % 5 == 0 else ""
            } for i in range(1, 11)
        ]
        
        return jsonify(mock_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/update-anomaly', methods=['POST'])
@token_required
@admin_required
def update_anomaly_status(current_user):
    data_id = request.json.get('data_id')
    anomaly_detected = request.json.get('anomaly_detected')
    anomaly_score = request.json.get('anomaly_score')
    explanation = request.json.get('explanation')
    
    if not data_id or anomaly_detected is None or anomaly_score is None:
        return jsonify({'error': 'Data ID, anomaly status, and score required'}), 400

    try:
        # Mock blockchain update
        # In a real implementation, this would interact with the Hyperledger Fabric SDK
        blockchain_response = {
            'id': data_id,
            'anomalyDetected': anomaly_detected,
            'anomalyScore': anomaly_score,
            'explanation': explanation or ""
        }
        
        return jsonify(blockchain_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'components': {
            'privacy_layer': 'available',
            'anomaly_detection': 'available' if anomaly_detection_api.is_fitted else 'not trained',
            'explainability': 'available' if explanation_generator.is_fitted else 'not trained'
        }
    })

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)