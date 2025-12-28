from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from typing import List, Dict, Optional


class QdrantService:
    def __init__(self):
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")

        # Try to connect to cloud Qdrant first, fall back to local
        try:
            # Initialize Qdrant client for cloud
            self.client = QdrantClient(
                url=self.url,
                api_key=self.api_key,
                prefer_grpc=False  # Using REST API
            )
            self.is_connected = True
        except Exception as e:
            print(f"Could not connect to cloud Qdrant: {e}")
            print("Attempting to connect to local Qdrant...")
            try:
                # Initialize Qdrant client for local instance
                self.client = QdrantClient(host="localhost", port=6333)
                self.is_connected = True
            except Exception as e2:
                print(f"Could not connect to local Qdrant either: {e2}")
                print("Qdrant service is not available. Using mock functionality.")
                self.is_connected = False

        self.collection_name = "book_data"
        if self.is_connected:
            self._initialize_collection()

    def _initialize_collection(self):
        """
        Initialize the Qdrant collection with appropriate configuration
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection if it doesn't exist
            # Using a common embedding dimension (we'll use 384 for nomic-embed-text-v1.5)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,  # Default size for nomic-embed-text-v1.5
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection '{self.collection_name}'")

    async def search_similar(
        self,
        query_vector: List[float],
        limit: int = 5
    ) -> List[Dict]:
        """
        Search for similar content in the vector database
        """
        if not self.is_connected:
            # Return empty results if Qdrant is not available
            return []

        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            # Extract relevant information
            results = []
            for hit in search_results:
                results.append({
                    "text_chunk": hit.payload.get("text", ""),
                    "score": hit.score
                })

            return results
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return []

    async def store_embeddings(
        self,
        content_id: str,
        embedding_vector: List[float],
        text_chunk: str
    ):
        """
        Store embeddings in Qdrant
        """
        if not self.is_connected:
            print("Qdrant not connected, skipping storage")
            return

        try:
            points = [
                models.PointStruct(
                    id=content_id,
                    vector=embedding_vector,
                    payload={
                        "text": text_chunk
                    }
                )
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        except Exception as e:
            print(f"Error storing in Qdrant: {e}")