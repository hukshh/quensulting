"""API endpoint handlers for version 1 booking transactions."""

import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.booking import BookingRequest, BookingResponse
from app.services.booking import booking_service

logger = logging.getLogger("app.api.v1.endpoints.booking")

router = APIRouter()


@router.post(
    "/book",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Schedule a dental clinic appointment",
)
async def book_appointment(payload: BookingRequest) -> dict:
    """Endpoint for scheduling clinic appointments, called by RetellAI webhooks.

    Validates payload structure and fields before calling the BookingService to
    generate reservation parameters.
    """
    try:
        result = await booking_service.book_appointment(payload)
        return result
    except ValueError as val_err:
        logger.warning("Validation error during booking process: %s", str(val_err))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as err:
        logger.exception("Unexpected error occurred while booking appointment: %s", str(err))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected internal error occurred. Please try again later."
        )
