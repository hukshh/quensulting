# Backend Services - Dental Receptionist Voice Agent

This directory contains the FastAPI-based backend server. It serves as the webhook target for RetellAI calls, validating conversations, logging appointments to Google Sheets, and triggering confirmation emails.

---

## Directory Layout
- `app/`: Main codebase.
  - `api/`: Route handlers and routing aggregates.
  - `core/`: Application settings, configurations, security setups, and logging setups.
  - `models/`: Database or persistent structures/models.
  - `schemas/`: Pydantic input/output payload validation models.
  - `services/`: Business workflow engines (Google Sheets service, SMTP emailing service, etc.).
  - `utils/`: Helper utilities (date helpers, formatting, etc.).
- `logs/`: Application log output directory.
- `tests/`: Automated test suite.

---

## Getting Started

### Local Setup
1. **Prepare Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment variables**:
   Create a local copy of `.env.example`:
   ```bash
   cp .env.example .env
   ```
   *Note: For Phase 1, you can leave the placeholder credentials as they are, since no integrations are executed.*

### Running the server
Start the FastAPI server via Uvicorn:
```bash
uvicorn app.main:app --reload
```
The server will bind to `http://127.0.0.1:8000` by default.

---

## Available Root Endpoints (Phase 1)
- **Welcome Message**: `GET /`
- **Application Health Check**: `GET /health`
