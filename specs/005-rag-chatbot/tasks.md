# Tasks: Integrated RAG Chatbot

**Input**: Design documents from `specs/005-rag-chatbot/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

## Format: `[ID] [P?] [Story?] Description with file path`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create `backend/` directory structure: `backend/src/api`, `backend/src/services`, `backend/src/models`, `backend/src/core`, `backend/tests`, `backend/Dockerfile`
- [ ] T002 Create `scripts/content_ingestion/` directory structure.
- [ ] T003 Initialize Python project in `backend/` with Poetry and add core dependencies (FastAPI, Uvicorn, Pydantic, httpx, python-dotenv, qdrant-client, psycopg2-binary, openai).
- [ ] T004 Initialize Python project in `scripts/content_ingestion/` with Poetry and add dependencies (requests, beautifulsoup4, markdown-it, tiktoken, openai, qdrant-client, psycopg2-binary).
- [ ] T005 [P] Create Docusaurus frontend directories for chatbot components: `docusaurus-root/src/components/ChatbotWidget`, `docusaurus-root/src/theme`, `docusaurus-root/src/css`.
- [ ] T006 [P] Configure basic Docusaurus styling for chatbot in `docusaurus-root/src/css/custom.css`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Setup

- [ ] T007 Create `.env` file for backend environment variables (OPENAI_API_KEY, NEON_POSTGRES_URL, QDRANT_HOST, QDRANT_API_KEY, FASTAPI_SECRET_KEY) in `backend/.env`.
- [ ] T008 [P] Implement `backend/src/services/neon_db.py` for Neon Serverless Postgres connection and ORM setup (`ContentChunk` entity definition).
- [ ] T009 [P] Implement `backend/src/services/qdrant_client.py` for Qdrant Cloud client initialization and collection management.
- [ ] T010 [P] Implement `backend/src/services/openai_service.py` for OpenAI API (embeddings and chat completions) interactions.
- [ ] T011 [P] Implement `backend/src/models/chat_models.py` with Pydantic models for `ContentChunk`, `ChatMessage`, `ChatRequest`, `ChatResponse`, `IngestRequest`, `IngestResponse` based on `data-model.md` and `contracts/`.
- [ ] T012 Implement `backend/src/api/main.py` (or modify existing) to initialize FastAPI app, include CORS middleware based on `research.md` decision.
- [ ] T013 Create `/api/ingest_content` endpoint in `backend/src/api/chat.py` (or `ingestion.py`) for content ingestion, including API key protection as per `contracts/ingest_api.json` and `research.md`.

### Content Ingestion Script Setup

- [ ] T014 Create `.env` file for content ingestion script environment variables (e.g., BACKEND_INGEST_URL, INGESTION_API_KEY) in `scripts/content_ingestion/.env`.
- [ ] T015 Implement `scripts/content_ingestion/ingest_docusaurus_content.py` to parse Docusaurus Markdown files, chunk content (using semantic chunking decision from `research.md`), and send to `backend/api/ingest_content` endpoint.

### Frontend Setup

- [ ] T016 Configure Docusaurus frontend to consume backend API via environment variables (e.g., `process.env.FASTAPI_BASE_URL`) in `docusaurus.config.ts` or a suitable frontend config.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Question about Book Content (Priority: P1) 🎯 MVP

**Goal**: As a reader, I want to ask the chatbot a question about the book's content and receive a relevant answer.

**Independent Test**: A user can type a question about a known fact in the book (e.g., "What is ROS 2?") and receive a correct answer based on the documented information. This delivers direct information retrieval.

### Tests for User Story 1

- [ ] T017 [P] [US1] Contract test for `POST /api/chat` in `backend/tests/contract/test_chat_api.py` ensuring request/response schema adherence.
- [ ] T018 [P] [US1] Integration test for RAG pipeline: Querying a known fact and asserting retrieval of relevant chunks from Qdrant and response from OpenAI in `backend/tests/integration/test_rag_pipeline.py`.
- [ ] T019 [P] [US1] Frontend E2E test: Open chatbot widget, type query, assert response appears with references in `docusaurus-root/tests/e2e/test_chatbot_basic.spec.ts`.

### Implementation for User Story 1

- [ ] T020 [P] [US1] Implement core RAG orchestration logic in `backend/src/core/rag_pipeline.py`, integrating `qdrant_client.py` and `openai_service.py`.
- [ ] T021 [US1] Implement `POST /api/chat` endpoint in `backend/src/api/chat.py` to handle user queries, call RAG pipeline, and return responses as per `contracts/chat_api.json`.
- [ ] T022 [P] [US1] Create React `ChatbotWidget` component in `docusaurus-root/src/components/ChatbotWidget/index.tsx` for the basic chat interface (input, display messages, send button).
- [ ] T023 [P] [US1] Implement `ChatbotContext.tsx` in `docusaurus-root/src/theme` for managing chatbot state (messages, loading, error).
- [ ] T024 [US1] Integrate `ChatbotWidget` globally into the Docusaurus layout (e.g., via theme swizzling `docusaurus-root/src/theme/Layout.js` or `Navbar.js`) as a floating button/widget.
- [ ] T025 [US1] Ensure clickable links from chatbot responses lead to relevant book sections in `docusaurus-root/src/components/ChatbotWidget/index.tsx`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Contextual Question from Selected Text (Priority: P1)

**Goal**: As a reader, I want to select a portion of text in the book and ask the chatbot a question specifically about that selected text.

**Independent Test**: A user can highlight a sentence (e.g., "ROS 2 uses a DDS-based communication middleware."), trigger the chatbot's contextual query feature, and then ask "What does DDS mean?", receiving an answer specific to the highlighted text. This delivers targeted clarification.

### Tests for User Story 2

- [ ] T026 [P] [US2] Integration test for contextual RAG: Highlight text, send query with context, assert answer relevance in `backend/tests/integration/test_contextual_rag.py`.
- [ ] T027 [P] [US2] Frontend E2E test: Select text, activate contextual query, type question, assert contextual response in `docusaurus-root/tests/e2e/test_chatbot_contextual.spec.ts`.

### Implementation for User Story 2

- [ ] T028 [P] [US2] Implement frontend logic in `docusaurus-root/src/theme/DocItem/Content/index.js` (or similar swizzled component) to detect text selection and expose it to the `ChatbotContext`.
- [ ] T029 [US2] Update `ChatbotWidget` in `docusaurus-root/src/components/ChatbotWidget/index.tsx` to include UI elements for activating/displaying selected context.
- [ ] T030 [US2] Modify `POST /api/chat` endpoint in `backend/src/api/chat.py` and `rag_pipeline.py` to effectively incorporate `context_selection` into the RAG query and prompt engineering for OpenAI.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T031 [P] Implement comprehensive error handling and logging for backend services (FastAPI, Qdrant, Neon, OpenAI).
- [ ] T032 [P] Refine frontend UI/UX for the `ChatbotWidget` (loading states, error messages, smooth transitions).
- [ ] T033 Code cleanup and refactoring across backend and frontend, ensuring adherence to project's coding standards.
- [ ] T034 Performance optimization for RAG queries (e.g., caching strategies, async processing).
- [ ] T035 Security hardening (e.g., input sanitization, rate limiting on `/chat` endpoint).
- [ ] T036 Update `quickstart.md` with any refined setup instructions or common troubleshooting.
- [ ] T037 Conduct end-to-end testing of the entire chatbot functionality in both light and dark Docusaurus themes.
- [ ] T038 Update project `README.md` to reflect new chatbot feature.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately.
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion.
    *   User stories can then proceed in parallel (if staffed)
    *   Or sequentially in priority order (P1 → P2 → P3).
-   **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
-   **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on User Story 1's `/api/chat` endpoint and basic chatbot UI.

### Within Each User Story

-   Tests MUST be written and FAIL before implementation.
-   Models before services.
-   Services before endpoints.
-   Core implementation before integration.
-   Story complete before moving to next priority.

### Parallel Opportunities

-   All tasks marked [P] can run in parallel (different files, no blocking dependencies).
-   Backend and Frontend foundational tasks can be initiated in parallel.
-   Once foundational tasks are complete, individual user story tasks (especially frontend and backend components) can be worked on in parallel by different team members.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently.
5.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!).
3.  Add User Story 2 → Test independently → Deploy/Demo.
4.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Backend components).
    *   Developer B: User Story 1 (Frontend components).
    *   Developer C: User Story 2 (Backend context handling).
    *   Developer D: User Story 2 (Frontend text selection).
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies.
-   [Story] label maps task to specific user story for traceability.
-   Each user story should be independently completable and testable.
-   Verify tests fail before implementing.
-   Commit after each task or logical group.
-   Stop at any checkpoint to validate story independently.
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.