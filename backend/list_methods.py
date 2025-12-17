"""
List all Qdrant client methods.
"""
from src.services.qdrant_client import get_qdrant_client

if __name__ == "__main__":
    client = get_qdrant_client()
    print("All client methods:")
    methods = [m for m in dir(client) if not m.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
