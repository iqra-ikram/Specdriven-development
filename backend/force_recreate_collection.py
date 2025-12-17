"""
Force recreate Qdrant collection with correct 384D dimensions
This script will delete and recreate the collection, fixing the dimension mismatch
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.qdrant_client import get_qdrant_client, COLLECTION_NAME, VECTOR_SIZE
from qdrant_client import models

def force_recreate():
    print("=" * 80)
    print("FORCE RECREATING QDRANT COLLECTION")
    print("=" * 80)
    
    client = get_qdrant_client()
    
    # Step 1: Delete existing collection
    print(f"\n[1/3] Deleting existing collection '{COLLECTION_NAME}'...")
    try:
        client.delete_collection(collection_name=COLLECTION_NAME)
        print(f"✓ Collection '{COLLECTION_NAME}' deleted")
    except Exception as e:
        print(f"Note: {e}")
        print("(Collection may not exist, continuing...)")
    
    # Step 2: Create new collection with 384D vectors
    print(f"\n[2/3] Creating new collection with {VECTOR_SIZE}-dimensional vectors...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE
        ),
    )
    print(f"✓ Collection '{COLLECTION_NAME}' created with {VECTOR_SIZE}D vectors")
    
    # Step 3: Verify
    print(f"\n[3/3] Verifying collection...")
    collection_info = client.get_collection(collection_name=COLLECTION_NAME)
    actual_size = collection_info.config.params.vectors.size
    print(f"✓ Verified: Vector dimension = {actual_size}")
    
    if actual_size == VECTOR_SIZE:
        print("\n" + "=" * 80)
        print("SUCCESS! Collection recreated with correct dimensions")
        print("=" * 80)
        print(f"\nNext step: Run 'poetry run python ingest_documents.py'")
    else:
        print(f"\n⚠ WARNING: Expected {VECTOR_SIZE}D but got {actual_size}D")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = force_recreate()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPlease check your .env file has:")
        print("  - QDRANT_HOST=your_qdrant_url")
        print("  - QDRANT_API_KEY=your_api_key")
        sys.exit(1)
