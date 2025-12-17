from typing import List
from src.services.gemini_service import get_gemini_embedding
from src.services.gemini_service import get_gemini_chat_completion
from src.services.qdrant_client import search_vectors
from src.services.neon_db import get_db, ContentChunk # Added
from src.models.chat_models import Reference
from sqlalchemy.orm import Session # Added
from fastapi import Depends # Added

async def generate_rag_response(
    user_query: str, 
    chat_history: List[dict] = None, 
    context_selection: str = None,
    db: Session = Depends(get_db) # Added DB dependency
) -> (str, List[Reference]):
    """
    Orchestrates the RAG pipeline to generate a response and retrieve references.
    
    Args:
        user_query: The user's question.
        chat_history: Optional list of previous chat messages (for conversational context).
        context_selection: Optional text selected by the user to provide additional context.
        db: SQLAlchemy session dependency.

    Returns:
        A tuple containing the generated answer (str) and a list of Reference objects.
    """

    # 1. Prepare the query for embedding and retrieval
    query_for_retrieval = user_query
    if context_selection:
        query_for_retrieval = f"Context: {context_selection}\nQuestion: {user_query}"

    # 2. Generate embedding for the query using Gemini
    query_embedding = get_gemini_embedding(query_for_retrieval)

    # 3. Retrieve relevant documents from Qdrant
    retrieved_chunks_info = search_vectors(query_embedding, limit=5, min_score=0.7)

    context_texts = []
    references = []
    
    # Fetch full ContentChunk from Neon DB using the IDs from Qdrant
    for hit in retrieved_chunks_info:
        payload = hit.payload
        content_chunk_id = payload.get('content_chunk_id')
        if content_chunk_id:
            # Query the database for the full content chunk
            db_chunk = db.query(ContentChunk).filter(ContentChunk.id == content_chunk_id).first()
            if db_chunk:
                context_texts.append(db_chunk.text_content)
                references.append(Reference(url=db_chunk.source_url, title=db_chunk.section_title))

    # Remove duplicates from references
    unique_references = list({ref.url: ref for ref in references}.values())

    # If no context found, just use the user query for chat completion
    if not context_texts:
        system_message = {
            "role": "system",
            "content": (
                "You are an AI assistant specialized in Physical AI and Humanoid Robotics. "
                "You don't have enough information from your knowledge base to answer this question. "
                "Please state that you don't have enough information based on your current knowledge."
            ),
        }
    else:
        system_message = {
            "role": "system",
            "content": (
                "You are an AI assistant specialized in Physical AI and Humanoid Robotics. "
                "Answer the user's question concisely based ONLY on the provided context. "
                "If the answer cannot be found in the context, state that you don't have enough information. "
                "Cite your sources using the provided URL and section title where applicable."
                f"\n\nContext:\n{'-'*80}\n" + "\n".join(context_texts) + f"\n{'-'*80}"
            ),
        }

    messages = [system_message]
    if chat_history:
        messages.extend(chat_history) # Add previous history if provided
    messages.append({"role": "user", "content": user_query})

    # 5. Generate completion using Gemini's chat model
    answer = get_gemini_chat_completion(messages)

    return answer, unique_references
