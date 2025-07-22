from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api import api_router
from app.core.config import settings
from app.db.connection import connect_to_mongo, close_mongo_connection
from app.middleware.db_middleware import DatabaseConnectionMiddleware
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Restaurant Billing API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # Load from .env
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add database connection middleware
app.add_middleware(DatabaseConnectionMiddleware)

# Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "profile"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "menu"), exist_ok=True)
    
    # Connect to database
    try:
        await connect_to_mongo()
        logging.info("Connected to MongoDB successfully")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
        # The app will still start, but the middleware will handle DB-dependent requests

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connection
    await close_mongo_connection()

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field_name = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": field_name,
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input", "")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Please check the following fields:",
            "details": errors
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later.",
            "details": str(exc) if settings.DEBUG else "Enable debug mode for detailed error"
        }
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Restaurant Billing API",
        "docs": f"{settings.API_V1_STR}/docs"
    }
