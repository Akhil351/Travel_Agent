# 📁 apis/travel_api.py
# API endpoints for travel agent

from fastapi import APIRouter
from uuid import UUID

from src.core.deps import db_dependency
from src.services import process_chat_message, get_all_messages, get_or_create_summary
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
    
    If session_id is provided: Continue existing conversation
    If session_id is not provided: Start new conversation (new session_id returned)
    
    Args:
        request: ChatRequest with user message and optional session_id
        db: Database session
        
    Returns:
        ChatResponse with AI response and session_id
    """
    try:
        result, session_id = process_chat_message(
            db, 
            request.message, 
            request.session_id
        )
        return ChatResponse(
            response=result["response"],
            session_id=session_id
        )
        
    except Exception as e:
        raise TravelAgentError(
            message=f"Error processing message: {str(e)}",
            error_code="CHAT_PROCESSING_ERROR",
            status_code=500,
        ) from e


@router.get("/history/{session_id}", response_model=MessageHistoryResponse)
async def get_history(session_id: UUID, db: db_dependency):
    """
    Get conversation history for a specific session.
    
    Args:
        session_id: UUID of the conversation session
        db: Database session
        
    Returns:
        MessageHistoryResponse with all messages for that session
    """
    try:
        # Get the conversation summary record
        summary = get_or_create_summary(db, session_id)
        
        # Get all messages for this conversation
        messages = get_all_messages(db, summary.id)
        
        return MessageHistoryResponse(messages=messages)
        
    except Exception as e:
        raise TravelAgentError(
            message=f"Error fetching history: {str(e)}",
            error_code="HISTORY_FETCH_ERROR",
            status_code=500,
        ) from e
