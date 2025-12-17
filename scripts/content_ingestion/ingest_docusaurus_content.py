import os
import argparse
import httpx # or requests
from dotenv import load_dotenv
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
import re
import uuid

load_dotenv()

BACKEND_INGEST_URL = os.getenv("BACKEND_INGEST_URL", "http://localhost:8000/api/ingest_content")
INGESTION_API_KEY = os.getenv("INGESTION_API_KEY")

if not INGESTION_API_KEY:
    print("Warning: INGESTION_API_KEY is not set. Ingestion may fail if endpoint requires it.")

# Initialize MarkdownIt parser
md = MarkdownIt()

def parse_markdown_file(file_path: str) -> str:
    """Reads a markdown file and returns its content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_content_semantic(markdown_content: str, source_url: str, document_id: str, max_tokens: int = 500) -> list[dict]:
    """
    Semantically chunks markdown content based on headers and then sentence splits.
    Extracts metadata: source_url, section_title.
    """
    html_content = md.render(markdown_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    chunks = []
    current_chunk_text = []
    current_section_title = None
    chunk_order = 0

    # Find all headings (h1, h2, h3) and paragraphs
    elements = soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])

    for element in elements:
        element_text = element.get_text(separator=" ", strip=True)
        
        if element.name in ['h1', 'h2', 'h3']:
            # If a new header, and there's accumulated text, save current chunk
            if current_chunk_text:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "text_content": " ".join(current_chunk_text),
                    "source_url": source_url,
                    "section_title": current_section_title,
                    "document_id": document_id,
                    "chunk_order": chunk_order,
                })
                chunk_order += 1
                current_chunk_text = [] # Reset for new section
            
            current_section_title = element_text # Update section title
            current_chunk_text.append(element_text) # Include header in its own section
        else:
            # For paragraphs and list items, split into sentences and add
            sentences = re.split(r'(?<=[.!?])\s+', element_text)
            for sentence in sentences:
                if sentence: # Avoid empty strings
                    current_chunk_text.append(sentence)
                    # Basic token length check (very rough, tiktoken is better but more complex for simple example)
                    if len(" ".join(current_chunk_text).split()) > max_tokens / 2: # Heuristic to cut before max
                        chunks.append({
                            "id": str(uuid.uuid4()),
                            "text_content": " ".join(current_chunk_text),
                            "source_url": source_url,
                            "section_title": current_section_title,
                            "document_id": document_id,
                            "chunk_order": chunk_order,
                        })
                        chunk_order += 1
                        current_chunk_text = []

    # Add any remaining text as a final chunk
    if current_chunk_text:
        chunks.append({
            "id": str(uuid.uuid4()),
            "text_content": " ".join(current_chunk_text),
            "source_url": source_url,
            "section_title": current_section_title,
            "document_id": document_id,
            "chunk_order": chunk_order,
        })
        
    # Final pass to combine very small chunks or split very large ones if needed
    # This is a basic implementation; a more robust one would use tiktoken for precise token counting
    # and more sophisticated merging/splitting logic.
    final_chunks = []
    temp_chunk = []
    for chunk in chunks:
        if len(" ".join(temp_chunk).split()) + len(chunk["text_content"].split()) < max_tokens:
            temp_chunk.append(chunk["text_content"])
        else:
            if temp_chunk:
                final_chunks.append({**chunk, "text_content": " ".join(temp_chunk)})
                temp_chunk = [chunk["text_content"]]
            else: # If a single chunk is already too large
                final_chunks.append(chunk)
    if temp_chunk:
        final_chunks.append({**chunks[-1], "text_content": " ".join(temp_chunk)}) # Use metadata from last sub-chunk
        
    return final_chunks


async def send_chunk_to_backend(chunk: dict):
    """Sends a single content chunk to the FastAPI ingestion endpoint."""
    headers = {"X-API-Key": INGESTION_API_KEY} if INGESTION_API_KEY else {}
    payload = {
        "document_id": chunk["document_id"],
        "content": chunk["text_content"],
        "source_url": chunk["source_url"],
        "section_title": chunk["section_title"]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BACKEND_INGEST_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
            print(f"Successfully ingested chunk for {chunk['document_id']} (Order: {chunk['chunk_order']})")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error ingesting chunk for {chunk['document_id']}: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error ingesting chunk for {chunk['document_id']}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Ingest Docusaurus Markdown content into the RAG chatbot backend.")
    parser.add_argument("--docusaurus-docs-path", type=str, required=True,
                        help="Path to the Docusaurus 'docs' directory (e.g., ../docusaurus-root/docs)")
    parser.add_argument("--backend-url", type=str, default=BACKEND_INGEST_URL,
                        help=f"URL of the backend ingestion endpoint (default: {BACKEND_INGEST_URL})")
    parser.add_argument("--api-key", type=str, default=INGESTION_API_KEY,
                        help="API key for authentication with the ingestion endpoint.")

    args = parser.parse_args()

    global BACKEND_INGEST_URL, INGESTION_API_KEY
    BACKEND_INGEST_URL = args.backend_url
    INGESTION_API_KEY = args.api_key

    docs_path = args.docusaurus_docs_path
    if not os.path.isdir(docs_path):
        print(f"Error: Docusaurus docs path not found: {docs_path}")
        return

    markdown_files = []
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                markdown_files.append(os.path.join(root, file))

    print(f"Found {len(markdown_files)} markdown files to ingest.")

    for file_path in markdown_files:
        print(f"Processing: {file_path}")
        markdown_content = parse_markdown_file(file_path)
        
        # Determine document_id (relative path from docs_path) and source_url
        relative_path = os.path.relpath(file_path, docs_path)
        document_id = relative_path # Use relative path as document_id
        
        # Assuming Docusaurus URLs are based on file path without extension
        source_url_slug = os.path.splitext(relative_path)[0]
        # This needs to be refined based on actual Docusaurus URL structure.
        # For simplicity, let's assume /docs/<path_to_file_without_ext>
        source_url = f"/docs/{source_url_slug}" 

        chunks = chunk_content_semantic(markdown_content, source_url, document_id)
        print(f"Generated {len(chunks)} chunks for {file_path}")

        for i, chunk in enumerate(chunks):
            # Assign chunk_order
            chunk["chunk_order"] = i
            await send_chunk_to_backend(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())