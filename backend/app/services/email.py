"""Service layer for sending booking confirmation emails via SMTP."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger("app.services.email")


class EmailService:
    """Service to handle composing and dispatching transactional emails."""

    def __init__(self) -> None:
        """Initialize EmailService."""
        pass

    def send_booking_confirmation(self, booking_data: Dict[str, Any]) -> bool:
        """Sends a structured booking confirmation email to the patient.

        Parameters:
            booking_data (Dict[str, Any]): Dictionary of confirmed booking details.

        Returns:
            bool: True if email dispatched successfully, False otherwise.
        """
        recipient_email = booking_data.get("email")
        if not recipient_email or recipient_email == "not_provided@brightsmiles.com":
            logger.info("Skipping email confirmation: No valid recipient email provided.")
            return False

        logger.info("Composing booking confirmation email for recipient: %s", recipient_email)

        # Setup MIME email envelope
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Appointment Confirmed - Bright Smiles Dental Clinic"
        msg["From"] = settings.email_from
        msg["To"] = recipient_email

        # Create plain text and HTML bodies
        patient_name = booking_data.get("patient", "Valued Patient")
        service_name = booking_data.get("service", "Dental Appointment")
        app_date = booking_data.get("date", "")
        app_time = booking_data.get("time", "")
        booking_id = booking_data.get("booking_id", "N/A")

        text_content = (
            f"Dear {patient_name},\n\n"
            f"Your appointment at Bright Smiles Dental Clinic has been successfully confirmed!\n\n"
            f"Appointment Details:\n"
            f"- Service: {service_name}\n"
            f"- Date: {app_date}\n"
            f"- Time: {app_time}\n"
            f"- Reference Booking ID: {booking_id}\n\n"
            f"If you need to reschedule or cancel your appointment, please contact us at least 24 hours in advance.\n\n"
            f"We look forward to seeing you!\n\n"
            f"Best regards,\n"
            f"Bright Smiles Front Desk Team"
        )

        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
                    <h2 style="color: #2b7de9;">Appointment Confirmed!</h2>
                    <p>Dear <strong>{patient_name}</strong>,</p>
                    <p>Your appointment at <strong>Bright Smiles Dental Clinic</strong> has been successfully scheduled and confirmed.</p>
                    
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #333;">Appointment Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold; width: 30%;">Treatment:</td>
                                <td style="padding: 5px 0;">{service_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Date:</td>
                                <td style="padding: 5px 0;">{app_date}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Time:</td>
                                <td style="padding: 5px 0;">{app_time}</td>
                            </tr>
                            <tr>
                                <td style="padding: 5px 0; font-weight: bold;">Booking ID:</td>
                                <td style="padding: 5px 0; font-family: monospace; font-size: 14px;">{booking_id}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p style="font-size: 14px; color: #666;">
                        * If you need to make changes to your booking, please call our clinic front desk at least 24 hours prior to your scheduled slot.
                    </p>
                    <p>We look forward to seeing you!</p>
                    <br>
                    <p style="margin-bottom: 0;">Warm regards,</p>
                    <p style="margin-top: 0; font-weight: bold; color: #2b7de9;">Bright Smiles Front Desk Team</p>
                </div>
            </body>
        </html>
        """

        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        try:
            logger.info(
                "Connecting to SMTP server at %s:%s",
                settings.smtp_host,
                settings.smtp_port,
            )
            # Establish standard SMTP TLS session
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()

            # Skip login if credentials are placeholders/empty
            username = settings.smtp_username
            password = settings.smtp_password
            if (
                username 
                and username != "your_gmail_address_here@gmail.com" 
                and password 
                and password != "your_gmail_app_password_here"
            ):
                logger.info("Logging in to SMTP server as %s", username)
                server.login(username, password)
            else:
                logger.warning("SMTP credentials not configured. Skipping SMTP login.")

            logger.info("Sending confirmation email from %s to %s", msg["From"], msg["To"])
            server.sendmail(settings.email_from, [recipient_email], msg.as_string())
            server.quit()
            logger.info("Successfully sent appointment confirmation email")
            return True

        except Exception as e:
            # Requirements: Log the error, do NOT fail the booking
            logger.error("Failed to send booking confirmation email: %s", str(e), exc_info=True)
            return False


# Global instance of EmailService to be imported/used
email_service = EmailService()
