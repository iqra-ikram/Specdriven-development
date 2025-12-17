---
id: 002
title: Update Constitution with Chatbot Requirements
stage: constitution
date: 2025-12-04
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, governance, chatbot, rag, stack]
links: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml:
  - N/A
prompt_text: |
  /sp.constitution i want to implement a chatbot in this project the requirements for the chatbot are mentioned below 2. Integrated RAG Chatbot Development: Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published book. This chatbot, utilizing the OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier, must be able to answer user questions about the book's content, including answering questions based only on text selected by the user. make me the consisituion
response_text: |
  Updated constitution to v1.1.0.
  - Expanded Principle IV (Tech Stack) to include the Chatbot stack (OpenAI, FastAPI, Neon, Qdrant).
  - Added Principle VII (Integrated AI Learning Support) to mandate the RAG chatbot feature.
  - Updated amendment date to 2025-12-04.
---
