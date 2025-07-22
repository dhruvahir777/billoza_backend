from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from app.db.connection import db

logger = logging.getLogger(__name__)

class DatabaseConnectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check database connection before processing requests.
    This middleware ensures that API endpoints requiring database access
    will return a proper error response if the database is not available.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Skip health check endpoints
        if request.url.path.endswith("/health") or request.url.path == "/":
            return await call_next(request)
        
        # Check if MongoDB connection is established
        if db.client is None or db.db is None:
            logger.error("Database connection not available")
            return Response(
                content='{"detail": "Database connection error. Please try again later."}',
                status_code=503,
                media_type="application/json"
            )
        
        # Continue with the request
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return Response(
                content='{"detail": "An error occurred while processing your request."}',
                status_code=500,
                media_type="application/json"
            )
