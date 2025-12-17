# Quickstart Guide: Integrated RAG Chatbot

**Feature**: 005-rag-chatbot

This guide provides a quick overview of how to get the Integrated RAG Chatbot development environment set up and running locally.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.10+**: For the FastAPI backend.
*   **Node.js LTS & npm/yarn**: For the Docusaurus frontend.
*   **Git**: For version control.
*   **Poetry**: (Recommended Python package manager) `pip install poetry`
*   **Docker / Docker Desktop**: (Optional, for local Qdrant/Postgres if not using cloud services)
*   **Accounts**:
    *   **OpenAI API Key**: Required for embedding and chat models.
    *   **Neon Serverless Postgres**: Account and database connection string.
    *   **Qdrant Cloud Free Tier**: Account, cluster URL, and API key.

## 1. Clone the Repository

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

## 2. Backend Setup (FastAPI, Neon, Qdrant)

Navigate to the `backend/` directory.

```bash
cd backend/
```

### 2.1. Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```ini
OPENAI_API_KEY="your_openai_api_key_here"
NEON_POSTGRES_URL="your_neon_postgres_connection_string_here"
QDRANT_HOST="your_qdrant_cloud_cluster_url_here"
QDRANT_API_KEY="your_qdrant_cloud_api_key_here"
FASTAPI_SECRET_KEY="a_very_secret_key_for_fastapi" # Generate a strong one
```

### 2.2. Install Dependencies

Using Poetry:

```bash
poetry install
```

### 2.3. Run Database Migrations (Neon Postgres)

Once Neon Postgres is configured, apply any initial database schemas. (Details for specific migration tool like `Alembic` will be in `backend/` documentation).

```bash
# Example (replace with actual command if using Alembic, etc.)
poetry run python -m your_app.db.migrate upgrade head
```

### 2.4. Start FastAPI Backend

```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend should now be running at `http://localhost:8000`.

## 3. Frontend Setup (Docusaurus)

Navigate to the `docusaurus-root/` directory.

```bash
cd docusaurus-root/
```

### 3.1. Install Dependencies

```bash
npm install # or yarn install
```

### 3.2. Environment Variables (for Frontend)

Frontend environment variables (e.g., `process.env.FASTAPI_BASE_URL`) will be handled by Docusaurus's build process. Configure these in `docusaurus.config.ts` or a similar configuration if needed. For local development, ensure your Docusaurus build points to `http://localhost:8000` for the backend.

### 3.3. Start Docusaurus Frontend

```bash
npm start # or yarn start
```

The Docusaurus site (with the integrated chatbot widget) should now be running at `http://localhost:3000`.

## 4. Initial Content Ingestion

Before the RAG chatbot can answer questions, it needs to ingest the book's content.

Navigate back to the repository root and then into `scripts/content_ingestion/`.

```bash
cd ../scripts/content_ingestion/
```

### 4.1. Configure Ingestion Script

Create a `.env` file here if needed for ingestion-specific variables (e.g., path to Docusaurus content).

### 4.2. Run Ingestion

```bash
poetry run python ingest_docusaurus_content.py --docusaurus-docs-path ../docusaurus-root/docs --backend-url http://localhost:8000/api/ingest_content --api-key your_ingestion_api_key
```
This script will:
1.  Parse your Docusaurus Markdown files.
2.  Chunk the content appropriately.
3.  Send the chunks to your running FastAPI backend's ingestion endpoint.
4.  The backend will then embed the chunks and store them in Qdrant and Neon Postgres.

## 5. Test the Chatbot

Once both frontend and backend are running, and content is ingested, open your Docusaurus site (`http://localhost:3000`) and interact with the chatbot widget!