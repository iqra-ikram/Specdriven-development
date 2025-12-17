import pytest
import uuid
from unittest.mock import AsyncMock, patch, MagicMock
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # Corrected import
from qdrant_client import models # Added

# Import the services that will be integrated into the RAG pipeline
from src.services.openai_service import get_embedding, get_chat_completion # Added
from src.services.qdrant_client import get_qdrant_client, COLLECTION_NAME, get_or_create_qdrant_collection, upsert_vectors, search_vectors
from src.services.neon_db import Base, ContentChunk, create_db_and_tables, get_engine, get_session_local

load_dotenv()

# --- Fixtures for Mocking ---

@pytest.fixture(scope="module", autouse=True)
def mock_env_vars():
    """Mock environment variables for Qdrant and OpenAI to prevent actual calls during testing setup."""
    with patch.dict(os.environ, {
        "QDRANT_HOST": "http://mock-qdrant:6333",
        "QDRANT_API_KEY": "mock-api-key",
        "OPENAI_API_KEY": "mock-openai-key",
        "NEON_POSTGRES_URL": "postgresql+psycopg2://user:password@host:port/database"
    }):
        yield

@pytest.fixture(scope="function")
def mock_openai_client():
    """Mocks the OpenAI client for isolated testing."""
    with patch('src.services.openai_service.get_openai_client', return_value=MagicMock()) as mock_get_client:
        yield mock_get_client.return_value

@pytest.fixture(scope="function")
def mock_qdrant_client():
    """Mocks the Qdrant client for isolated testing."""
    with patch('src.services.qdrant_client.get_qdrant_client', return_value=MagicMock()) as mock_get_client:
        yield mock_get_client.return_value

@pytest.fixture(scope="function")
def mock_db_session():
    """Mocks the SQLAlchemy session for isolated testing."""
    # Use an in-memory SQLite database for testing the ORM functionality
    # This avoids connecting to a real Neon Postgres instance
    in_memory_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(in_memory_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=in_memory_engine)
    
    # Patch get_engine and get_session_local to return our in-memory setup
    with patch('src.services.neon_db.get_engine', return_value=in_memory_engine), \
         patch('src.services.neon_db.get_session_local', return_value=TestingSessionLocal):
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            Base.metadata.drop_all(in_memory_engine) # Clean up after test


# --- Tests ---

@pytest.mark.asyncio
async def test_get_embedding_integration(mock_openai_client):
    """
    Tests the integration with OpenAI's embedding service.
    Ensures `get_embedding` calls the OpenAI client correctly and returns a vector.
    """
    mock_openai_client.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.1, 0.2, 0.3])]
    )
    
    text = "test text"
    embedding = get_embedding(text)
    
    mock_openai_client.embeddings.create.assert_called_once_with(
        input=[text], model="text-embedding-ada-002"
    )
    assert isinstance(embedding, list)
    assert len(embedding) == 3 # Based on mock return value

@pytest.mark.asyncio
async def test_get_chat_completion_integration(mock_openai_client):
    """
    Tests the integration with OpenAI's chat completion service.
    Ensures `get_chat_completion` calls the OpenAI client correctly and returns a response.
    """
    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Mocked chat response"))]
    )
    
    messages = [{"role": "user", "content": "Hello"}]
    response_content = get_chat_completion(messages)
    
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-4", messages=messages, temperature=0.7
    )
    assert response_content == "Mocked chat response"

@pytest.mark.asyncio
async def test_qdrant_collection_management_integration(mock_qdrant_client):
    """
    Tests Qdrant collection management.
    Ensures `get_or_create_qdrant_collection` attempts to get/create a collection.
    """
    # Simulate collection not existing initially
    mock_qdrant_client.get_collection.side_effect = Exception("Collection not found")
    
    get_or_create_qdrant_collection()
    
    mock_qdrant_client.get_collection.assert_called_once_with(collection_name=COLLECTION_NAME)
    mock_qdrant_client.create_collection.assert_called_once_with(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )

@pytest.mark.asyncio
async def test_qdrant_upsert_and_search_integration(mock_qdrant_client):
    """
    Tests Qdrant upsert and search functionality.
    Ensures `upsert_vectors` and `search_vectors` call the Qdrant client correctly.
    """
    mock_qdrant_client.upsert.return_value = MagicMock(status="ok")
    mock_qdrant_client.search.return_value = [
        MagicMock(id="1", score=0.9, payload={"source_url": "/doc1"}),
        MagicMock(id="2", score=0.8, payload={"source_url": "/doc2"})
    ]

    vectors_to_upsert = [
        {"id": "test-uuid-1", "vector": [0.1]*1536, "payload": {"content_chunk_id": "test-uuid-1", "source_url": "/doc1"}}
    ]
    upsert_vectors(vectors_to_upsert)
    mock_qdrant_client.upsert.assert_called_once()

    query_vector = [0.1]*1536
    results = search_vectors(query_vector)
    mock_qdrant_client.search.assert_called_once_with(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=5,
        score_threshold=0.7 # Updated
    )
    assert len(results) == 2

@pytest.mark.asyncio
async def test_neon_db_content_chunk_crud_integration(mock_db_session):
    """
    Tests basic CRUD operations for ContentChunk with the mocked in-memory database.
    This validates the ORM model's functionality.
    """
    # Create
    new_chunk = ContentChunk(
        id=uuid.uuid4(),
        text_content="This is a test chunk.",
        source_url="/docs/intro",
        section_title="Introduction",
        document_id="intro.md",
        chunk_order=1
    )
    mock_db_session.add(new_chunk)
    mock_db_session.commit()
    mock_db_session.refresh(new_chunk)

    assert new_chunk.id is not None
    assert new_chunk.text_content == "This is a test chunk."

    # Read
    retrieved_chunk = mock_db_session.query(ContentChunk).filter_by(document_id="intro.md").first()
    assert retrieved_chunk.text_content == "This is a test chunk."
    
    # Update
    retrieved_chunk.section_title = "Updated Intro"
    mock_db_session.commit()
    mock_db_session.refresh(retrieved_chunk)
    assert retrieved_chunk.section_title == "Updated Intro"

    # Delete (optional, but good for completeness)
    mock_db_session.delete(retrieved_chunk)
    mock_db_session.commit()
    deleted_chunk = mock_db_session.query(ContentChunk).filter_by(document_id="intro.md").first()
    assert deleted_chunk is None
