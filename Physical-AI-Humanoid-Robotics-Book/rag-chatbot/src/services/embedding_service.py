import os
import httpx
from typing import List
import random


class EmbeddingService:
    def __init__(self):
        # Use OpenRouter embeddings by default
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.use_mock = not self.openrouter_api_key or self.openrouter_api_key.startswith("sk-")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using OpenRouter API or mock if not available"""
        if self.use_mock:
            # Generate a mock embedding (768 dimensions to match nomic-embed-text-v1.5)
            return [random.random() * 2 - 1 for _ in range(768)]  # Values between -1 and 1
        else:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "nomic-ai/nomic-embed-text-v1.5",
                "input": text
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )

                if response.status_code != 200:
                    raise Exception(f"Embedding API error: {response.status_code} - {response.text}")

                result = response.json()
                return result["data"][0]["embedding"]

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings


# Create a global instance
embedding_service = EmbeddingService()