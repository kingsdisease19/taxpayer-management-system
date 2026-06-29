from bcrypt import hashpw, gensalt, checkpw
from typing import Optional

class PasswordHasher:
    """Utility for hashing and verifying passwords securely."""
    
    @staticmethod
    def hash(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain-text password
        
        Returns:
            Bcrypt hash (includes salt)
        
        Example:
            hash_value = PasswordHasher.hash("MyPassword123")
            # Returns: $2b$12$a1b2c3d4e5f6g7h8i9j0...
        """
        salt = gensalt()
        return hashpw(password.encode(), salt).decode()
    
    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        """
        Verify a plain-text password against a hash.
        
        Args:
            password: Plain-text password (user input on login)
            hashed: Bcrypt hash (stored in database)
        
        Returns:
            True if password matches hash, False otherwise
        
        Example:
            if PasswordHasher.verify("MyPassword123", stored_hash):
                print("Password correct!")
        """
        return checkpw(password.encode(), hashed.encode())