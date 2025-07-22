import os
import json
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Any, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Restaurant Billing API"
    DEBUG: bool = True
    
    # CORS settings - will load from .env file
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # JWT settings
    JWT_SECRET: str = "your_jwt_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # MongoDB settings
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = "restaurant_db"
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB default
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert ALLOWED_ORIGINS string to list"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            # Handle comma-separated string
            if ',' in self.ALLOWED_ORIGINS:
                return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
            # Handle single URL
            elif self.ALLOWED_ORIGINS.strip():
                return [self.ALLOWED_ORIGINS.strip()]
            # Handle empty string
            else:
                return ["http://localhost:3000"]
        else:
            return ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
# Create instance of settings
settings = Settings()
