# Project Context - QuensultingAI Dental Receptionist Voice Agent

## Purpose
The purpose of this project is to build a production-quality, robust AI Receptionist Voice Agent for a dental clinic. The agent will handle patient calls, answer clinic FAQs, schedule/book dental appointments, handle interruptions or fallbacks, transfer calls to humans when necessary, save appointment details dynamically to Google Sheets, and trigger email confirmations via Gmail SMTP.

The core conversational flow is configured using RetellAI Conversation Flow rather than simple LLM prompts, ensuring structured branching, deterministic dialog states, and high reliability under voice conditions.

---

## Architectural Philosophy
Our design principles focus on a clean, scalable, and interview-ready architecture:
1. **Separation of Concerns (SoC)**: Business logic, API routing, data validation, configurations, and external integrations are strictly separated.
2. **SOLID Principles**: Each module has a single responsibility. We use dependencies injection patterns where applicable, keeping services decoupled and easily testable.
3. **No Logic in Routers**: FastAPI routers act solely as entry points that parse requests, trigger validations, delegate execution to underlying services, and return responses.
4. **Service Layer Pattern**: All core workflows (Google Sheets updating, SMTP emailing, RetellAI webhook processing) reside within the `services/` directory.
5. **Configuration Decoupling**: Configuration is centralized using `pydantic-settings` to load settings from environment variables securely, avoiding hardcoded values.

---

## Coding Standards
We enforce high-quality coding conventions:
- **Type Hints**: Explicit Python type hinting is used everywhere to facilitate static code analysis and auto-completion.
- **Descriptive Naming**: Variables, classes, functions, and endpoints are named expressively. No magic numbers or ambiguous abbreviations are used.
- **Docstrings & Clean Comments**: Every module, class, and function has descriptive docstrings detailing parameters and return values.
- **Modular Code**: Code is written in small, single-purpose functions under ~40 lines.
- **Robust Error Handling**: API endpoints use custom HTTP Exceptions and log failures comprehensively using python's built-in `logging` module.

---

## Technology Choices
- **Python 3.11+**: Provides modern typing features, high performance, and robust library support.
- **FastAPI**: A high-performance, asynchronous web framework for building APIs.
- **Pydantic v2 & Pydantic-Settings**: For validation and configuration parsing, validating settings at startup.
- **RetellAI**: A state-of-the-art conversational voice platform handling real-time voice synthesis and recognition.
- **Google Sheets API**: Lightweight data storage to record bookings, avoiding the need for a database.
- **Gmail SMTP**: Reliable transactional email delivery for confirmation emails.
- **Uvicorn**: Lightweight ASGI web server.

---

## Project Scope
- **FAQ Handling**: Answering standard clinic questions (hours, address, services, pricing).
- **Appointment Booking**: Walking the user through capturing appointment time, service type, and caller details.
- **RetellAI Webhook Integration**: Receiving post-call updates and status triggers.
- **Google Sheets Log**: Dynamically appending appointment data to a configured spreadsheet.
- **SMTP Email Confirmations**: Triggering automated emails after booking.
- **Human Handoff**: Providing mechanisms for the voice agent to transfer the call to a human receptionist.

---

## Out-of-Scope Features
To maintain focus and avoid unnecessary complexity, the following are explicitly out of scope:
- User Authentication (Login, Signup, JWT, OAuth)
- Administrative Dashboards / UI Frontends (React, Next.js, HTML portals)
- Databases (PostgreSQL, MongoDB, Redis)
- Background Workers / Task Queues (Celery, RQ)
- Payment Gateway Integrations
- Containerization (Docker, Kubernetes)
- Mobile Applications
