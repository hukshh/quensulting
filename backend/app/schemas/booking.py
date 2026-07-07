"""Pydantic schemas for appointment booking validation."""

import re
from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, Field, field_validator

# Supported dental services list
SUPPORTED_SERVICES = {
    "Dental Cleaning",
    "Root Canal",
    "Teeth Whitening",
    "Braces Consultation",
    "Tooth Extraction",
    "General Consultation",
}


class BookingRequest(BaseModel):
    """Schema validating the RetellAI incoming booking webhook payload."""

    call_id: Optional[str] = Field(default=None, description="Unique RetellAI call identifier")
    caller_name: str = Field(..., description="First and last name of the patient")
    phone_number: str = Field(..., description="10-digit callback phone number")
    email: str = Field(..., description="Contact email address")
    service: str = Field(..., description="Selected dental treatment type")
    appointment_date: str = Field(..., description="Preferred date (YYYY-MM-DD)")
    appointment_time: str = Field(..., description="Preferred time (HH:MM)")
    notes: Optional[str] = Field(default="", description="Additional patient notes")
    confidence_score: Optional[float] = Field(default=1.0, description="RetellAI speech confidence score")

    @field_validator("caller_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate patient name has at least 2 characters and only contains letters/spaces."""
        cleaned = v.strip()
        if len(cleaned) < 2:
            raise ValueError("Patient name must be at least 2 characters long")
        if not re.match(r"^[a-zA-Z\s]+$", cleaned):
            raise ValueError("Patient name must only contain alphabetical characters and spaces")
        return cleaned

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number contains exactly 10 digits."""
        # Strip common formatting characters
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        cleaned = v.strip()
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, cleaned):
            raise ValueError("Invalid email address format")
        return cleaned

    @field_validator("service")
    @classmethod
    def validate_service(cls, v: str) -> str:
        """Validate dental service matches the supported catalog."""
        cleaned = v.strip()
        if cleaned not in SUPPORTED_SERVICES:
            raise ValueError(
                f"Service '{cleaned}' is not supported. Supported services: {', '.join(SUPPORTED_SERVICES)}"
            )
        return cleaned

    @field_validator("appointment_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Validate date is YYYY-MM-DD, is in the future, and is not a Sunday."""
        try:
            target_date = datetime.strptime(v.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Appointment date must be in YYYY-MM-DD format")

        today = date.today()
        if target_date < today:
            raise ValueError("Appointment date cannot be in the past")

        # Sunday is 6 in weekday() (Monday is 0)
        if target_date.weekday() == 6:
            raise ValueError("Appointments cannot be scheduled on Sundays")

        return v.strip()

    @field_validator("appointment_time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        """Validate time is HH:MM and falls within operating hours (9 AM - 6 PM)."""
        try:
            time_obj = datetime.strptime(v.strip(), "%H:%M").time()
        except ValueError:
            try:
                # Fallback to check if hours/minutes are passed as HH:MM:SS
                time_obj = datetime.strptime(v.strip(), "%H:%M:%S").time()
            except ValueError:
                raise ValueError("Appointment time must be in HH:MM format")

        start_time = time(9, 0)
        end_time = time(18, 0)

        if not (start_time <= time_obj <= end_time):
            raise ValueError("Appointment time must be within clinic hours (9:00 AM – 6:00 PM)")

        return time_obj.strftime("%H:%M")


class BookingResponse(BaseModel):
    """Schema validating the backend API successful response payload."""

    status: str = Field(default="success")
    booking_id: str = Field(..., description="Unique booking transaction ID")
    message: str = Field(default="Appointment booked successfully")
    summary: dict = Field(..., description="Details of the confirmed appointment")
