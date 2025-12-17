"""
Document Ingestion Script for RAG System
Reads markdown files from Docusaurus docs, chunks them, generates embeddings using FastEmbed,
and stores them in Qdrant vector database and Neon PostgreSQL.
"""

import os
import sys
import uuid
from pathlib import Path
from typing import List, Tuple
import re

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.gemini_service import get_gemini_embedding
from src.services.qdrant_client import recreate_qdrant_collection, upsert_vectors, VECTOR_SIZE
from src.services.neon_db import get_engine, get_session_local, ContentChunk, create_db_and_tables

def ingest_documents(docs_directory: str):
    """
    Main ingestion function.
    Reads all markdown files, chunks them, generates embeddings, and stores in DB.
    """
    def read_markdown_file(file_path: Path) -> Tuple[str, str]:
        """
        Reads a markdown file and extracts title and content.
        
        Returns:
            Tuple of (title, content)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract title from first heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # Use filename as title
            title = file_path.stem.replace('-', ' ').title()
        
        return title, content

    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Splits text into overlapping chunks.
        
        Args:
            text: The text to chunk
            chunk_size: Target size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        # Simple character-based chunking
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:  # Only break if we're past halfway
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Filter empty chunks

    def get_relative_url(file_path: Path, docs_root: Path) -> str:
        """
        Converts file path to Docusaurus URL.
        
        Example: docs/intro.md -> /docs/intro
        """
        relative_path = file_path.relative_to(docs_root.parent)
        url_path = str(relative_path).replace('\\', '/')
        
        # Remove .md extension and convert to URL
        if url_path.endswith('.md') or url_path.endswith('.mdx'):
            url_path = url_path.rsplit('.', 1)[0]
        
        return f"/{url_path}"

    docs_path = Path(docs_directory)
    
    if not docs_path.exists():
        print(f"Error: Directory {docs_directory} does not exist!")
        return
    
    print("=" * 80)
    print("Starting Document Ingestion")
    print("=" * 80)
    
    # Step 1: Recreate Qdrant collection
    print("\n[1/5] Recreating Qdrant collection...")
    recreate_qdrant_collection()
    print(f"✓ Collection recreated with {VECTOR_SIZE}-dimensional vectors")
    
    # Step 2: Ensure database tables exist
    print("\n[2/5] Setting up database...")
    create_db_and_tables()
    print("✓ Database tables ready")
    
    # Step 3: Find all markdown files
    print("\n[3/5] Finding markdown files...")
    md_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))
    # Filter out node_modules
    md_files = [f for f in md_files if 'node_modules' not in str(f)]
    print(f"✓ Found {len(md_files)} markdown files")
    
    # Step 4: Process each file
    print("\n[4/5] Processing documents...")
    
    all_chunks_data = []
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        for idx, file_path in enumerate(md_files, 1):
            print(f"\n  [{idx}/{len(md_files)}] Processing: {file_path.name}")
            
            # Read file
            title, content = read_markdown_file(file_path)
            
            # Chunk content
            chunks = chunk_text(content)
            print(f"    → Created {len(chunks)} chunks")
            
            # Get URL
            source_url = get_relative_url(file_path, docs_path)
            
            # Process each chunk
            for chunk_idx, chunk in enumerate(chunks):
                chunk_id = uuid.uuid4()
                
                # Store in database
                db_chunk = ContentChunk(
                    id=chunk_id,
                    text_content=chunk,
                    source_url=source_url,
                    section_title=title,
                    document_id=str(file_path.relative_to(docs_path)),
                    chunk_order=chunk_idx
                )
                db.add(db_chunk)
                
                # Prepare for embedding
                all_chunks_data.append({
                    'id': chunk_id,
                    'text': chunk,
                    'source_url': source_url,
                    'section_title': title
                })
        
        # Commit all chunks to database
        db.commit()
        print(f"\n  ✓ Stored {len(all_chunks_data)} chunks in database")
        
    finally:
        db.close()
    
    # Step 5: Generate embeddings and upload to Qdrant
    print("\n[5/5] Generating embeddings and uploading to Qdrant...")
    
    # Process in batches for efficiency
    batch_size = 32
    total_batches = (len(all_chunks_data) + batch_size - 1) // batch_size
    
    for batch_idx in range(0, len(all_chunks_data), batch_size):
        batch = all_chunks_data[batch_idx:batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        
        print(f"  Batch {batch_num}/{total_batches}: Embedding {len(batch)} chunks...")
        
        # Generate embeddings
        texts = [item['text'] for item in batch]
        embeddings = [get_gemini_embedding(text) for text in texts]
        
        # Prepare vectors for Qdrant
        vectors_to_upsert = [
            {
                'id': str(item['id']),
                'vector': embedding,
                'payload': {
                    'content_chunk_id': str(item['id']),
                    'source_url': item['source_url'],
                    'section_title': item['section_title']
                }
            }
            for item, embedding in zip(batch, embeddings)
        ]
        
        # Upload to Qdrant
        upsert_vectors(vectors_to_upsert)
    
    print(f"\n  ✓ Uploaded {len(all_chunks_data)} vectors to Qdrant")
    
    print("\n" + "=" * 80)
    print("✓ Ingestion Complete!")
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  - Files processed: {len(md_files)}")
    print(f"  - Total chunks: {len(all_chunks_data)}")
    print(f"  - Embedding model: Gemini embedding-001 ({VECTOR_SIZE}D)")
    print(f"  - Vector database: Qdrant")
    print(f"  - Metadata database: Neon PostgreSQL")
    print("\nYour RAG system is ready to use! 🚀")

if __name__ == "__main__":
    # Default to docusaurus docs directory
    docs_dir = Path(__file__).parent.parent / "docusaurus-root" / "docs"
    
    if len(sys.argv) > 1:
        docs_dir = Path(sys.argv[1])
    
    print(f"Ingesting documents from: {docs_dir}")
    ingest_documents(str(docs_dir))
