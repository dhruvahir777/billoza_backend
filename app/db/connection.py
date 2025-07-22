from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
from app.core.config import settings
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None
    users = None
    menu_items = None
    orders = None

db = Database()

async def connect_to_mongo():
    """
    Connect to MongoDB with retry logic.
    Attempts to connect multiple times before giving up.
    """
    logger.info("Connecting to MongoDB...")
    
    # Connection retry settings
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            # Set a short server selection timeout for faster detection of connection issues
            db.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
                tlsAllowInvalidCertificates=True,  # Only use in development
                retryWrites=True
            )
            
            # Initialize database and collections
            db.db = db.client[settings.MONGODB_DB_NAME]
            db.users = db.db.users
            db.menu_items = db.db.menu_items
            db.orders = db.db.orders
            
            # Ping the server to verify connection
            await db.client.admin.command('ping')
            logger.info(f"Connected to MongoDB successfully on attempt {attempt}")
            return
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            if attempt == max_retries:
                logger.error(f"Failed to connect to MongoDB after {max_retries} attempts: {str(e)}")
                # We don't raise the exception here to allow the app to start
                # The DatabaseConnectionMiddleware will handle requests that need DB access
                return
            else:
                logger.warning(f"MongoDB connection attempt {attempt} failed: {str(e)}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)

async def close_mongo_connection():
    """Close MongoDB connection."""
    if db.client:
        logger.info("Closing MongoDB connection...")
        db.client.close()
        logger.info("MongoDB connection closed")
