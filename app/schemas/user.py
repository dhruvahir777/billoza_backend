from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.db.models.user import UserRole

class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    full_name: str
    restaurant_name: str
    role: UserRole = UserRole.OWNER
    phone: Optional[str] = None
    address: Optional[str] = None
    
class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    restaurant_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    
class UserProfile(UserBase):
    """Schema for user profile response."""
    id: str = Field(..., alias="_id")
    custom_user_id: str
    profile_image: Optional[str] = None
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
        populate_by_name = True
