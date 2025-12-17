# Data Model: Integrated RAG Chatbot

**Feature**: 005-rag-chatbot

## Overview

This document outlines the key entities and their attributes for the Integrated RAG Chatbot feature. The primary goal is to represent the Docusaurus book content in a structured way suitable for both relational storage (Neon Postgres) and vector indexing (Qdrant Cloud).

## Entities

### 1. `ContentChunk` (Neon Serverless Postgres)

Represents a semantically coherent piece of content extracted from the Docusaurus book, enriched with metadata. This will be the source of truth for text and associated information.

*   **`id`**: (Primary Key, UUID) Unique identifier for the content chunk.
*   **`text_content`**: (Text, NOT NULL) The raw text content of the chunk.
*   **`source_url`**: (Text, NOT NULL) The absolute URL to the Docusaurus page where the chunk originated (e.g., `/docs/intro`).
*   **`section_title`**: (Text, NULLABLE) The title of the closest heading (H1, H2, or H3) preceding the chunk. Useful for contextual referencing.
*   **`document_id`**: (Text, NOT NULL) A unique identifier for the entire Docusaurus document (e.g., the Markdown file path).
*   **`chunk_order`**: (Integer, NOT NULL) The sequential order of this chunk within its `document_id`.
*   **`created_at`**: (Timestamp, DEFAULT NOW()) Timestamp of when the chunk was first ingested.
*   **`updated_at`**: (Timestamp, DEFAULT NOW()) Timestamp of when the chunk was last updated.

### 2. `VectorEmbedding` (Qdrant Cloud)

Represents the vector representation of a `ContentChunk` for efficient similarity search. Stored in Qdrant with a payload linking back to `ContentChunk`.

*   **`id`**: (UUID) Unique identifier for the vector, corresponding to `ContentChunk.id`.
*   **`vector`**: (Vector, NOT NULL) The high-dimensional embedding of `ContentChunk.text_content`.
*   **`payload`**: (JSONB / Key-Value Store) Metadata associated with the vector.
    *   `content_chunk_id`: (UUID, NOT NULL) Foreign key to `ContentChunk.id`.
    *   `source_url`: (Text, NOT NULL) Copy of `ContentChunk.source_url`.
    *   `section_title`: (Text, NULLABLE) Copy of `ContentChunk.section_title`.
    *   `document_id`: (Text, NOT NULL) Copy of `ContentChunk.document_id`.

### 3. `ChatSession` (Ephemeral / Frontend-Managed for MVP)

Represents a user's interaction session with the chatbot. For MVP, this might be managed on the frontend or be short-lived on the backend. Future iterations might persist this.

*   **`session_id`**: (UUID) Unique identifier for the chat session.
*   **`user_id`**: (Text, NULLABLE) Identifier for an authenticated user (if authentication is added later).
*   **`start_time`**: (Timestamp) Time the session started.
*   **`last_activity`**: (Timestamp) Last time a message was sent/received.
*   **`messages`**: (Array of `ChatMessage`) Collection of messages within the session.

### 4. `ChatMessage` (Part of `ChatSession`)

Represents a single message exchange within a chat session.

*   **`message_id`**: (UUID) Unique identifier for the message.
*   **`sender`**: (Enum: 'user', 'chatbot') Who sent the message.
*   **`text`**: (Text, NOT NULL) The content of the message.
*   **`timestamp`**: (Timestamp) When the message was sent.
*   **`context_selection`**: (Text, NULLABLE) If the message was a user query with selected text, store that text.
*   **`source_references`**: (Array of `Reference`) If the chatbot response included sources.

### 5. `Reference` (Part of `ChatMessage`)

Represents a link to the original source content within the book.

*   **`url`**: (Text, NOT NULL) The URL to the Docusaurus page.
*   **`title`**: (Text, NULLABLE) The title of the section or page.

## Relationships

*   One `ContentChunk` has one `VectorEmbedding`.
*   One `ChatSession` contains many `ChatMessage`s.
*   One `ChatMessage` (from chatbot) can have many `Reference`s.
*   One `VectorEmbedding` payload directly links to its `ContentChunk`.

## Data Flow Summary

1.  Docusaurus Markdown content is processed, chunked, and enriched with metadata to create `ContentChunk` records.
2.  `ContentChunk.text_content` is converted into `VectorEmbedding`s using OpenAI's embedding model.
3.  `ContentChunk` records are stored in Neon Postgres.
4.  `VectorEmbedding`s (with `ContentChunk.id` and other metadata in payload) are stored in Qdrant Cloud.
5.  User submits a query (and optional `context_selection`) via the Docusaurus frontend.
6.  FastAPI backend receives the query.
7.  If `context_selection` is present, it's appended/prefixed to the query for enhanced relevance.
8.  The query (and context) is embedded via OpenAI.
9.  Qdrant performs a similarity search using the query embedding to retrieve relevant `VectorEmbedding`s (and their payloads).
10. The `content_chunk_id` from Qdrant's payload is used to retrieve full `ContentChunk.text_content` from Neon Postgres (or just use payload if sufficient).
11. Retrieved `ContentChunk.text_content` serves as context for OpenAI's Chat Completion API (using ChatKit/Agents SDK).
12. OpenAI generates a response.
13. FastAPI parses the response, extracts potential source references, and returns it to the Docusaurus frontend.
14. Frontend displays the response and clickable source links.