import hashlib
import json

class SHA256Hashing:
    """
    Implements SHA-256 hashing for data integrity verification in CryptaNet.
    SHA-256 is a cryptographic hash function that generates a fixed-size 256-bit (32-byte) hash.
    It is designed to be a one-way function, making it practically impossible to derive the original
    data from the hash value.
    """
    
    @staticmethod
    def hash_data(data):
        """
        Generate a SHA-256 hash of the provided data.
        
        Args:
            data (str, bytes, or dict): The data to hash. If a dictionary is provided,
                                        it will be converted to a JSON string first.
        
        Returns:
            str: The hexadecimal representation of the SHA-256 hash.
        """
        if isinstance(data, dict):
            # Convert dictionary to a consistently ordered JSON string
            data = json.dumps(data, sort_keys=True)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def verify_hash(data, hash_value):
        """
        Verify that the provided data matches the expected hash value.
        
        Args:
            data (str, bytes, or dict): The data to verify.
            hash_value (str): The expected hash value to compare against.
        
        Returns:
            bool: True if the hash of the data matches the expected hash value, False otherwise.
        """
        calculated_hash = SHA256Hashing.hash_data(data)
        return calculated_hash == hash_value
    
    @staticmethod
    def hash_file(file_path):
        """
        Generate a SHA-256 hash of the contents of a file.
        
        Args:
            file_path (str): The path to the file to hash.
        
        Returns:
            str: The hexadecimal representation of the SHA-256 hash.
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read and update hash in chunks to efficiently handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()