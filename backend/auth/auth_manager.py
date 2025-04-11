import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify

class AuthManager:
    """
    Manages authentication and authorization for the CryptaNet system.
    
    This class provides methods for user authentication, JWT token generation,
    and role-based access control.
    """
    
    def __init__(self, secret_key, token_expiration=24):
        """
        Initialize the authentication manager.
        
        Args:
            secret_key (str): The secret key used for JWT token generation.
            token_expiration (int): Token expiration time in hours. Defaults to 24.
        """
        self.secret_key = secret_key
        self.token_expiration = token_expiration
        self.users_db = {}  # In-memory user database (replace with a real database in production)
    
    def add_user(self, username, password, role='user'):
        """
        Add a new user to the system.
        
        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.
            role (str): The role of the new user. Defaults to 'user'.
            
        Returns:
            bool: True if the user was added successfully, False otherwise.
        """
        if username in self.users_db:
            return False
        
        self.users_db[username] = {
            'password': generate_password_hash(password),
            'role': role
        }
        
        return True
    
    def authenticate(self, username, password):
        """
        Authenticate a user and generate a JWT token.
        
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            
        Returns:
            dict: A dictionary containing the JWT token and user information if authentication is successful,
                 None otherwise.
        """
        if username not in self.users_db:
            return None
        
        if check_password_hash(self.users_db[username]['password'], password):
            token = jwt.encode({
                'username': username,
                'role': self.users_db[username]['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self.token_expiration)
            }, self.secret_key, algorithm='HS256')
            
            return {
                'token': token,
                'username': username,
                'role': self.users_db[username]['role']
            }
        
        return None
    
    def token_required(self, f):
        """
        Decorator for routes that require a valid JWT token.
        
        Args:
            f: The function to decorate.
            
        Returns:
            function: The decorated function.
        """
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
                data = jwt.decode(token, self.secret_key, algorithms=['HS256'])
                current_user = data['username']
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
            
            return f(current_user, *args, **kwargs)
        
        return decorated
    
    def admin_required(self, f):
        """
        Decorator for routes that require admin privileges.
        
        Args:
            f: The function to decorate.
            
        Returns:
            function: The decorated function.
        """
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if self.users_db.get(current_user, {}).get('role') != 'admin':
                return jsonify({'message': 'Admin privileges required!'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    
    def get_user_role(self, username):
        """
        Get the role of a user.
        
        Args:
            username (str): The username of the user.
            
        Returns:
            str: The role of the user, or None if the user does not exist.
        """
        if username not in self.users_db:
            return None
        
        return self.users_db[username]['role']
    
    def update_user_role(self, username, new_role):
        """
        Update the role of a user.
        
        Args:
            username (str): The username of the user.
            new_role (str): The new role of the user.
            
        Returns:
            bool: True if the role was updated successfully, False otherwise.
        """
        if username not in self.users_db:
            return False
        
        self.users_db[username]['role'] = new_role
        return True
    
    def change_password(self, username, old_password, new_password):
        """
        Change the password of a user.
        
        Args:
            username (str): The username of the user.
            old_password (str): The old password of the user.
            new_password (str): The new password of the user.
            
        Returns:
            bool: True if the password was changed successfully, False otherwise.
        """
        if username not in self.users_db:
            return False
        
        if not check_password_hash(self.users_db[username]['password'], old_password):
            return False
        
        self.users_db[username]['password'] = generate_password_hash(new_password)
        return True