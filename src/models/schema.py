from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# -------------------- Flights Models --------------------

class FlightsInput(BaseModel):
    """Input parameters for Google Flights search via SerpAPI."""

    departure_airport: str = Field(
        ...,
        description="Departure airport IATA code (e.g., DEL, BOM)"
    )
    arrival_airport: str = Field(
        ...,
        description="Arrival airport IATA code (e.g., AMS, JFK)"
    )
    outbound_date: str = Field(
        ...,
        description="Outbound date in YYYY-MM-DD format (e.g., 2024-10-01)"
    )
    return_date: str = Field(
        ...,
        description="Return date in YYYY-MM-DD format (e.g., 2024-10-07)"
    )
    adults: int = Field(
        ...,
        description="Number of adult passengers"
    )
    children: int = Field(
        ...,
        description="Number of child passengers"
    )
    infants_in_seat: int = Field(
        ...,
        description="Number of infants with a reserved seat"
    )
    infants_on_lap: int = Field(
        ...,
        description="Number of infants traveling on an adult's lap"
    )


class FlightsInputSchema(BaseModel):
    """Wrapper schema required for LangChain tool invocation."""
    params: FlightsInput


# -------------------- Hotels Models --------------------

class HotelsInput(BaseModel):
    """Input parameters for Google Hotels search via SerpAPI."""

    q: str = Field(
        ...,
        description="City or location to search hotels (e.g., Bengaluru, Goa)"
    )
    check_in_date: str = Field(
        ...,
        description="Check-in date in YYYY-MM-DD format (e.g., 2026-03-10)"
    )
    check_out_date: str = Field(
        ...,
        description="Check-out date in YYYY-MM-DD format (e.g., 2026-03-12)"
    )
    adults: int = Field(
        ...,
        description="Number of adult guests"
    )
    children: int = Field(
        ...,
        description="Number of child guests"
    )
    rooms: int = Field(
        ...,
        description="Number of rooms required"
    )
    sort_by: int = Field(
        ...,
        description="Sort order (e.g., 8 = highest rating)"
    )
    hotel_class: str = Field(
        ...,
        description="Hotel star class (e.g., 3, 4, 5)"
    )


class HotelsInputSchema(BaseModel):
    """Wrapper schema required for LangChain tool invocation."""
    params: HotelsInput


# -------------------- API Request/Response Models --------------------

class ChatRequest(BaseModel):
    """Request model for chat message."""
    message: str
    session_id: Optional[UUID] = Field(
        None,
        description="Session ID for conversation. If not provided, a new session will be created."
    )


class ChatResponse(BaseModel):
    """Response model for chat message."""
    response: str | dict
    session_id: UUID = Field(
        ...,
        description="Session ID for this conversation"
    )


class MessageHistoryResponse(BaseModel):
    """Response model for message history."""
    messages: list
