from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
from src.config.settings import settings
import logging


class QdrantService:
    def __init__(self):
        if settings.QDRANT_HOST:
            # Local instance
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )
        else:
            # Cloud instance
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )

        self.collection_name = "book_content"
        self._initialize_collection()

    def _initialize_collection(self):
        """
        Initialize the Qdrant collection with appropriate configuration
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logging.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # Qwen embedding dimensions
                    distance=models.Distance.COSINE
                )
            )
            logging.info(f"Created collection '{self.collection_name}'")

    async def search_similar(
        self,
        query_vector: List[float],
        limit: int = 5,
        book_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for similar content in the vector database
        """
        # Prepare filters
        filters = None
        if book_id:
            filters = models.Filter(
                must=[
                    models.FieldCondition(
                        key="book_id",
                        match=models.MatchValue(value=book_id)
                    )
                ]
            )

        # Perform search
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=filters,
            limit=limit
        )

        # Extract relevant information
        results = []
        for hit in search_results:
            results.append({
                "text_chunk": hit.payload.get("text_chunk", ""),
                "chunk_index": hit.payload.get("chunk_index", 0),
                "page_number": hit.payload.get("page_number"),
                "score": hit.score,
                "book_id": hit.payload.get("book_id")
            })

        return results

    async def store_embeddings(
        self,
        content_id: str,
        embedding_vector: List[float],
        book_id: str,
        text_chunk: str,
        chunk_index: int,
        page_number: Optional[int] = None
    ):
        """
        Store embeddings in Qdrant
        """
        points = [
            models.PointStruct(
                id=content_id,
                vector=embedding_vector,
                payload={
                    "text_chunk": text_chunk,
                    "book_id": book_id,
                    "chunk_index": chunk_index,
                    "page_number": page_number
                }
            )
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )


# Singleton instance
qdrant_service = QdrantService()