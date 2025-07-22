from passlib.context import CryptContext
from typing import Optional, Dict, Any
from app.db.connection import db
from datetime import datetime

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The password in plain text
        hashed_password: The hashed password to compare against
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new user in the database.
    
    Args:
        user_data: Dictionary containing user information
        
    Returns:
        dict: The created user document
        
    Raises:
        Exception: If user creation fails
    """
    if db.users is None:
        raise Exception("Database connection not available")
    
    # Add timestamps
    current_time = datetime.utcnow()
    user_data["created_at"] = current_time
    user_data["updated_at"] = current_time
    
    # Insert user into database
    result = await db.users.insert_one(user_data)
    
    # Get the created user
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return created_user

async def get_user_by_email(email: str) -> Optional[dict]:
    """
    Get a user by email.
    
    Args:
        email: The email of the user to find
        
    Returns:
        dict: The user document if found, None otherwise
    """
    if db.users is None:
        return None
        
    user = await db.users.find_one({"email": email})
    return user
