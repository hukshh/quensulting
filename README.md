# QuensultingAI Dental Receptionist Voice Agent

This repository contains the AI Receptionist Voice Agent developed for a dental clinic as part of the QuensultingAI internship assignment. The agent handles voice communications, schedules appointments, answers questions, logs data into Google Sheets, and confirms bookings via automated emails.

---

## Project Overview
Our Dental Receptionist Voice Agent is designed to act as a production-grade automated assistant. Leveraging **RetellAI Conversation Flow** for structured dialogue and branching, the agent evaluates caller needs, answers frequently asked questions, tracks/books appointments, and seamlessly interacts with a Python/FastAPI backend to log transactions and notify customers.

---

## Assignment Objective
The goal is to design a clean, modular, and production-quality service architecture that:
- Captures caller dialog flows reliably without relying on unstructured, prompt-only LLM instructions.
- Log details of successful appointments into Google Sheets.
- Deliver confirmation emails via secure Gmail SMTP configurations.
- Adheres to clear architectural patterns (SOLID, Separation of Concerns, Service-Layer pattern) for readability and presentation in technical interviews.

---

## Architecture Overview
The system relies on a clean lifecycle process:

```
Caller ◄──(Audio)──► RetellAI Platform ◄──(State/Dialog)──► Conversation Flow ──► FastAPI Backend ──► Google Sheets & Email SMTP
```

For more detailed diagrams and component summaries, see [ARCHITECTURE.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/ARCHITECTURE.md).

---

## Folder Structure

```
quensulting-ai-voice-agent/
├── backend/                  # Python FastAPI codebase
│   ├── app/
│   │   ├── api/              # API endpoints and versioned routers
│   │   │   ├── v1/           # Version 1 application routes
│   │   │   └── endpoints/    # Main root endpoints (health, welcome)
│   │   ├── core/             # Application configs and logging setups
│   │   ├── models/           # Database or persistence models (unused in Phase 1)
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── services/         # Core business logic services
│   │   ├── utils/            # Helper utilities and validators
│   │   └── main.py           # FastAPI entrypoint
│   ├── tests/                # Test suite directory
│   ├── logs/                 # Active execution log directory
│   ├── requirements.txt      # Project library dependencies
│   ├── pyproject.toml        # Tool and project metadata configuration
│   ├── .env.example          # Environment template settings
│   └── README.md             # Backend setup readme
├── docs/                     # System documentation
│   ├── PROJECT_CONTEXT.md    # Scope, coding standards, and background context
│   ├── ROADMAP.md            # The 25-phase execution roadmap
│   └── ARCHITECTURE.md       # Technical flowcharts and explanations
├── retell/                   # RetellAI Conversation Flow configurations/schemas
├── assets/                   # Non-code assets (diagrams, resources)
├── .gitignore                # System and IDE file tracking exclusions
├── LICENSE                   # Project MIT license
├── README.md                 # Root documentation guide
└── CHANGELOG.md              # Project change history
```

---

## Technology Stack
- **Python**: 3.11+
- **Framework**: FastAPI (Asynchronous ASGI server)
- **Validation**: Pydantic v2 & Pydantic Settings
- **Voice Engine**: RetellAI Conversation Flow
- **Integrations**: Google Sheets API & Gmail SMTP Service

---

## Getting Started

### Prerequisites
- Python 3.11 or higher installed.
- Pip (Python Package Installer).

### Run the Backend Locally
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment configuration file:
   ```bash
   cp .env.example .env
   ```
5. Run the web server:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Verify the application runs:
   - Root Welcome Endpoint: `http://localhost:8000/`
   - Health Check: `http://localhost:8000/health`

---

## Future Development Phases
The development checklist tracks 25 key milestones to complete the dental assistant. View the complete roadmap in [ROADMAP.md](file:///Users/ovaiskoite/quensulting/quensulting/docs/ROADMAP.md).