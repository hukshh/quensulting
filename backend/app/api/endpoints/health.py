"""Root level health and index endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Root"])
async def index() -> dict[str, str]:
    """Root endpoint welcoming users or API clients."""
    return {"message": "Welcome to the QuensultingAI Dental Receptionist Voice Agent API"}


@router.get("/health", tags=["Root"])
async def health_check() -> dict[str, str]:
    """Health check endpoint to monitor API status."""
    return {"status": "healthy"}
