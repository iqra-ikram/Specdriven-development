id: 011
title: Migrate Chatbot Backend from OpenAI to Gemini API
stage: refactor
date: 2025-12-05
surface: agent
model: gemini-1.5-pro-a006-20240730
feature: rag-chatbot
branch: 006-add-urdu-translation
user: user
command: i will not use the open ai api key i want to use the gemini api key please do this for me
labels: ["refactor", "backend", "chatbot", "api-migration", "gemini"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/services/gemini_service.py
  - backend/pyproject.toml
  - backend/src/core/rag_pipeline.py
  - backend/src/services/openai_service.py (deleted)
  - backend/src/services/qdrant_client.py
  - backend/README.md
tests_yaml: |
  - N/A (Requires running backend and frontend to verify)
prompt_text: |
  i will not use the open ai api key i want to use the gemini api key please do this for me
response_text: |
  The chatbot backend has been migrated from using OpenAI API to Google Gemini API. This involved creating a new `gemini_service.py` for Gemini API calls, updating `pyproject.toml` dependencies, refactoring `rag_pipeline.py` to use the new service, deleting the old `openai_service.py`, adjusting Qdrant's `VECTOR_SIZE` for Gemini embeddings, and updating the `backend/README.md` to reflect the new API key requirement and setup instructions.
