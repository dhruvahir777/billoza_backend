# API routes package initialization
from fastapi import APIRouter
from app.api.auth.routes import router as auth_router
from app.api.users.menu import router as menu_router
from app.api.users.orders import router as order_router
from app.api.users.reports import router as report_router
from app.api.health import router as health_router
from app.core.config import settings

# Create main API router
api_router = APIRouter()

# Include all API routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(menu_router, prefix="/users", tags=["Menu"])
api_router.include_router(order_router, prefix="/users", tags=["Orders"])
api_router.include_router(report_router, prefix="/users", tags=["Reports"])
api_router.include_router(health_router, tags=["Health"])
