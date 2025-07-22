from fastapi import APIRouter, HTTPException, status
from app.services.auth_service import authenticate_user, create_access_token, register_user
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

# Simple schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    restaurant_name: str
    phone: str
    address: str
    profile_image: str = None

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=AuthResponse, status_code=201)
async def register_new_user(user_data: RegisterRequest):
    """
    Register new user with email, password, full_name, restaurant_name, phone, address
    """
    try:
        # Register new user
        new_user = await register_user(user_data)
        
        # Create access token for the new user
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": new_user["email"], 
                "user_id": str(new_user["_id"]),
                "custom_user_id": new_user.get("user_id", "")
            }, 
            expires_delta=access_token_expires
        )
        
        # Prepare user data for response (exclude password)
        user_response = {
            "id": str(new_user["_id"]),
            "user_id": new_user.get("user_id", ""),
            "email": new_user["email"],
            "full_name": new_user["full_name"],
            "restaurant_name": new_user["restaurant_name"],
            "phone": new_user["phone"],
            "address": new_user["address"],
            "profile_image": new_user.get("profile_image")
        }
        
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_response
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Registration Failed",
                "message": str(e),
                "type": "validation_error"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Registration Failed",
                "message": "Unable to create user account. Please try again.",
                "type": "server_error",
                "details": str(e)
            }
        )

@router.post("/login", response_model=AuthResponse)
async def login_user(login_data: LoginRequest):
    """
    Login user with email and password only
    """
    try:
        user = await authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Authentication Failed",
                    "message": "Invalid email or password. Please check your credentials and try again.",
                    "type": "authentication_error"
                }
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user["email"], 
                "user_id": str(user["_id"]),
                "custom_user_id": user.get("user_id", "")
            }, 
            expires_delta=access_token_expires
        )
        
        # Prepare user data for response (exclude password)
        user_response = {
            "id": str(user["_id"]),
            "user_id": user.get("user_id", ""),
            "email": user["email"],
            "full_name": user["full_name"],
            "restaurant_name": user["restaurant_name"],
            "phone": user["phone"],
            "address": user["address"],
            "profile_image": user.get("profile_image")
        }
        
        return {
            "message": "Login successful",
            "access_token": access_token, 
            "token_type": "bearer",
            "user": user_response
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Login Failed",
                "message": "Unable to process login request. Please try again.",
                "type": "server_error",
                "details": str(e)
            }
        )
