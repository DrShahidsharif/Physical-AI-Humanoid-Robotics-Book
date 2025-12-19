from typing import List, Dict, Optional
from src.services.qdrant_service import qdrant_service
from src.services.embedding_service import embedding_service
from src.services.openrouter_service import openrouter_service


class RAGService:
    def __init__(self):
        pass

    async def query(
        self,
        user_question: str,
        selected_text: Optional[str] = None,
        book_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Main RAG query method that handles both general and selected text queries
        """
        # Prepare context based on whether selected_text is provided
        if selected_text:
            # Use selected text directly as context
            context = selected_text
            sources = ["Selected Text"]
        else:
            # Perform similarity search in Qdrant to find relevant book context
            query_embedding = await embedding_service.generate_embedding(user_question)
            search_results = await qdrant_service.search_similar(
                query_vector=query_embedding,
                limit=5,
                book_id=book_id
            )

            # Combine the most relevant chunks as context
            context_parts = []
            sources = []
            for result in search_results:
                context_parts.append(result["text_chunk"])
                sources.append(f"Book Chunk {result['chunk_index']}")

            context = "\n\n".join(context_parts)

        # Create system prompt to keep the bot in-character as a book assistant
        system_prompt = {
            "role": "system",
            "content": """You are an intelligent book assistant designed to help readers understand and engage with book content.
            Your responses should be:
            1. Based solely on the provided book content
            2. Helpful, clear, and educational
            3. Respectful of the book's original context and meaning
            4. Focused on explaining concepts, answering questions, and providing insights based on the book
            5. Honest about limitations if the requested information is not in the provided context

            Do not make up information that is not in the provided context. If you don't know the answer based on the provided text, say so."""
        }

        # Prepare messages for the LLM
        user_message = {
            "role": "user",
            "content": f"""Based on the following book content, please answer this question: {user_question}

Book Content:
{context}"""
        }

        messages = [system_prompt, user_message]

        # Get response from LLM
        llm_response = await openrouter_service.get_completion(messages)

        return {
            "answer": llm_response,
            "sources": sources,
            "session_id": session_id,
            "context_used": "selected_text" if selected_text else "book_content"
        }


# Singleton instance
rag_service = RAGService()