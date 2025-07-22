from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional
from bson import ObjectId

# User roles enum
class UserRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    STAFF = "staff"

# MongoDB document structure for User
user_model = {
    "email": str,
    "password": str,
    "role": str,
    "first_name": str,
    "last_name": str,
    "restaurant_name": str,
    "phone": str,
    "address": str,
    "profile_image": Optional[str],
    "created_at": datetime,
    "updated_at": datetime,
    "is_active": bool
}
