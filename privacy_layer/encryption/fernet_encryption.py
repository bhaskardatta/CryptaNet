import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class FernetEncryption:
    """
    Implements symmetric encryption using Fernet for data confidentiality in CryptaNet.
    Fernet guarantees that a message encrypted using it cannot be manipulated or read
    without the key. Fernet is an implementation of symmetric (also known as "secret key") 
    authenticated cryptography.
    """
    
    def __init__(self, key=None):
        """
        Initialize the encryption module with a key.
        If no key is provided, a new one will be generated.
        
        Args:
            key (bytes, optional): The encryption key. Defaults to None.
        """
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher_suite = Fernet(self.key)
    
    def get_key(self):
        """
        Get the current encryption key.
        
        Returns:
            bytes: The encryption key.
        """
        return self.key
    
    def encrypt(self, data):
        """
        Encrypt the provided data using Fernet symmetric encryption.
        
        Args:
            data (str or bytes): The data to encrypt.
            
        Returns:
            bytes: The encrypted data.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.cipher_suite.encrypt(data)
    
    def decrypt(self, encrypted_data):
        """
        Decrypt the provided encrypted data using Fernet symmetric encryption.
        
        Args:
            encrypted_data (bytes): The encrypted data to decrypt.
            
        Returns:
            bytes: The decrypted data.
        """
        return self.cipher_suite.decrypt(encrypted_data)
    
    @staticmethod
    def generate_key_from_password(password, salt=None):
        """
        Generate a Fernet key from a password and salt using PBKDF2.
        
        Args:
            password (str): The password to derive the key from.
            salt (bytes, optional): The salt for key derivation. Defaults to None.
            
        Returns:
            tuple: (key, salt) where key is the derived Fernet key and salt is the salt used.
        """
        if salt is None:
            salt = os.urandom(16)
        
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key, salt