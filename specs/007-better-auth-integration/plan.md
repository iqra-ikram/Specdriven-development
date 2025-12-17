# Implementation Plan: Better Auth Integration

**Branch**: `007-better-auth-integration` | **Date**: 2025-12-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/007-better-auth-integration/spec.md`

## Summary

Integrate `better-auth` as a separate Node.js service to handle user authentication (Sign Up, Sign In, Sign Out). This service will share a **Neon Serverless Postgres** database with the existing Python (FastAPI) backend. The Python backend will verify session tokens directly via the database. Docusaurus frontend will interact with the Auth Service for login/registration and the Python Backend for protected data.

## Technical Context

**Language/Version**: Node.js (for Auth Service), Python 3.11 (Existing Backend), TypeScript (Frontend/Auth)
**Primary Dependencies**: 
- Auth Service: `better-auth`, `hono` or `express` (for API), `pg` (Postgres driver)
- Backend: `fastapi`, `sqlalchemy` (or direct DB driver for session checks)
- Frontend: `docusaurus`, React, `better-auth/client`
**Storage**: Neon Serverless Postgres (Shared)
**Testing**: Jest (Auth Service), Pytest (Backend verification)
**Target Platform**: Node.js runtime (Auth), Python runtime (Backend)
**Project Type**: Hybrid (Web Frontend + Python Backend + Node Auth Service)
**Constraints**: Must run alongside existing services. `better-auth` requires Node.js.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Unwavering Focus on Physical AI**: (Neutral) Auth enables user-specific AI features.
- **II. Structured, Modular Curriculum**: (Pass) Auth is a foundational module.
- **III. Docusaurus for Frontend**: (Pass) Integration targets Docusaurus.
- **IV. Prescribed Tech Stack**: 
    - *Violation Check*: Constitution specifies FastAPI/Neon. `better-auth` introduces Node.js. 
    - *Justification*: Explicit user request for `better-auth` overrides the default stack for this specific feature. Neon is still used.
- **VIII. Global Accessibility**: (Pass) Auth pages should support i18n (future task, but architecture allows it).

*Re-checked after Design Phase: PASSED. Hybrid architecture respects the Neon/FastAPI core while adding the requested capability.*

## Project Structure

### Documentation (this feature)

```text
specs/007-better-auth-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
auth-service/          # NEW: Node.js service for Better Auth
├── package.json
├── src/
│   ├── index.ts      # Server entry point
│   ├── auth.ts       # Better Auth config
│   └── db.ts         # Database connection
└── tsconfig.json

backend/               # EXISTING: Python Backend
├── src/
│   ├── core/
│   │   └── auth_middleware.py # Session verification logic
│   └── ...

docusaurus-root/       # EXISTING: Frontend
├── src/
│   ├── components/
│   │   ├── Auth/     # Login/Signup forms
│   │   └── ...
│   ├── lib/
│   │   └── auth-client.ts # Better Auth client setup
│   └── ...
```

**Structure Decision**: A new `auth-service` directory at the root to house the Node.js application, keeping it distinct from the Python `backend` but sharing the database.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Node.js Service | User explicitly requested `better-auth` (Node lib) | Python-native auth rejected by user preference for `better-auth` features. |