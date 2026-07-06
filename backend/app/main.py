"""Main application entry point for QuensultingAI Dental Voice Agent backend."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.health import router as health_router
from app.api.v1.router import api_router as v1_router
from app.core.config import settings

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan event handler for FastAPI startup and shutdown actions."""
    logger.info("Starting up Dental Receptionist Voice Agent backend...")
    logger.info(
        "Application running in Environment: %s", settings.app_env
    )
    yield
    logger.info("Shutting down Dental Receptionist Voice Agent backend...")


# Initialize FastAPI app
app = FastAPI(
    title="QuensultingAI Dental Receptionist Voice Agent",
    description=(
        "Backend service for dental receptionist voice agent, handling FAQ "
        "answering, booking logs, and confirmations."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS Middleware (crucial for future integrations/dashboard tools)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Root-Level Endpoints
app.include_router(health_router)

# Register Version 1 Endpoints (ready for future phases)
app.include_router(v1_router, prefix="/api/v1")
