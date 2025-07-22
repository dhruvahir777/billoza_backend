from fastapi import FastAPI
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create FastAPI app
app = FastAPI(
    title="Restaurant Billing API Test",
    description="Test configuration",
    version="1.0.0",
)

@app.get("/")
def root():
    """Root endpoint to test if app is running"""
    return {
        "message": "Hello World",
        "allowed_origins": settings.allowed_origins_list
    }
