from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Annotated, Optional
import uuid # Added
from sqlalchemy.orm import Session # Added
from fastapi import Depends # Added
from dotenv import load_dotenv # Added
import os # Added

from ..models.chat_models import IngestRequest, IngestResponse
from ..core.rag_pipeline import generate_rag_response
from ..services.neon_db import get_db # Added

load_dotenv()

router = APIRouter()

async def verify_api_key(x_api_key: Annotated[Optional[str], Header()] = None):
    ingestion_api_key = os.getenv("INGESTION_API_KEY")
    if not ingestion_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INGESTION_API_KEY is not configured on the server."
        )
    if x_api_key is None or x_api_key != ingestion_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key

@router.post("/ingest_content", response_model=IngestResponse, tags=["Ingestion"])
async def ingest_content_endpoint(
    request: IngestRequest,
    api_key: Annotated[str, Depends(verify_api_key)]
):
    """
    Ingest processed Docusaurus content chunks into the RAG system.
    This endpoint is typically used by an internal script or CI/CD pipeline to update the chatbot's knowledge base.
    Requires an API key for authentication.
    """
    
    # TODO: Implement the actual ingestion logic here.
    # This will involve:
    # 1. Storing the content in Neon Postgres (ContentChunk)
    # 2. Generating embeddings for request.content using openai_service.py
    # 3. Upserting the embeddings and metadata into Qdrant using qdrant_client.py
    
    # For now, just return a success response
    print(f"Received content for document_id: {request.document_id}, source_url: {request.source_url}")
    return IngestResponse(status="success", message="Content chunk received for ingestion (processing TBD).")

from ..models.chat_models import ChatRequest, ChatResponse
from ..core.rag_pipeline import generate_rag_response

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)): # Added db dependency
    """
    Handle user chat queries, retrieve relevant information, and generate responses.
    """
    session_id = request.session_id if request.session_id else str(uuid.uuid4())
    
    answer, references = await generate_rag_response(
        user_query=request.query,
        context_selection=request.context_selection,
        chat_history=[], # TODO: Implement chat history management if needed
        db=db # Passed db dependency
    )
    
    return ChatResponse(answer=answer, references=references, session_id=session_id)

