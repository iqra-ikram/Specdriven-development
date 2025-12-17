# Backend Service

This directory contains the FastAPI backend service for the RAG chatbot.

## Setup

1.  **Install Dependencies**:
    ```bash
    poetry install
    ```
2.  **Environment Variables**:
    Create a `.env` file in the `backend/` directory with the following variables:
    *   `GOOGLE_API_KEY`: Your Google Gemini API key. This is required for generating embeddings and chat completions.
    *   `QDRANT_HOST`: The host for your Qdrant vector database (e.g., `http://localhost:6333`).
    *   `QDRANT_API_KEY`: The API key for your Qdrant instance.
    *   `DATABASE_URL`: Your PostgreSQL database URL (e.g., `postgresql://user:password@host:port/database`).
    *   `BACKEND_INGEST_URL`: (Optional) The URL for the content ingestion endpoint if different from default (e.g., `http://localhost:8000/api/ingest_content`).
    *   `INGESTION_API_KEY`: (Optional) An API key for authenticating content ingestion requests.

## Running the Service

```bash
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Initializing Qdrant Collection

Before ingesting data, ensure your Qdrant collection is initialized:

```bash
poetry run python init_qdrant.py
```
