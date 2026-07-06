# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-07-06

### Added
- **Project Structure**: Created baseline workspace layout (`backend/`, `docs/`, `retell/`, `assets/`, `tests/`).
- **Endpoints**: Implemented root endpoints `GET /` and `GET /health` inside FastAPI backend.
- **Configuration Setup**: Configured environment management template `.env.example` and Pydantic configuration loader structure.
- **Tool Configuration**: Created `pyproject.toml` for Python project configurations.
- **Git Settings**: Configured `.gitignore` to prevent tracking environments, logs, and credentials.
- **Project Documentation**:
  - `docs/PROJECT_CONTEXT.md` (Background, Coding Standards, Scope, Scope Exclusions).
  - `docs/ROADMAP.md` (Detailed 25-phase execution plan).
  - `docs/ARCHITECTURE.md` (Caller-to-SMTP sequential flow and Mermaid diagrams).
  - `README.md` (Main repository readme).
  - `backend/README.md` (Backend project instructions).
  - `LICENSE` (MIT License).
