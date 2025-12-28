import asyncio
import os
from src.services.embedding_service import embedding_service

async def test_embedding():
    # Set the API key from the .env file
    from dotenv import load_dotenv
    load_dotenv()

    text = "This is a test sentence for embedding."
    try:
        embedding = await embedding_service.generate_embedding(text)
        print(f"Embedding generated successfully! Length: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
    except Exception as e:
        print(f"Error generating embedding: {e}")

if __name__ == "__main__":
    asyncio.run(test_embedding())