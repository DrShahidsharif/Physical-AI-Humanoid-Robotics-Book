#!/usr/bin/env python3
"""
Script to process book content (PDF/Markdown), chunk it, and upload to Qdrant using Qwen embeddings
"""
import asyncio
import argparse
from pathlib import Path
from typing import List
from src.services.qdrant_service import qdrant_service
from src.services.embedding_service import embedding_service


def read_book_content(file_path: str) -> str:
    """Read book content from file (supports .txt, .md, .pdf)"""
    file_path = Path(file_path)

    if file_path.suffix.lower() == '.pdf':
        # For PDF files, we would use PyPDF2 or similar
        # Since we don't have PDF processing dependencies installed, we'll simulate
        print(f"Warning: PDF processing requires additional dependencies. Reading as text...")
        with open(file_path, 'rb') as f:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    elif file_path.suffix.lower() in ['.md', '.txt']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If this isn't the last chunk, try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings near the end
            chunk_text = text[start:end]
            last_sentence_end = max(
                chunk_text.rfind('.'),
                chunk_text.rfind('!'),
                chunk_text.rfind('?'),
                chunk_text.rfind('\n')
            )

            if last_sentence_end > chunk_size // 2:  # Only break if we're not cutting too early
                end = start + last_sentence_end + 1
        else:
            end = len(text)

        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)

        # Move start position with overlap
        next_start = end - overlap if end < len(text) else end
        start = max(next_start, start + 1)  # Ensure we make progress

        # If we're not making progress, just advance by chunk_size
        if start >= end:
            start = end

    return chunks


async def process_book(book_path: str, book_id: str):
    """Process a book file and store embeddings in Qdrant"""
    print(f"Processing book: {book_path}")

    # Read the book content
    content = read_book_content(book_path)
    print(f"Book content length: {len(content)} characters")

    # Chunk the text
    chunks = chunk_text(content)
    print(f"Created {len(chunks)} chunks")

    # Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")

        # Generate embedding
        try:
            embedding = await embedding_service.generate_embedding(chunk)
        except Exception as e:
            print(f"Error generating embedding for chunk {i+1}: {e}")
            continue

        # Store in Qdrant
        content_id = f"{book_id}_chunk_{i}"
        try:
            await qdrant_service.store_embeddings(
                content_id=content_id,
                embedding_vector=embedding,
                book_id=book_id,
                text_chunk=chunk,
                chunk_index=i
            )
            print(f"Stored chunk {i+1} in Qdrant")
        except Exception as e:
            print(f"Error storing chunk {i+1} in Qdrant: {e}")
            continue

    print(f"Successfully processed and stored {book_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process book content and store embeddings in Qdrant")
    parser.add_argument("--book-path", required=True, help="Path to the book file (PDF, MD, or TXT)")
    parser.add_argument("--book-id", required=True, help="Unique identifier for the book")

    args = parser.parse_args()

    asyncio.run(process_book(args.book_path, args.book_id))