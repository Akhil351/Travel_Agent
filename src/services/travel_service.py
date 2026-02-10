# 📁 services/travel_service.py
# Service layer for managing messages

from typing import List, Dict
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from src.models.psql import Message
from src.agents import build_travel_agent


# ------------------------------------------------------------------
# 🚀 Lazy Agent Initialization
# ------------------------------------------------------------------

# Agent will be compiled on first use (lazy loading)
_TRAVEL_AGENT = None


def get_travel_agent():
    """Get or create the travel agent (lazy initialization)."""
    global _TRAVEL_AGENT
    if _TRAVEL_AGENT is None:
        _TRAVEL_AGENT = build_travel_agent()
    return _TRAVEL_AGENT


# ------------------------------------------------------------------
# 💬 Message Management
# ------------------------------------------------------------------

def save_messages(session: Session, user_message: str, ai_message: str) -> None:
    """
    Save both user and AI messages to the database.
    
    Args:
        session: Database session
        user_message: User's message content
        ai_message: AI's response content
    """
    # Create user message
    user_msg = Message(
        role="user",
        content=user_message
    )
    
    # Create AI message
    ai_msg = Message(
        role="ai",
        content=ai_message
    )
    
    session.add(user_msg)
    session.add(ai_msg)
    session.commit()


def get_all_messages(session: Session) -> List[Dict[str, str]]:
    """
    Get all messages from the database.
    
    Args:
        session: Database session
        
    Returns:
        List of message dictionaries with 'role' and 'content'
    """
    messages = session.query(Message).order_by(Message.created_at.asc()).all()
    
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]




# ------------------------------------------------------------------
# 🤖 Agent Runner
# ------------------------------------------------------------------

def run_travel_agent(user_message: str, previous_messages: List = None) -> str:
    """
    Run the travel agent with optional conversation history.
    
    Args:
        user_message: Current user message
        previous_messages: Optional list of previous LangChain message objects
        
    Returns:
        AI response as string
    """
    # Build initial messages
    messages = []
    
    # Add previous conversation history if exists
    if previous_messages:
        messages.extend(previous_messages)
    
    # Add current user message
    messages.append(HumanMessage(content=user_message))
    
    # Initialize agent state
    initial_state = {"messages": messages}
    
    # Get or create agent (lazy initialization)
    agent = get_travel_agent()
    
    # Invoke the agent
    result = agent.invoke(initial_state)
    
    # Extract final AI response
    final_message = result["messages"][-1]
    
    return final_message.content


# ------------------------------------------------------------------
# 🚀 Main Workflow
# ------------------------------------------------------------------

def process_chat_message(session: Session, user_message: str) -> Dict[str, str]:
    """
    Main workflow for processing a chat message.
    
    Args:
        session: Database session
        user_message: User's message
        
    Returns:
        Dictionary with 'response'
    """
    
    # Step 1: Get all previous messages from database
    previous_messages_dict = get_all_messages(session)
    
    # Step 2: Convert to LangChain message objects
    previous_messages = []
    if previous_messages_dict:
        for msg in previous_messages_dict:
            if msg["role"] == "user":
                previous_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                previous_messages.append(AIMessage(content=msg["content"]))
    
    # Step 3: Run agent with previous messages
    ai_response = run_travel_agent(
        user_message=user_message,
        previous_messages=previous_messages if previous_messages else None
    )
    
    # Step 4: Save messages
    save_messages(session, user_message, ai_response)
    
    # Step 5: Return response
    return {
        "response": ai_response
    }
