#!/usr/bin/env python3
"""
Simple Blockchain Service for CryptaNet
Provides basic blockchain-like functionality for demonstration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import hashlib
import time
from datetime import datetime
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class SimpleBlockchain:
    """Simple blockchain implementation for demonstration"""
    
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0
        }
        genesis_block['hash'] = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)
        logger.info("Genesis block created")
    
    def calculate_hash(self, block):
        """Calculate SHA-256 hash of a block"""
        # Create a copy without the hash field to avoid circular reference
        block_copy = {k: v for k, v in block.items() if k != 'hash'}
        block_string = json.dumps(block_copy, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def get_latest_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Add a transaction to the pending transactions"""
        transaction['id'] = str(uuid.uuid4())
        transaction['timestamp'] = datetime.now().isoformat()
        self.pending_transactions.append(transaction)
        logger.info(f"Transaction added: {transaction['id']}")
        return transaction['id']
    
    def mine_pending_transactions(self):
        """Mine a new block with pending transactions"""
        if not self.pending_transactions:
            return None
        
        new_block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.pending_transactions.copy(),
            'previous_hash': self.get_latest_block()['hash'],
            'nonce': 0
        }
        
        # Simple proof of work (find hash starting with zeros)
        new_block['hash'] = self.calculate_hash(new_block)
        while not new_block['hash'].startswith('00'):
            new_block['nonce'] += 1
            new_block['hash'] = self.calculate_hash(new_block)
        
        self.chain.append(new_block)
        self.pending_transactions = []
        logger.info(f"Block {new_block['index']} mined with hash: {new_block['hash'][:16]}...")
        return new_block
    
    def get_chain_info(self):
        """Get blockchain information"""
        return {
            'chain_length': len(self.chain),
            'pending_transactions': len(self.pending_transactions),
            'latest_block_hash': self.get_latest_block()['hash'],
            'total_transactions': sum(len(block['transactions']) for block in self.chain)
        }
    
    def validate_chain(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block's hash is valid
            if current_block['hash'] != self.calculate_hash(current_block):
                return False
            
            # Check if current block points to previous block
            if current_block['previous_hash'] != previous_block['hash']:
                return False
        
        return True

# Initialize blockchain
blockchain = SimpleBlockchain()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        chain_info = blockchain.get_chain_info()
        is_valid = blockchain.validate_chain()
        
        return jsonify({
            'status': 'healthy',
            'service': 'blockchain',
            'chain_length': chain_info['chain_length'],
            'pending_transactions': chain_info['pending_transactions'],
            'total_transactions': chain_info['total_transactions'],
            'chain_valid': is_valid,
            'latest_block': blockchain.get_latest_block()['hash'][:16] + '...',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit_transaction():
    """Submit a transaction to the blockchain"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Add transaction to pending pool
        transaction_id = blockchain.add_transaction({
            'data': data.get('data'),
            'organization_id': data.get('organization_id'),
            'data_type': data.get('data_type'),
            'encrypted_data': data.get('encrypted_data'),
            'data_hash': data.get('data_hash')
        })
        
        # Mine a new block every 5 transactions for demo purposes
        if len(blockchain.pending_transactions) >= 5:
            new_block = blockchain.mine_pending_transactions()
            if new_block:
                logger.info(f"Auto-mined block {new_block['index']}")
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'status': 'pending',
            'message': 'Transaction submitted to blockchain'
        })
        
    except Exception as e:
        logger.error(f"Submit transaction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['GET'])
def query_blockchain():
    """Query blockchain data"""
    try:
        organization_id = request.args.get('organization_id')
        
        # Get all transactions from all blocks
        all_transactions = []
        for block in blockchain.chain:
            for tx in block['transactions']:
                if not organization_id or tx.get('organization_id') == organization_id:
                    tx['block_index'] = block['index']
                    tx['block_hash'] = block['hash']
                    all_transactions.append(tx)
        
        return jsonify({
            'success': True,
            'transactions': all_transactions,
            'count': len(all_transactions),
            'chain_info': blockchain.get_chain_info()
        })
        
    except Exception as e:
        logger.error(f"Query blockchain error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/mine', methods=['POST'])
def mine_block():
    """Manually mine a block"""
    try:
        new_block = blockchain.mine_pending_transactions()
        if new_block:
            return jsonify({
                'success': True,
                'block': new_block,
                'message': f'Block {new_block["index"]} mined successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No pending transactions to mine'
            })
        
    except Exception as e:
        logger.error(f"Mine block error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/info', methods=['GET'])
def blockchain_info():
    """Get blockchain information"""
    try:
        chain_info = blockchain.get_chain_info()
        is_valid = blockchain.validate_chain()
        
        return jsonify({
            'success': True,
            'chain_length': chain_info['chain_length'],
            'pending_transactions': chain_info['pending_transactions'],
            'total_transactions': chain_info['total_transactions'],
            'latest_block_hash': chain_info['latest_block_hash'],
            'chain_valid': is_valid,
            'blocks': [
                {
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'hash': block['hash'][:16] + '...',
                    'transaction_count': len(block['transactions'])
                } for block in blockchain.chain[-5:]  # Last 5 blocks
            ]
        })
        
    except Exception as e:
        logger.error(f"Blockchain info error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/debug', methods=['GET'])
def debug_chain():
    """Debug endpoint to check chain validation issues"""
    try:
        debug_info = []
        for i in range(len(blockchain.chain)):
            block = blockchain.chain[i]
            calculated_hash = blockchain.calculate_hash(block)
            
            is_hash_valid = block['hash'] == calculated_hash
            
            debug_block = {
                'index': block['index'],
                'stored_hash': block['hash'],
                'calculated_hash': calculated_hash,
                'hash_valid': is_hash_valid,
                'previous_hash': block.get('previous_hash', 'N/A'),
                'transaction_count': len(block.get('transactions', []))
            }
            
            if i > 0:
                prev_block = blockchain.chain[i-1]
                debug_block['previous_block_hash'] = prev_block['hash']
                debug_block['previous_hash_match'] = block['previous_hash'] == prev_block['hash']
            
            debug_info.append(debug_block)
        
        return jsonify({
            'success': True,
            'blocks': debug_info,
            'chain_valid': blockchain.validate_chain()
        })
    except Exception as e:
        logger.error(f"Debug error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API documentation"""
    return jsonify({
        'service': 'CryptaNet Simple Blockchain Service',
        'version': '1.0.0',
        'endpoints': {
            'GET /health': 'Health check',
            'POST /submit': 'Submit transaction',
            'GET /query': 'Query blockchain data',
            'POST /mine': 'Mine pending transactions',
            'GET /info': 'Get blockchain information',
            'GET /debug': 'Debug blockchain issues'
        },
        'chain_info': blockchain.get_chain_info()
    })

if __name__ == '__main__':
    logger.info("Starting Simple Blockchain Service on port 5005...")
    app.run(host='0.0.0.0', port=5005, debug=False)
