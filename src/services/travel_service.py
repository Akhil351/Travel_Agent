# 📁 services/travel_service.py
# Service layer for managing messages and conversation summaries

import json
import uuid
from typing import List, Dict, Tuple, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from src.models.psql import Message, ConversationSummary
from src.agents import build_travel_agent
from src.agents.summarize_agent import update_summary
from src.core import settings


# ------------------------------------------------------------------
# 🚀 Lazy Agent Initialization
# ------------------------------------------------------------------

_TRAVEL_AGENT = None


def get_travel_agent():
    """Get or create the travel agent (lazy initialization)."""
    global _TRAVEL_AGENT
    if _TRAVEL_AGENT is None:
        _TRAVEL_AGENT = build_travel_agent()
    return _TRAVEL_AGENT


# ------------------------------------------------------------------
# 📝 Conversation Summary Management
# ------------------------------------------------------------------

def get_or_create_summary(session: Session, session_id: UUID) -> ConversationSummary:
    """
    Get existing conversation summary or create new one.
    
    Args:
        session: Database session
        session_id: UUID of the conversation session
        
    Returns:
        ConversationSummary object
    """
    summary = session.query(ConversationSummary).filter(
        ConversationSummary.session_id == session_id
    ).first()
    
    if not summary:
        summary = ConversationSummary(
            session_id=session_id,
            summary=""
        )
        session.add(summary)
        session.commit()
        session.refresh(summary)
    
    return summary


def update_conversation_summary(
    session: Session, 
    summary_record: ConversationSummary
) -> None:
    """
    Update conversation summary with unsummarized messages.
    
    Args:
        session: Database session
        summary_record: ConversationSummary to update
    """
    # Get all unsummarized messages for this conversation
    unsummarized_messages = session.query(Message).filter(
        Message.conversation_summary_id == summary_record.id,
        Message.is_summarized == False
    ).order_by(Message.created_at.asc()).all()
    
    if not unsummarized_messages:
        return
    
    # Convert to dict format for summarize agent
    messages_dict = [
        {"role": msg.role, "content": msg.content}
        for msg in unsummarized_messages
    ]
    
    # Update summary using summarize agent
    new_summary = update_summary(
        current_summary=summary_record.summary,
        new_messages=messages_dict
    )
    
    # Update summary in database
    summary_record.summary = new_summary
    
    # Mark all those messages as summarized
    for msg in unsummarized_messages:
        msg.is_summarized = True
    
    session.commit()


# ------------------------------------------------------------------
# 💬 Message Management
# ------------------------------------------------------------------

def save_messages(
    session: Session, 
    user_message: str, 
    ai_message: str,
    conversation_summary_id: int
) -> None:
    """
    Save both user and AI messages to the database.
    
    Args:
        session: Database session
        user_message: User's message content
        ai_message: AI's response content
        conversation_summary_id: ID of the conversation summary
    """
    user_msg = Message(
        role="user",
        content=user_message,
        conversation_summary_id=conversation_summary_id,
        is_summarized=False
    )
    
    ai_msg = Message(
        role="ai",
        content=ai_message,
        conversation_summary_id=conversation_summary_id,
        is_summarized=False
    )
    
    session.add(user_msg)
    session.add(ai_msg)
    session.commit()


def get_unsummarized_messages(
    session: Session, 
    conversation_summary_id: int
) -> List[Dict[str, str]]:
    """
    Get all unsummarized messages for a conversation.
    
    Args:
        session: Database session
        conversation_summary_id: ID of the conversation summary
        
    Returns:
        List of message dictionaries with 'role' and 'content'
    """
    messages = session.query(Message).filter(
        Message.conversation_summary_id == conversation_summary_id,
        Message.is_summarized == False
    ).order_by(Message.created_at.asc()).all()
    
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def count_unsummarized_messages(
    session: Session, 
    conversation_summary_id: int
) -> int:
    """
    Count unsummarized messages for a conversation.
    
    Args:
        session: Database session
        conversation_summary_id: ID of the conversation summary
        
    Returns:
        Count of unsummarized messages
    """
    return session.query(Message).filter(
        Message.conversation_summary_id == conversation_summary_id,
        Message.is_summarized == False
    ).count()


def get_all_messages(session: Session, conversation_summary_id: int) -> List[Dict[str, str]]:
    """
    Get all messages for a conversation.
    
    Args:
        session: Database session
        conversation_summary_id: ID of the conversation summary
        
    Returns:
        List of message dictionaries with 'role' and 'content'
    """
    messages = session.query(Message).filter(
        Message.conversation_summary_id == conversation_summary_id
    ).order_by(Message.created_at.asc()).all()
    
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


# ------------------------------------------------------------------
# 🤖 Agent Runner
# ------------------------------------------------------------------

def run_travel_agent(
    user_message: str, 
    conversation_summary: str = "",
    unsummarized_messages: List[Dict[str, str]] = None
) -> str:
    """
    Run the travel agent with summary and recent messages.
    
    Args:
        user_message: Current user message
        conversation_summary: Compressed summary of old messages
        unsummarized_messages: Recent unsummarized messages
        
    Returns:
        AI response as string
    """
    # Build messages list
    messages = []
    
    # Add unsummarized messages (recent context)
    if unsummarized_messages:
        for msg in unsummarized_messages:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                messages.append(AIMessage(content=msg["content"]))
    
    # Add current user message
    messages.append(HumanMessage(content=user_message))
    
    # Initialize agent state with summary and messages
    initial_state = {
        "conversation_summary": conversation_summary,
        "messages": messages
    }
    
    # Get agent and invoke
    agent = get_travel_agent()
    result = agent.invoke(initial_state)
    
    # Extract final AI response
    final_message = result["messages"][-1]
    
    return final_message.content


# ------------------------------------------------------------------
# 🚀 Main Workflow
# ------------------------------------------------------------------

def process_chat_message(
    session: Session, 
    user_message: str,
    session_id: Optional[UUID] = None
) -> Tuple[Dict[str, str], UUID]:
    """
    Main workflow for processing a chat message with summarization.
    
    Args:
        session: Database session
        user_message: User's message
        session_id: Optional session ID (creates new if not provided)
        
    Returns:
        Tuple of (response dict, session_id)
    """
    
    # Step 1: Create new session if not provided
    if session_id is None:
        session_id = uuid.uuid4()
    
    # Step 2: Get or create conversation summary
    summary_record = get_or_create_summary(session, session_id)
    
    # Step 3: Get unsummarized messages (recent context)
    unsummarized_messages = get_unsummarized_messages(session, summary_record.id)
    
    # Step 4: Run agent with summary + unsummarized messages + new message
    ai_response = run_travel_agent(
        user_message=user_message,
        conversation_summary=summary_record.summary,
        unsummarized_messages=unsummarized_messages
    )
    
    # Step 5: Save new messages
    save_messages(session, user_message, ai_response, summary_record.id)
    
    # Step 6: Check if we should update summary
    threshold = settings["SUMMARY_UPDATE_THRESHOLD"]
    unsummarized_count = count_unsummarized_messages(session, summary_record.id)
    
    if unsummarized_count >= threshold:
        update_conversation_summary(session, summary_record)
    
    # Step 7: Parse and return response
    try:
        response_data = json.loads(ai_response)
        return {"response": response_data}, session_id
    except (json.JSONDecodeError, TypeError):
        return {"response": ai_response}, session_id
