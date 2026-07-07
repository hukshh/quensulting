"""Service layer module for handling appointment bookings."""

import logging
import uuid
from datetime import datetime
from app.schemas.booking import BookingRequest
from app.services.google_sheets import google_sheets_service

logger = logging.getLogger("app.services.booking")


class BookingService:
    """Service class encapsulating business logic for dental appointments."""

    def __init__(self) -> None:
        """Initialize BookingService."""
        # In a real database/production application, we would initialize database sessions or clients here.
        pass

    async def book_appointment(self, payload: BookingRequest) -> dict:
        """Process the appointment booking request.

        1. Validates details (already handled by Pydantic schema validation at entry)
        2. Generates a unique transaction identifier
        3. Appends the transaction details to Google Sheets
        4. Coordinates with external APIs (SMTP Mailer - to be implemented in future phases)
        5. Logs metrics

        Parameters:
            payload (BookingRequest): Pydantic validated request payload.

        Returns:
            dict: Structured response summary.
        """
        logger.info(
            "Processing booking for patient: %s, service: %s, date: %s, time: %s",
            payload.caller_name,
            payload.service,
            payload.appointment_date,
            payload.appointment_time,
        )

        # Generate a unique transaction booking ID
        # Format: bk_YYYYMMDD_<random_hex>
        date_str = payload.appointment_date.replace("-", "")
        unique_suffix = uuid.uuid4().hex[:6].upper()
        booking_id = f"bk_{date_str}_{unique_suffix}"

        timestamp_str = datetime.utcnow().isoformat()

        # Setup confirmation summary
        summary = {
            "patient": payload.caller_name,
            "phone": payload.phone_number,
            "email": payload.email,
            "service": payload.service,
            "date": payload.appointment_date,
            "time": payload.appointment_time,
            "notes": payload.notes,
            "confidence_score": payload.confidence_score,
            "created_at": timestamp_str,
        }

        # Structure data for Google Sheets mapping:
        # Columns: Booking ID, Timestamp, Caller Name, Phone, Email, Service, Date, Time, Status
        sheet_data = {
            "booking_id": booking_id,
            "timestamp": timestamp_str,
            "caller_name": payload.caller_name,
            "phone": payload.phone_number,
            "email": payload.email,
            "service": payload.service,
            "date": payload.appointment_date,
            "time": payload.appointment_time,
            "status": "Confirmed"
        }

        # Log to Google Sheets
        # Exception handling is encapsulated inside the service: it logs and returns False on error,
        # ensuring the main booking transaction does not fail.
        google_sheets_service.append_booking(sheet_data)

        # FUTURE PHASES:
        # - SMTP Email Confirmation: send_email(summary)

        logger.info("Appointment successfully booked with ID: %s", booking_id)

        return {
            "status": "success",
            "booking_id": booking_id,
            "message": "Appointment booked successfully",
            "summary": summary,
        }


# Global instance of BookingService to be injected/imported
booking_service = BookingService()

