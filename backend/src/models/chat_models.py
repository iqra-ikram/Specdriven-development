from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

# Reference model as defined in data-model.md and chat_api.json
class Reference(BaseModel):
    url: str
    title: Optional[str] = None

# ChatMessage model as defined in data-model.md
class ChatMessage(BaseModel):
    message_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    sender: str # "user" or "chatbot"
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    context_selection: Optional[str] = None
    source_references: Optional[List[Reference]] = None

# ContentChunk Pydantic model (for API communication, mirroring the ORM model)
class ContentChunk(BaseModel):
    id: uuid.UUID
    text_content: str
    source_url: str
    section_title: Optional[str] = None
    document_id: str
    chunk_order: int
    created_at: datetime
    updated_at: datetime

# IngestRequest model from ingest_api.json / chat_api.json
class IngestRequest(BaseModel):
    document_id: str
    content: str
    source_url: str
    section_title: Optional[str] = None

# IngestResponse model from ingest_api.json / chat_api.json
class IngestResponse(BaseModel):
    status: str # "success" or "error"
    message: str

# ChatRequest model from chat_api.json
class ChatRequest(BaseModel):
    query: str
    context_selection: Optional[str] = None
    session_id: Optional[str] = None # Using str for session_id as it might be frontend-generated

# ChatResponse model from chat_api.json
class ChatResponse(BaseModel):
    answer: str
    references: List[Reference] = Field(default_factory=list)
    session_id: str
