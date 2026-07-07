"""Version 1 API router initialization."""

from fastapi import APIRouter

from app.api.v1.endpoints.booking import router as booking_router

# Create version 1 router
api_router = APIRouter()

# Include booking endpoint router under appointments prefix
api_router.include_router(booking_router, prefix="/appointments", tags=["Appointments"])
