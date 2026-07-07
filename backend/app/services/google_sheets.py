"""Service layer for integrating Google Sheets API using gspread."""

import os
import logging
from typing import Dict, Any
import gspread
from google.oauth2.service_account import Credentials
from app.core.config import settings

logger = logging.getLogger("app.services.google_sheets")


class GoogleSheetsService:
    """Service to handle reading/writing data to Google Sheets."""

    def __init__(self) -> None:
        """Initialize GoogleSheetsService and set up scopes."""
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        self._client = None

    def _get_client(self) -> gspread.Client:
        """Authenticates with Google Service Account and returns a gspread client.

        Returns:
            gspread.Client: Authenticated client instance.
        """
        if self._client is not None:
            return self._client

        creds_path = settings.google_application_credentials
        
        # Resolve path relative to backend root if it is relative
        if not os.path.isabs(creds_path):
            # Cwd is expected to be backend/
            creds_path = os.path.abspath(creds_path)

        if not os.path.exists(creds_path):
            raise FileNotFoundError(
                f"Google Service Account credentials file not found at: {creds_path}"
            )

        logger.info("Authenticating Google Sheets client using credentials at %s", creds_path)
        credentials = Credentials.from_service_account_file(
            creds_path, scopes=self.scopes
        )
        self._client = gspread.authorize(credentials)
        return self._client

    def append_booking(self, booking_data: Dict[str, Any]) -> bool:
        """Appends a new booking record to the Google Sheet.

        Columns:
        1. Booking ID
        2. Timestamp
        3. Caller Name
        4. Phone
        5. Email
        6. Service
        7. Date
        8. Time
        9. Status

        Parameters:
            booking_data (Dict[str, Any]): Dictionary of booking details.

        Returns:
            bool: True if append was successful, False otherwise.
        """
        try:
            client = self._get_client()
            spreadsheet_id = settings.google_spreadsheet_id

            if not spreadsheet_id or spreadsheet_id == "your_google_spreadsheet_id_here":
                raise ValueError("Valid Google Spreadsheet ID has not been configured.")

            # Open spreadsheet by ID and select first worksheet
            sheet = client.open_by_key(spreadsheet_id).get_worksheet(0)

            # Build row matching required column sequence
            row_data = [
                booking_data.get("booking_id", ""),
                booking_data.get("timestamp", ""),
                booking_data.get("caller_name", ""),
                booking_data.get("phone", ""),
                booking_data.get("email", ""),
                booking_data.get("service", ""),
                booking_data.get("date", ""),
                booking_data.get("time", ""),
                booking_data.get("status", "Pending")
            ]

            logger.info("Appending row to sheet ID %s: %s", spreadsheet_id, row_data)
            sheet.append_row(row_data)
            logger.info("Successfully appended booking to Google Sheets")
            return True

        except Exception as e:
            # Requirements: Log the error, do NOT fail the booking, return success/continue.
            logger.error("Failed to append booking to Google Sheets: %s", str(e), exc_info=True)
            return False


# Global instance to be imported/used in services
google_sheets_service = GoogleSheetsService()
