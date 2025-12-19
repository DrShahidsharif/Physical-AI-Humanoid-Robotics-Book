from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from src.services.rag_service import rag_service


router = APIRouter()


class QueryRequest(BaseModel):
    user_question: str
    selected_text: Optional[str] = None
    book_id: Optional[str] = None
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    session_id: Optional[str] = None
    context_used: str


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main query endpoint that accepts user_question and optional selected_text
    If selected_text is provided, use it directly as context
    If not, perform similarity search in Qdrant to find relevant book context
    """
    try:
        result = await rag_service.query(
            user_question=request.user_question,
            selected_text=request.selected_text,
            book_id=request.book_id,
            session_id=request.session_id
        )
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# Also include the original /ask-selection endpoint for compatibility
class AskSelectionRequest(BaseModel):
    question: str
    selected_text: str
    session_id: str


@router.post("/ask-selection")
async def ask_selection_endpoint(request: AskSelectionRequest):
    """
    Endpoint for questions about specific selected text
    """
    try:
        result = await rag_service.query(
            user_question=request.question,
            selected_text=request.selected_text,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing selection query: {str(e)}")