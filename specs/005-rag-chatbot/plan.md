# Implementation Plan: Integrated RAG Chatbot

**Branch**: `005-rag-chatbot` | **Date**: 2025-12-04 | **Spec**: specs/005-rag-chatbot/spec.md
**Input**: Feature specification from `specs/005-rag-chatbot/spec.md`

## Summary

Integrated Retrieval-Augmented Generation (RAG) chatbot embedded within the Docusaurus book, designed to answer user questions about the book's content, including contextual questions based on selected text.

## Technical Context

**Language/Version**: Python 3.10+ (for FastAPI backend), TypeScript/JavaScript (for Docusaurus frontend).  
**Primary Dependencies**: FastAPI, OpenAI Agents/ChatKit SDKs, Qdrant Client (for Python backend), Neon Serverless Postgres Client (for Python backend).  
**Storage**: Neon Serverless Postgres (structured content metadata), Qdrant Cloud Free Tier (vector embeddings).  
**Testing**: Pytest (FastAPI backend), Playwright/Jest (Docusaurus frontend integration), unit tests for RAG logic.  
**Target Platform**: Web (Docusaurus frontend, FastAPI backend deployed on a serverless platform, e.g., Vercel, Netlify Functions, or AWS Lambda).  
**Performance Goals**: Chatbot response under 5 seconds for new queries, under 1 second for responses leveraging cached RAG results or simple direct answers.  
**Constraints**: Must adhere to the technology stack mandated by Principle IV and VII of the project's Constitution.  
**Scale/Scope**: The chatbot will be integrated into the existing Docusaurus site, serving as an interactive learning assistant for book readers. It will handle concurrent requests typical for a documentation site.

## Constitution Check

**Constitution Version**: 1.1.0

- [x] **III. Docusaurus for Frontend UI**: The chatbot's user interface will be developed as a component integrated within the Docusaurus framework, adhering to existing UI/UX principles.
- [x] **IV. Prescribed Core Technology Stack (AI & Web Infrastructure)**: The plan explicitly leverages OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier, fully aligning with the mandated stack.
- [x] **VII. Integrated AI Learning Support**: The core purpose of this feature is to provide integrated, context-aware AI assistance for learners, directly fulfilling this principle.

## Project Structure

### Documentation (this feature)

```text
specs/005-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── chat_api.json    # OpenAPI/JSON Schema for chat endpoint
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure
backend/
├── src/
│   ├── api/
│   │   └── chat.py      # FastAPI endpoints for chat and RAG
│   ├── services/
│   │   └── qdrant_client.py # Qdrant interaction service
│   │   └── openai_service.py # OpenAI Chat/Agent interaction service
│   │   └── neon_db.py # Neon Postgres client and ORM
│   ├── models/
│   │   └── chat_models.py # Pydantic models for request/response
│   └── core/
│       └── rag_pipeline.py # Core RAG orchestration logic
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── Dockerfile # For backend deployment

frontend/ (existing docusaurus-root/)
├── src/
│   ├── components/
│   │   └── ChatbotWidget/ # React component for chatbot UI
│   ├── theme/
│   │   └── ChatbotContext.tsx # React context for chatbot state
│   └── css/
│       └── custom.css # Chatbot widget styling
└── static/ # Potentially for static assets if needed

scripts/
└── content_ingestion/
    └── ingest_docusaurus_content.py # Script to process and embed book content
```

**Structure Decision**: This plan adopts a web application structure with a Python FastAPI backend for RAG logic and AI orchestration, and the existing Docusaurus frontend enhanced with a React chatbot widget. A separate `scripts/` directory will house content ingestion tools.

## Complexity Tracking

No constitution violations detected.

---

## Phase 0: Research & Discovery

**Goal**: Gather necessary information to design the RAG pipeline and Docusaurus integration effectively.

1.  **Research Task: Docusaurus React Component Integration**: Investigate best practices for embedding custom React widgets and passing data/events between Docusaurus's static content and the dynamic React widget. Explore swizzling options if necessary.
2.  **Research Task: Docusaurus Content Chunking for RAG**: Determine optimal strategies for parsing Docusaurus Markdown content, chunking it into manageable pieces, and extracting metadata (e.g., source URLs, section titles) suitable for vector embedding and retrieval.
3.  **Research Task: FastAPI & OpenAI SDK Integration**: Explore patterns for building a FastAPI backend that efficiently calls OpenAI Agents/ChatKit SDKs, manages conversational state (if any beyond single-turn RAG), and handles streaming responses.
4.  **Research Task: Qdrant Cloud & Neon Postgres Setup**: Document the setup process for Qdrant Cloud Free Tier (index creation, API keys) and Neon Serverless Postgres (database setup, connection strings) and their respective Python client SDKs.
5.  **Research Task: Secure Backend-Frontend Communication**: Investigate secure methods for the Docusaurus frontend to communicate with the FastAPI backend, considering CORS, API key management, and environment variables.

**Output**: `specs/005-rag-chatbot/research.md` (consolidated findings, decisions, and rationale for each research task).

## Phase 1: Design & Contracts

**Prerequisites**: `specs/005-rag-chatbot/research.md` complete.

1.  **Data Model Definition**:
    *   **Book Content Entity**: Define the schema for storing processed Docusaurus content chunks in Neon Postgres, including `id`, `text_chunk`, `source_url`, `section_title`, and any other relevant metadata.
    *   **Vector Embedding Entity**: Define the schema for Qdrant, linking `text_chunk_id` to its `embedding` and `metadata`.
    *   **Chat Session/Message Entities**: If session history is to be stored (even ephemeral), define simple structures for `session_id`, `user_query`, `chatbot_response`.
    **Output**: `specs/005-rag-chatbot/data-model.md`

2.  **API Contract Generation**:
    *   **Chat Endpoint**: Design the FastAPI endpoint for handling user queries.
        *   `POST /api/chat`:
            *   Input: `{"query": "string", "context_selection": "string | null", "session_id": "string | null"}`
            *   Output: `{"answer": "string", "references": [{"url": "string", "title": "string"}], "session_id": "string"}`
    *   **Content Ingestion Endpoint (Internal/Admin)**: Design a FastAPI endpoint (or CLI command for initial ingestion) for processing and embedding book content.
        *   `POST /api/ingest_content`: (for automated re-ingestion)
            *   Input: `{"document_id": "string", "content": "string", "source_url": "string"}`
            *   Output: `{"status": "success/error", "message": "string"}`
    **Output**: `specs/005-rag-chatbot/contracts/chat_api.json` (OpenAPI/JSON Schema definition), `specs/005-rag-chatbot/contracts/ingest_api.json`

3.  **Quickstart Guide**:
    *   Outline initial setup steps for local development:
        *   Setting up Neon Postgres and Qdrant Cloud accounts.
        *   Cloning the repository.
        *   Installing dependencies (Poetry for Python, npm/yarn for Node.js).
        *   Running the FastAPI backend and Docusaurus frontend.
        *   Initial content ingestion process.
    **Output**: `specs/005-rag-chatbot/quickstart.md`

4.  **Agent Context Update**:
    *   The agent context has been implicitly updated by the Constitution amendment. No specific script run required for this phase.

## Phase 2: Implementation Tasks (Not part of this command's output)

The output of this `/sp.plan` command focuses on Phase 0 and Phase 1 artifacts. Detailed implementation tasks will be generated in a subsequent step using `/sp.tasks`.