from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from src.services.rag_service import rag_service


router = APIRouter()


class AskRequest(BaseModel):
    question: str
    session_id: str
    book_id: Optional[str] = None


@router.post("/ask")
async def ask_endpoint(request: AskRequest):
    """
    Endpoint for general questions about the entire book
    """
    try:
        result = await rag_service.query(
            user_question=request.question,
            selected_text=None,  # No selected text, will use vector search
            book_id=request.book_id,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing general query: {str(e)}")