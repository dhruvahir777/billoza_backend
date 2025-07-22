from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt
from app.core.config import settings

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the provided data and expiration time.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time, defaults to settings value
        
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token and return its payload.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        dict: The decoded token payload
    """
    return jwt.decode(
        token, 
        settings.JWT_SECRET, 
        algorithms=[settings.JWT_ALGORITHM]
    )
