from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user import UserProfile

class Token(BaseModel):
    """Token schema for authentication response."""
    access_token: str
    token_type: str

class UserRegistration(BaseModel):
    """Schema for user registration request."""
    full_name: str
    email: str
    password: str
    restaurant_name: str
    role: str = "owner"
    phone: Optional[str] = None
    address: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    """Schema for user registration response."""
    message: str
    user: UserProfile
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: Optional[str] = None
    user_id: Optional[str] = None
    exp: Optional[int] = None

class LoginResponse(BaseModel):
    """Schema for login response."""
    access_token: str
    token_type: str
    user: dict
