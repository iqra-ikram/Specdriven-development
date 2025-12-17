"""
Initialize Qdrant collection for the RAG system.
"""
from src.services.qdrant_client import get_or_create_qdrant_collection

if __name__ == "__main__":
    print("Initializing Qdrant collection...")
    get_or_create_qdrant_collection()
    print("Qdrant collection initialized successfully!")
