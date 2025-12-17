"""
Test Qdrant client search functionality.
"""
from src.services.qdrant_client import get_qdrant_client, COLLECTION_NAME
from src.services.openai_service import get_embedding

if __name__ == "__main__":
    print("Testing Qdrant client...")
    client = get_qdrant_client()
    print(f"Client type: {type(client)}")
    print(f"Client methods: {[m for m in dir(client) if 'search' in m.lower()]}")
    
    # Try to get a test embedding
    print("\nGenerating test embedding...")
    test_embedding = get_embedding("test query")
    print(f"Embedding generated, length: {len(test_embedding)}")
    
    # Try to search
    print(f"\nSearching in collection: {COLLECTION_NAME}")
    try:
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=test_embedding,
            limit=5
        )
        print(f"Search successful! Found {len(results.points)} results")
    except Exception as e:
        print(f"Search failed with error: {e}")
        print(f"Error type: {type(e)}")
