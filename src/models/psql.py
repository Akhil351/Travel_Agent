# 📁 models/psql.py
# SQLAlchemy models for PostgreSQL database

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

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
    
    role = Column(String(20), nullable=False)
    
    content = Column(Text, nullable=False)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
