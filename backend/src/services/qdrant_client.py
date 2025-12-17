from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

_qdrant_client = None

def get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        qdrant_host = os.getenv("QDRANT_HOST")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_host or not qdrant_api_key:
            raise ValueError("QDRANT_HOST and QDRANT_API_KEY environment variables must be set.")
        
        _qdrant_client = QdrantClient(
            url=qdrant_host, # Changed from host to url
            api_key=qdrant_api_key,
        )
    return _qdrant_client

COLLECTION_NAME = "content_chunks"
VECTOR_SIZE = 768 # Updated to match Gemini's embedding-001 output dimension

def recreate_qdrant_collection():
    """
    Deletes and recreates the Qdrant collection for content chunks.
    This is useful for development/testing but should be used with caution in production.
    """
    client = get_qdrant_client()
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' recreated.")

def get_or_create_qdrant_collection():
    """
    Ensures the Qdrant collection exists. If not, it creates it.
    """
    client = get_qdrant_client()
    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception: # Qdrant client raises an exception if collection not found
        print(f"Collection '{COLLECTION_NAME}' not found, creating it...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created.")

def upsert_vectors(vectors_with_payloads: list):
    """
    Upserts vectors into the Qdrant collection.

    Args:
        vectors_with_payloads: A list of dictionaries, each containing 'id', 'vector', and 'payload'.
                                'id' should be a UUID string or object, 'vector' a list of floats,
                                'payload' a dictionary.
    """
    client = get_qdrant_client()
    points = [
        models.PointStruct(
            id=str(item["id"]),
            vector=item["vector"],
            payload=item["payload"]
        )
        for item in vectors_with_payloads
    ]
    
    operation_info = client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points,
    )
    print(f"Qdrant upsert operation status: {operation_info.status}")

def search_vectors(query_vector: list, limit: int = 5, min_score: float = 0.7):
    """
    Searches the Qdrant collection for vectors similar to the query_vector.

    Args:
        query_vector: The embedding of the query.
        limit: Maximum number of results to return.
        min_score: Minimum similarity score for results to be returned.

    Returns:
        A list of search results, each containing 'id', 'score', and 'payload'.
    """
    client = get_qdrant_client()
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        score_threshold=min_score,
    )
    return search_result.points

