from app.db.connection import db
from app.core.security import get_password_hash
from bson import ObjectId
from app.schemas.user import UserCreate, UserProfileUpdate
from datetime import datetime
from typing import Optional, Dict, Any
from app.utils.image_upload import save_upload_file, delete_file
from fastapi import UploadFile

async def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user's profile by ID.
    
    Args:
        user_id: The user's ID
        
    Returns:
        dict: The user document if found, None otherwise
    """
    if db.users is None:
        return None
    
    try:
        user_id_obj = ObjectId(user_id)
        user = await db.users.find_one({"_id": user_id_obj})
        return user
    except Exception:
        return None

async def create_user(user_data: UserCreate) -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        user_data: The user data
        
    Returns:
        dict: The created user document
    """
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Prepare user document
    now = datetime.utcnow()
    user_doc = {
        "email": user_data.email,
        "password": hashed_password,
        "role": user_data.role,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "restaurant_name": user_data.restaurant_name,
        "phone": user_data.phone,
        "address": user_data.address,
        "profile_image": None,
        "created_at": now,
        "updated_at": now,
        "is_active": True
    }
    
    # Insert user
    result = await db.users.insert_one(user_doc)
    
    # Get the inserted user
    user = await db.users.find_one({"_id": result.inserted_id})
    return user

async def update_user_profile(user_id: str, profile_data: UserProfileUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a user's profile.
    
    Args:
        user_id: The user's ID
        profile_data: The profile data to update
        
    Returns:
        dict: The updated user document if found, None otherwise
    """
    if db.users is None:
        return None
    
    try:
        user_id_obj = ObjectId(user_id)
        
        # Prepare update document
        update_data = {}
        for field, value in profile_data.dict(exclude_unset=True).items():
            if value is not None:
                update_data[field] = value
        
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        # Update user
        await db.users.update_one(
            {"_id": user_id_obj},
            {"$set": update_data}
        )
        
        # Get the updated user
        updated_user = await db.users.find_one({"_id": user_id_obj})
        return updated_user
    except Exception:
        return None

async def update_profile_image(user_id: str, file: UploadFile) -> Optional[Dict[str, Any]]:
    """
    Update a user's profile image.
    
    Args:
        user_id: The user's ID
        file: The uploaded file
        
    Returns:
        dict: The updated user document if found, None otherwise
    """
    if db.users is None:
        return None
    
    try:
        user_id_obj = ObjectId(user_id)
        
        # Get the current user
        user = await db.users.find_one({"_id": user_id_obj})
        if not user:
            return None
        
        # Delete old image if exists
        if user.get("profile_image"):
            delete_file(user["profile_image"])
        
        # Save new image
        file_path = await save_upload_file(file, "profile")
        
        # Update user profile with new image
        await db.users.update_one(
            {"_id": user_id_obj},
            {
                "$set": {
                    "profile_image": file_path,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Get the updated user
        updated_user = await db.users.find_one({"_id": user_id_obj})
        return updated_user
    except Exception:
        return None
