#!/usr/bin/env python3
"""
Script to ingest book data into Qdrant vector store
"""
import asyncio
import os
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingService


def chunk_text(text: str, chunk_size: int = 500) -> list:
    """Split text into 500-character chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    return chunks


async def main():
    # Initialize services
    qdrant_service = QdrantService()
    embedding_service = EmbeddingService()

    # Read the book file
    if not os.path.exists("book.txt"):
        print("Creating sample book.txt file...")
        with open("book.txt", "w") as f:
            f.write("""
Artificial Intelligence and Large Language Models

Introduction to AI
Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.

Large Language Models
Large language models (LLMs) are a type of language model notable for their size and capabilities. These models are trained on vast amounts of text data and can generate human-like text, answer questions, and perform various natural language processing tasks.

Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) is a technique that combines the generative capabilities of LLMs with the precision of information retrieval. It retrieves relevant documents from a knowledge base and uses them as context for generating responses.

Vector Databases
Vector databases store and index vector embeddings, allowing for fast similarity searches. They are essential for RAG systems as they enable efficient retrieval of relevant information based on semantic similarity.
""")

    with open("book.txt", "r", encoding="utf-8") as f:
        book_content = f.read()

    print(f"Loaded book content ({len(book_content)} characters)")

    # Chunk the text
    chunks = chunk_text(book_content)
    print(f"Created {len(chunks)} chunks of 500 characters each")

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
        content_id = f"chunk_{i}"
        try:
            await qdrant_service.store_embeddings(
                content_id=content_id,
                embedding_vector=embedding,
                text_chunk=chunk
            )
            print(f"Stored chunk {i+1} in Qdrant")
        except Exception as e:
            print(f"Error storing chunk {i+1} in Qdrant: {e}")
            continue

    print("Successfully ingested book data into Qdrant!")


if __name__ == "__main__":
    asyncio.run(main())