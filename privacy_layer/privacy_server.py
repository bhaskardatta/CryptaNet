#!/usr/bin/env python3
"""
Flask API server for CryptaNet Privacy Layer Service
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import base64
from pathlib import Path
import logging
from cryptography.fernet import Fernet
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class SimplePrivacyLayer:
    """Simplified privacy layer for encryption/decryption operations"""
    
    def __init__(self):
        """Initialize with a default encryption key"""
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        
    def encrypt_data(self, data):
        """Encrypt data and return encrypted data with hash"""
        try:
            # Convert data to JSON string
            if isinstance(data, dict):
                data_str = json.dumps(data, sort_keys=True)
            else:
                data_str = str(data)
            
            # Encrypt the data
            encrypted_data = self.cipher.encrypt(data_str.encode())
            
            # Generate hash for integrity
            data_hash = hashlib.sha256(data_str.encode()).hexdigest()
            
            return {
                'encrypted_data': base64.b64encode(encrypted_data).decode(),
                'hash': data_hash,
                'key': base64.b64encode(self.key).decode()
            }
            
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            raise
    
    def decrypt_data(self, encrypted_data, key=None):
        """Decrypt data and verify integrity"""
        try:
            # Use provided key or default
            cipher = self.cipher if key is None else Fernet(base64.b64decode(key))
            
            # Decode and decrypt
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted_data = cipher.decrypt(encrypted_bytes)
            
            # Try to parse as JSON, fall back to string
            try:
                return json.loads(decrypted_data.decode())
            except json.JSONDecodeError:
                return decrypted_data.decode()
                
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            raise
    
    def verify_hash(self, data, expected_hash):
        """Verify data integrity using hash"""
        try:
            if isinstance(data, dict):
                data_str = json.dumps(data, sort_keys=True)
            else:
                data_str = str(data)
                
            computed_hash = hashlib.sha256(data_str.encode()).hexdigest()
            return computed_hash == expected_hash
            
        except Exception as e:
            logger.error(f"Error verifying hash: {e}")
            return False

# Initialize privacy layer
privacy_layer = SimplePrivacyLayer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'privacy-layer',
        'api_ready': True
    })

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    """Encrypt data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract data to encrypt
        plaintext_data = data.get('data')
        if plaintext_data is None:
            return jsonify({'error': 'No data field provided'}), 400
        
        # Encrypt the data
        result = privacy_layer.encrypt_data(plaintext_data)
        
        return jsonify({
            'success': True,
            'encrypted_data': result['encrypted_data'],
            'hash': result['hash'],
            'key': result['key']
        })
        
    except Exception as e:
        logger.error(f"Error in encryption: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    """Decrypt data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract encrypted data and key
        encrypted_data = data.get('encrypted_data')
        key = data.get('key')
        
        if not encrypted_data:
            return jsonify({'error': 'No encrypted_data provided'}), 400
        
        # Decrypt the data
        decrypted_data = privacy_layer.decrypt_data(encrypted_data, key)
        
        return jsonify({
            'success': True,
            'decrypted_data': decrypted_data
        })
        
    except Exception as e:
        logger.error(f"Error in decryption: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/verify', methods=['POST'])
def verify_integrity():
    """Verify data integrity using hash"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract data and expected hash
        check_data = data.get('data')
        expected_hash = data.get('hash')
        
        if check_data is None or expected_hash is None:
            return jsonify({'error': 'Both data and hash must be provided'}), 400
        
        # Verify integrity
        is_valid = privacy_layer.verify_hash(check_data, expected_hash)
        
        return jsonify({
            'success': True,
            'is_valid': is_valid
        })
        
    except Exception as e:
        logger.error(f"Error in verification: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get service status"""
    return jsonify({
        'status': 'running',
        'service': 'privacy-layer',
        'endpoints': ['/health', '/encrypt', '/decrypt', '/verify', '/status'],
        'version': 'simple-v1.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Privacy Layer API server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
