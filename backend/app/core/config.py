"""Application settings module using pydantic-settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings class mapping environment variables to attributes.

    Uses Pydantic v2 settings configuration.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.example"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application settings
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")

    # RetellAI configurations
    retell_api_key: str = Field(
        default="your_retell_api_key_here", alias="RETELL_API_KEY"
    )
    retell_webhook_signature_key: str = Field(
        default="your_webhook_signature_key_here",
        alias="RETELL_WEBHOOK_SIGNATURE_KEY",
    )

    # Google Sheets configurations
    google_spreadsheet_id: str = Field(
        default="your_google_spreadsheet_id_here", alias="GOOGLE_SPREADSHEET_ID"
    )
    google_application_credentials: str = Field(
        default="app/core/credentials.json", alias="GOOGLE_APPLICATION_CREDENTIALS"
    )

    # SMTP/Email configurations
    smtp_host: str = Field(default="smtp.gmail.com", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_username: str = Field(
        default="your_gmail_address_here@gmail.com", alias="SMTP_USERNAME"
    )
    smtp_password: str = Field(
        default="your_gmail_app_password_here", alias="SMTP_PASSWORD"
    )
    email_from: str = Field(
        default="your_gmail_address_here@gmail.com", alias="EMAIL_FROM"
    )


# Instantiate settings to be imported across the application
settings = Settings()
