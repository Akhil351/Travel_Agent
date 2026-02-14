# 📁 models/psql.py
# SQLAlchemy models for PostgreSQL database

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

# ------------------------------------------------------------------
# 🏗️ Base model
# ------------------------------------------------------------------

Base = declarative_base()


# ------------------------------------------------------------------
# 💬 Messages Table
# ------------------------------------------------------------------

class Message(Base):
    """
    Stores individual user and AI messages.
    """
    
    __tablename__ = "messages"
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    conversation_summary_id = Column(
        Integer,
        nullable=False
    )
    
    role = Column(String(20), nullable=False)
    
    content = Column(Text, nullable=False)
    
    is_summarized = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


# ------------------------------------------------------------------
# 📝 Conversation Summary Table
# ------------------------------------------------------------------

class ConversationSummary(Base):
    """
    Stores rolling summary of conversation history.
    Updated periodically to compress old messages.
    """
    
    __tablename__ = "conversation_summaries"
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    session_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid.uuid4
    )
    
    summary = Column(
        Text,
        nullable=False,
        default="",
        comment="Rolling summary of conversation history"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
