# 📁 apis/travel_api.py
# API endpoints for travel agent

from fastapi import APIRouter

from src.core.deps import db_dependency
from src.services import process_chat_message, get_all_messages
from src.models.schema import ChatRequest, ChatResponse, MessageHistoryResponse
from src.exceptions import TravelAgentError


# ------------------------------------------------------------------
# 🌐 Router
# ------------------------------------------------------------------

router = APIRouter(prefix="/travel", tags=["Travel Agent"])


# ------------------------------------------------------------------
# 🚀 Endpoints
# ------------------------------------------------------------------

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: db_dependency):
    """
    Process a user message and get AI response.
    
    Args:
        request: ChatRequest with user message
        db: Database session
        
    Returns:
        ChatResponse with AI response
    """
    try:
        result = process_chat_message(db, request.message)
        return ChatResponse(response=result["response"])
        
    except Exception as e:
        raise TravelAgentError(
            message=f"Error processing message: {str(e)}",
            error_code="CHAT_PROCESSING_ERROR",
            status_code=500,
        ) from e


@router.get("/history", response_model=MessageHistoryResponse)
async def get_history(db: db_dependency):
    """
    Get all conversation history.
    
    Args:
        db: Database session
        
    Returns:
        MessageHistoryResponse with all messages
    """
    try:
        messages = get_all_messages(db)
        return MessageHistoryResponse(messages=messages)
        
    except Exception as e:
        raise TravelAgentError(
            message=f"Error fetching history: {str(e)}",
            error_code="HISTORY_FETCH_ERROR",
            status_code=500,
        ) from e
