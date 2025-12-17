import pytest
from fastapi.testclient import TestClient
from src.api.main import app # Import the main FastAPI app
from src.models.chat_models import ChatRequest, ChatResponse, IngestRequest, IngestResponse
import os
from dotenv import load_dotenv
from pytest_httpx import HTTPXMock # Added
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.services.neon_db import get_db, Base, ContentChunk # Import ORM models and get_db
import uuid # For ContentChunk ID
from unittest.mock import MagicMock, patch # Added

load_dotenv()

# Mock environment variables for services initialized at app startup
os.environ["NEON_POSTGRES_URL"] = "postgresql+psycopg2://test:test@localhost:5432/test_db"
os.environ["QDRANT_HOST"] = "http://test-qdrant:6333"
os.environ["QDRANT_API_KEY"] = "test-qdrant-api-key"
os.environ["OPENAI_API_KEY"] = "test-openai-api-key"

# Dummy API Key for testing ingestion endpoint
TEST_INGESTION_API_KEY = "test-api-key"

# --- Mock DB Dependency ---

@pytest.fixture(scope="function")
def client_with_overrides(httpx_mock: HTTPXMock): # Fixture to provide TestClient with mocks
    # Create a mock ContentChunk matching what's expected from Qdrant and the DB
    mock_content_chunk = ContentChunk(
        id=uuid.UUID("00000000-0000-0000-0000-000000000001"), # Must be uuid.UUID object
        text_content="ROS 2 is the Robot Operating System version 2.",
        source_url="/docs/intro",
        section_title="Introduction to ROS 2",
        document_id="intro.md",
        chunk_order=1
    )

    # Mock the DB session and its query method to return our mock_content_chunk
    mock_db_session = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_filter = MagicMock()
    
    mock_filter.first.return_value = mock_content_chunk # Directly set return_value for .first()
    mock_query.filter.return_value = mock_filter
    mock_db_session.query.return_value = mock_query

    # Patch get_engine and get_session_local to prevent real DB connections
    # and provide a mocked db session via get_db dependency
    with patch('src.services.neon_db.get_engine', return_value=MagicMock()), \
         patch('src.services.neon_db.get_session_local', return_value=MagicMock()):
        
        # Temporarily override get_db to provide our mocked session for the test
        def override_get_db_mock():
            yield mock_db_session
        app.dependency_overrides[get_db] = override_get_db_mock
        
        # Setup for TestClient
        test_client = TestClient(app)

        yield test_client
        
        # Teardown
        app.dependency_overrides = {}

@pytest.fixture(scope="module")
def setup_ingestion_api_key():
    """Set up and tear down INGESTION_API_KEY for tests."""
    original_key = os.getenv("INGESTION_API_KEY")
    os.environ["INGESTION_API_KEY"] = TEST_INGESTION_API_KEY
    yield
    if original_key is not None:
        os.environ["INGESTION_API_KEY"] = original_key
    else:
        del os.environ["INGESTION_API_KEY"]

def test_ingest_content_endpoint_schema_adherence(client_with_overrides: TestClient, setup_ingestion_api_key):
    """
    Test the /ingest_content endpoint for schema adherence based on IngestRequest and IngestResponse.
    """
    # Valid request body
    valid_request_payload = {
        "document_id": "test-doc-1",
        "content": "This is a test content chunk.",
        "source_url": "/docs/test-doc",
        "section_title": "Test Section"
    }
    
    headers = {"X-API-Key": TEST_INGESTION_API_KEY}
    response = client_with_overrides.post("/ingest_content", json=valid_request_payload, headers=headers)
    
    assert response.status_code == 200
    
    # Validate response schema
    response_data = response.json()
    IngestResponse(**response_data) # Pydantic will raise ValidationError if schema is not adhered
    assert response_data["status"] == "success"

def test_ingest_content_endpoint_unauthorized(client_with_overrides: TestClient):
    """
    Test that /ingest_content endpoint returns 401 if API Key is missing or invalid.
    """
    valid_request_payload = {
        "document_id": "test-doc-1",
        "content": "This is a test content chunk.",
        "source_url": "/docs/test-doc",
        "section_title": "Test Section"
    }
    
    # Missing API Key
    response = client_with_overrides.post("/ingest_content", json=valid_request_payload)
    assert response.status_code == 401
    
    # Invalid API Key
    headers = {"X-API-Key": "wrong-key"}
    response = client_with_overrides.post("/ingest_content", json=valid_request_payload, headers=headers)
    assert response.status_code == 401

def test_chat_endpoint_schema_adherence(client_with_overrides: TestClient, httpx_mock: HTTPXMock): # Added httpx_mock and using new client
    """
    Test the /chat endpoint for schema adherence based on ChatRequest and ChatResponse.
    """
    # Mock OpenAI embedding API call
    httpx_mock.add_response(
        url="https://api.openai.com/v1/embeddings",
        method="POST",
        json={
            "data": [
                {"embedding": [0.1] * 1536} # Mock embedding vector
            ],
            "model": "text-embedding-ada-002",
            "usage": {"prompt_tokens": 10, "total_tokens": 10}
        },
        status_code=200
    )

    # Mock OpenAI chat completion API call
    httpx_mock.add_response(
        url="https://api.openai.com/v1/chat/completions",
        method="POST",
        json={
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Mocked answer about ROS 2. [ref: /docs/ros2]"
                    }
                }
            ],
            "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70}
        },
        status_code=200
    )

    # Mock Qdrant client's search method directly
    mock_qdrant_client_instance = MagicMock()
    mock_qdrant_client_instance.search.return_value = [
        MagicMock(id="mock-chunk-id-1", score=0.99, payload={
            "content_chunk_id": "00000000-0000-0000-0000-000000000001",
            "source_url": "/docs/intro",
            "section_title": "Introduction to ROS 2",
            "document_id": "intro.md",
            "text_content": "ROS 2 is the Robot Operating System version 2."
        })
    ]
    with patch('src.services.qdrant_client.get_qdrant_client', return_value=mock_qdrant_client_instance):
        # Valid request body
        valid_request_payload = {
            "query": "What is ROS 2?",
            "context_selection": "ROS 2 uses DDS.",
            "session_id": "a-session-id"
        }
        
        response = client_with_overrides.post("/chat", json=valid_request_payload)
        
        assert response.status_code == 200
        ChatResponse(**response.json()) # Pydantic will raise ValidationError if schema is not adhered
        
        response_data = response.json()
        assert "answer" in response_data
        assert isinstance(response_data["answer"], str)
        assert "references" in response_data
        assert isinstance(response_data["references"], list)
        assert "session_id" in response_data
        assert isinstance(response_data["session_id"], str)

