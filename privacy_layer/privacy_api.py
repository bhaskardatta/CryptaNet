import json
import os
from .encryption.fernet_encryption import FernetEncryption
from .hashing.sha256_hashing import SHA256Hashing
from .zkp.zero_knowledge_proof import ZeroKnowledgeProof

class PrivacyAPI:
    """
    Provides a unified API for the privacy layer of CryptaNet.
    
    This class integrates encryption, hashing, and zero-knowledge proof mechanisms
    to ensure data confidentiality, integrity, and selective disclosure.
    """
    
    def __init__(self, encryption_key=None):
        """
        Initialize the privacy API with the necessary components.
        
        Args:
            encryption_key (bytes, optional): The encryption key to use. If None, a new key will be generated.
        """
        self.encryption = FernetEncryption(key=encryption_key)
        self.zkp = ZeroKnowledgeProof()
    
    def encrypt_data(self, data):
        """
        Encrypt data and generate a hash for integrity verification.
        
        Args:
            data (dict or str): The data to encrypt.
            
        Returns:
            dict: A dictionary containing the encrypted data and its hash.
        """
        # Convert dict to JSON string if necessary
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        
        # Generate hash of original data for integrity verification
        data_hash = SHA256Hashing.hash_data(data_str)
        
        # Encrypt the data
        encrypted_data = self.encryption.encrypt(data_str)
        
        return {
            'encrypted_data': encrypted_data,
            'data_hash': data_hash
        }
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt data and verify its integrity using the hash.
        
        Args:
            encrypted_data (dict): A dictionary containing the encrypted data and its hash.
            
        Returns:
            tuple: (data, is_valid) where data is the decrypted data and is_valid indicates
                  whether the integrity check passed.
        """
        # Decrypt the data
        decrypted_data = self.encryption.decrypt(encrypted_data['encrypted_data'])
        
        # Verify the integrity of the decrypted data
        is_valid = SHA256Hashing.verify_hash(decrypted_data, encrypted_data['data_hash'])
        
        # Convert JSON string back to dict if possible
        try:
            decrypted_data = json.loads(decrypted_data)
        except json.JSONDecodeError:
            # If not valid JSON, keep as string/bytes
            if isinstance(decrypted_data, bytes):
                decrypted_data = decrypted_data.decode('utf-8')
        
        return decrypted_data, is_valid
    
    def selective_disclosure(self, data, fields_to_disclose):
        """
        Selectively disclose only specific fields from the data.
        
        Args:
            data (dict): The complete data dictionary.
            fields_to_disclose (list): List of field names to disclose.
            
        Returns:
            dict: A dictionary containing only the disclosed fields and ZKP proofs for the undisclosed fields.
        """
        return self.zkp.selective_disclosure(data, fields_to_disclose)
    
    def verify_selective_disclosure(self, disclosed_data, field, value):
        """
        Verify that an undisclosed field has a specific value without revealing the field.
        
        Args:
            disclosed_data (dict): The selectively disclosed data containing proofs.
            field (str): The field name to verify.
            value (str): The expected value of the field.
            
        Returns:
            bool: True if the field has the expected value, False otherwise.
        """
        if field in disclosed_data:
            # Field was disclosed, direct comparison
            return disclosed_data[field] == value
        
        if '_proofs' not in disclosed_data or field not in disclosed_data['_proofs']:
            return False
        
        proof_data = disclosed_data['_proofs'][field]
        commitment = proof_data['commitment']
        proof = proof_data['proof']
        
        # For challenge 0, we need the secret data (value)
        if proof['challenge'] == 0:
            return self.zkp.verify_proof(commitment, proof, secret_data=value)
        
        # For challenge 1, we can't verify without the randomness
        return False
    
    def get_encryption_key(self):
        """
        Get the current encryption key.
        
        Returns:
            bytes: The encryption key.
        """
        return self.encryption.get_key()
    
    @staticmethod
    def generate_key_from_password(password, salt=None):
        """
        Generate an encryption key from a password and salt.
        
        Args:
            password (str): The password to derive the key from.
            salt (bytes, optional): The salt for key derivation. Defaults to None.
            
        Returns:
            tuple: (key, salt) where key is the derived encryption key and salt is the salt used.
        """
        return FernetEncryption.generate_key_from_password(password, salt)