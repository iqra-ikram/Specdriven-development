# Research & Discovery: Integrated RAG Chatbot

**Feature**: 005-rag-chatbot

## Best Practices for Docusaurus React Widget Integration

### Decision: React Component with Custom Hook and Context

*   **Rationale**: Docusaurus is a React application. Developing the chatbot UI as a standard React component allows full flexibility in UI/UX design, state management, and interaction. Utilizing React Context provides a robust way to manage chatbot state (e.g., chat history, loading status, selected text context) across different parts of the Docusaurus frontend without prop-drilling. A custom hook can encapsulate the logic for interacting with the backend API.
*   **Alternatives Considered**:
    *   **Direct HTML/JS Injection**: Rejected due to poor maintainability, lack of React ecosystem benefits, and potential conflicts with Docusaurus's hydration process.
    *   **Docusaurus Plugin**: Overkill for a single widget; more suited for core Docusaurus functionalities.
*   **Integration Point**: The widget can be rendered globally via a Docusaurus theme swizzle (e.g., modifying `Layout.js` or `Navbar.js` to include the widget) or specifically on doc pages if context dictates. A global floating widget is preferred for accessibility across the site.

## Optimal Strategies for Chunking Docusaurus Markdown Content for RAG

### Decision: Semantic Chunking with Markdown Headers and Sentence Splitter

*   **Rationale**: Simple fixed-size chunking can break semantic meaning. A more effective approach combines:
    1.  **Header-based Segmentation**: Splitting Markdown files primarily by top-level headers (H1, H2, H3) to maintain topic coherence. Each segment gets metadata about its original header path.
    2.  **Sentence-level Splitting**: Further splitting large header segments into individual sentences or smaller paragraphs (e.g., 2-3 sentences) if they exceed a certain token limit (e.g., 250-500 tokens). This ensures precise context retrieval without overwhelming the LLM.
    3.  **Metadata Preservation**: For each chunk, important metadata such as `source_url`, `section_title`, and potentially `last_updated_date` will be extracted and stored alongside the vector embedding.
*   **Alternatives Considered**:
    *   **Fixed-size Chunking**: Rejected due to high risk of losing semantic coherence at chunk boundaries.
    *   **Document-level Embedding**: Rejected as it provides insufficient granularity for precise answers.

## Securely Exposing FastAPI Backend Endpoints to a Docusaurus Frontend

### Decision: CORS Configuration, API Key (for Ingestion), and Environment Variables

*   **Rationale**:
    1.  **CORS (Cross-Origin Resource Sharing)**: The FastAPI backend must be configured to allow requests from the Docusaurus frontend's origin (e.g., `https://your-docusaurus-site.com` or `http://localhost:3000` for development). This is fundamental for web security.
    2.  **API Key for Ingestion**: The content ingestion endpoint should be protected with an API key (or similar token) to prevent unauthorized updates to the knowledge base. This key will be managed securely as an environment variable and used by CI/CD or an admin script.
    3.  **Environment Variables**: All sensitive information (API keys, database credentials, Qdrant API keys, OpenAI API keys) will be managed via environment variables in both the backend and frontend (for build-time configuration).
    4.  **HTTPS**: Deployment must be over HTTPS for all communication.
*   **Alternatives Considered**:
    *   **JWT/OAuth for Chatbot**: Rejected for MVP as per spec (public access). More complex authentication could be added later if user-specific features are introduced.

## Qdrant Vector Embedding Strategies for Docusaurus Content

### Decision: Text-Embedding-Ada-002 with Custom Metadata Indexing

*   **Rationale**:
    1.  **Embedding Model**: OpenAI's `text-embedding-ada-002` offers a good balance of performance and cost-effectiveness for general-purpose text embeddings. It's well-suited for a RAG system on documentation.
    2.  **Qdrant Collection**: A single Qdrant collection will store vector embeddings. Each vector will have associated `payload` containing metadata like `source_url`, `section_title`, `original_text_chunk`.
    3.  **Filtering/Search**: Qdrant's filtering capabilities will be leveraged to allow for context-aware search (e.g., filtering by a specific Docusaurus module or chapter if such metadata is available), enhancing retrieval relevance.
*   **Alternatives Considered**:
    *   **Other Embedding Models**: Considered Sentence Transformers or Cohere, but OpenAI provides seamless integration with ChatKit and generally high quality.

## OpenAI ChatKit/Agents SDK Integration Patterns with FastAPI

### Decision: Direct SDK Calls within FastAPI Service Layer

*   **Rationale**: FastAPI will act as the orchestration layer. A dedicated service (e.g., `openai_service.py`) will encapsulate all interactions with the OpenAI ChatKit/Agents SDKs. This promotes modularity and testability.
    *   The service will handle:
        *   Constructing prompts (including retrieved RAG context).
        *   Making API calls to OpenAI.
        *   Parsing and formatting responses.
        *   Potentially managing token usage.
*   **Alternatives Considered**:
    *   **Frontend Direct Calls to OpenAI**: Rejected due to security concerns (exposing API keys) and CORS issues. FastAPI acts as a secure proxy and orchestration layer.
    *   **Using OpenAI Functions**: Will be considered for more complex agentic behaviors but a simpler RAG flow (chat completion with context) is sufficient for MVP.