from app.core.security import verify_password, get_user_by_email, hash_password, create_user
from app.core.jwt import create_access_token
from datetime import timedelta
from typing import Optional, Dict, Any
from app.core.config import settings
import random
import string

async def register_user(user_data) -> Dict[str, Any]:
    """
    Register a new user with email, password, full_name, restaurant_name, phone, address, profile_image
    """
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered. Please use a different email address.")
        
        # Generate custom user ID
        user_id = generate_custom_user_id()
        
        # Hash the password
        hashed_password = hash_password(user_data.password)
        
        # Prepare user data for database
        user_dict = {
            "user_id": user_id,
            "email": user_data.email,
            "password": hashed_password,
            "full_name": user_data.full_name,
            "restaurant_name": user_data.restaurant_name,
            "phone": user_data.phone,
            "address": user_data.address,
            "profile_image": user_data.profile_image,
            "is_active": True
        }
        
        # Create user in database
        created_user = await create_user(user_dict)
        
        return created_user
        
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to register user: {str(e)}")

def generate_custom_user_id() -> str:
    """
    Generate a custom user ID in format BZU + 6 random digits.
    """
    digits = ''.join(random.choices(string.digits, k=6))
    return f"BZU{digits}"

async def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user by email and password.
    """
    try:
        user = await get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user["password"]):
            return None
        
        return user
    except Exception:
        return None
