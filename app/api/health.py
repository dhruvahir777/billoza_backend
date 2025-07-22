from fastapi import APIRouter

# Health check endpoint
router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    Does not check database connection.
    """
    return {"status": "ok"}
