import hashlib
import os
import random
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class ZeroKnowledgeProof:
    """
    Implements a simplified Zero-Knowledge Proof (ZKP) system for selective disclosure in CryptaNet.
    
    This implementation provides a way for a prover to demonstrate knowledge of certain information
    without revealing the actual information itself. It's used for selective disclosure of supply
    chain data while maintaining privacy.
    """
    
    def __init__(self):
        """
        Initialize the ZKP system with new key pairs for the prover and verifier.
        """
        # Generate key pairs for demonstration purposes
        self.prover_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.prover_public_key = self.prover_private_key.public_key()
        
        self.verifier_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.verifier_public_key = self.verifier_private_key.public_key()
    
    def create_commitment(self, secret_data):
        """
        Create a commitment to the secret data that can be used in the ZKP protocol.
        
        Args:
            secret_data (str): The secret data to commit to.
            
        Returns:
            tuple: (commitment, randomness) where commitment is the hash of the data and randomness
                  is the random value used in the commitment.
        """
        if isinstance(secret_data, str):
            secret_data = secret_data.encode('utf-8')
            
        # Generate random value for the commitment
        randomness = os.urandom(16).hex()
        
        # Create commitment as hash(secret_data || randomness)
        commitment = hashlib.sha256(secret_data + randomness.encode('utf-8')).hexdigest()
        
        return commitment, randomness
    
    def generate_challenge(self):
        """
        Generate a random challenge for the ZKP protocol.
        
        Returns:
            int: A random challenge value.
        """
        return random.randint(0, 1)  # Simplified challenge: 0 or 1
    
    def generate_proof(self, secret_data, randomness, challenge):
        """
        Generate a proof based on the secret data, randomness, and challenge.
        
        Args:
            secret_data (str): The secret data.
            randomness (str): The randomness used in the commitment.
            challenge (int): The challenge from the verifier.
            
        Returns:
            dict: The proof containing the necessary information for verification.
        """
        if isinstance(secret_data, str):
            secret_data = secret_data.encode('utf-8')
        
        # Sign different values based on the challenge
        if challenge == 0:
            # Prove knowledge of secret_data without revealing it
            signature = self.prover_private_key.sign(
                secret_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return {
                'signature': signature,
                'challenge': challenge
            }
        else:
            # Prove knowledge of randomness
            signature = self.prover_private_key.sign(
                randomness.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return {
                'signature': signature,
                'challenge': challenge
            }
    
    def verify_proof(self, commitment, proof, secret_data=None, randomness=None):
        """
        Verify a ZKP proof against the commitment.
        
        Args:
            commitment (str): The commitment to verify against.
            proof (dict): The proof to verify.
            secret_data (str, optional): The secret data (only needed for challenge 0).
            randomness (str, optional): The randomness (only needed for challenge 1).
            
        Returns:
            bool: True if the proof is valid, False otherwise.
        """
        challenge = proof['challenge']
        signature = proof['signature']
        
        try:
            if challenge == 0 and secret_data is not None:
                if isinstance(secret_data, str):
                    secret_data = secret_data.encode('utf-8')
                
                # Verify signature on secret_data
                self.prover_public_key.verify(
                    signature,
                    secret_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                
                # Verify commitment matches
                if randomness is not None:
                    calculated_commitment = hashlib.sha256(secret_data + randomness.encode('utf-8')).hexdigest()
                    return calculated_commitment == commitment
                return True
            
            elif challenge == 1 and randomness is not None:
                # Verify signature on randomness
                self.prover_public_key.verify(
                    signature,
                    randomness.encode('utf-8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return True
            
            return False
        
        except Exception:
            return False

    def selective_disclosure(self, full_data, fields_to_disclose):
        """
        Selectively disclose only specific fields from the full data.
        
        Args:
            full_data (dict): The complete data dictionary.
            fields_to_disclose (list): List of field names to disclose.
            
        Returns:
            dict: A dictionary containing only the disclosed fields and ZKP proofs for the undisclosed fields.
        """
        result = {}
        proofs = {}
        
        # Include disclosed fields directly
        for field in fields_to_disclose:
            if field in full_data:
                result[field] = full_data[field]
        
        # Generate proofs for undisclosed fields
        for field in full_data:
            if field not in fields_to_disclose:
                field_value = str(full_data[field])
                commitment, randomness = self.create_commitment(field_value)
                challenge = self.generate_challenge()
                proof = self.generate_proof(field_value, randomness, challenge)
                
                proofs[field] = {
                    'commitment': commitment,
                    'proof': proof
                }
        
        result['_proofs'] = proofs
        return result