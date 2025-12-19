from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.models import chat_history
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingService
from src.services.openrouter_service import OpenRouterService
import os


# Initialize services (will be initialized on first use)
qdrant_service = None
openrouter_service = None
embedding_service = None

def get_qdrant_service():
    global qdrant_service
    if qdrant_service is None:
        qdrant_service = QdrantService()
    return qdrant_service

def get_openrouter_service():
    global openrouter_service
    if openrouter_service is None:
        openrouter_service = OpenRouterService()
    return openrouter_service

def get_embedding_service():
    global embedding_service
    if embedding_service is None:
        embedding_service = EmbeddingService()
    return embedding_service

app = FastAPI(title="RAG Chatbot Backend", version="1.0.0")


class AskRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    context_used: str


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """
    Endpoint to ask questions with optional selected text
    If selected_text is provided, use it directly as context
    Otherwise, perform vector search in Qdrant
    """
    try:
        # Get services (initialize on first use)
        qdrant_svc = get_qdrant_service()
        openrouter_svc = get_openrouter_service()
        embedding_svc = get_embedding_service()

        # Determine context based on whether selected_text is provided
        if request.selected_text:
            context = request.selected_text
        else:
            # Generate embedding for the question
            query_embedding = await embedding_svc.generate_embedding(request.question)

            # Search for similar content in Qdrant
            search_results = await qdrant_svc.search_similar(
                query_vector=query_embedding,
                limit=5
            )

            # Combine the most relevant results as context
            context_parts = [result["text_chunk"] for result in search_results]
            context = "\n\n".join(context_parts)

        # Create the prompt for the LLM
        system_prompt = {
            "role": "system",
            "content": "You are an AI assistant helping users understand book content. Answer questions based on the provided context. Be helpful, accurate, and concise."
        }

        user_prompt = {
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {request.question}\n\nPlease answer the question based on the context provided."
        }

        messages = [system_prompt, user_prompt]

        # Get response from OpenRouter
        answer = await openrouter_svc.get_completion(messages)

        # Log the interaction to in-memory storage
        chat_history.add_entry(
            question=request.question,
            answer=answer,
            context_used=context
        )

        return AskResponse(answer=answer, context_used=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running!"}


@app.get("/health")
async def health_check():
    qdrant_svc = get_qdrant_service()
    status = "connected" if qdrant_svc.is_connected else "not connected"

    return {"status": "healthy", "services": {
        "qdrant": status,
        "openrouter": "configured",
        "storage": "in-memory"
    }}