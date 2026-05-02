# Travel Agent - AI-Powered Travel Assistant

An intelligent travel assistant powered by LangChain, LangGraph, and OpenAI that helps users search for flights and hotels with natural conversation. Features include real-time search via SerpAPI, conversation memory with intelligent summarization, and structured JSON responses.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [AI Agent Architecture](#ai-agent-architecture)
- [Conversation Memory System](#conversation-memory-system)
- [Database Schema](#database-schema)
- [Usage Examples](#usage-examples)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

Travel Agent is an AI-powered conversational assistant that simplifies travel planning by allowing users to search for flights and hotels through natural language conversations. The system leverages advanced language models, real-time search capabilities, and intelligent conversation management to provide a seamless travel booking experience.

### Key Capabilities

- **Natural Language Understanding**: Communicate in plain English to search for travel options
- **Real-time Flight Search**: Integration with Google Flights via SerpAPI
- **Real-time Hotel Search**: Integration with Google Hotels via SerpAPI
- **Conversation Memory**: Maintains context across multiple interactions
- **Intelligent Summarization**: Automatically compresses long conversations for efficient memory management
- **Structured Responses**: Returns clean, parsed JSON data for easy frontend integration
- **Session Management**: Supports multiple concurrent user sessions

## Features

### Core Features

- **Multi-tool AI Agent**: LangGraph-based agent with flight and hotel search tools
- **Conversational Interface**: Natural language processing for travel queries
- **Session Management**: UUID-based session tracking for conversation continuity
- **Conversation Summarization**: Automatic compression of conversation history
- **PostgreSQL Storage**: Persistent message and summary storage
- **Structured JSON Responses**: Clean, parsed data ready for frontend consumption

### AI Agent Features

- **Tool Binding**: OpenAI function calling for structured tool invocation
- **State Management**: LangGraph state graph for complex conversation flows
- **Context Awareness**: Uses conversation summaries for long-term memory
- **Smart Routing**: Conditional edges for intelligent decision-making
- **Error Handling**: Graceful error handling with custom exceptions

### Search Features

#### Flight Search
- Departure and arrival airports (IATA codes)
- Outbound and return dates
- Passenger details (adults, children, infants)
- Currency and location customization
- Real-time pricing and availability

#### Hotel Search
- Location-based search
- Check-in and check-out dates
- Guest details (adults, children)
- Room requirements
- Hotel class filtering (3-star, 4-star, 5-star)
- Sorting options (highest rated, etc.)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
│           (Frontend/API Consumer - not included)            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/JSON
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI SERVER                            │
│                  (Port 8080)                                │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                       │  │
│  │  • POST /backoffice/travel/chat                      │  │
│  │  • GET  /backoffice/travel/history/{session_id}     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  SERVICE LAYER                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Travel Service                                     │   │
│  │  • Message Processing                               │   │
│  │  • Session Management                               │   │
│  │  • Summary Management                               │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────┬─────────────────────────────┬───────────────────┘
            │                             │
            │                             │
            ▼                             ▼
┌───────────────────────────┐   ┌─────────────────────────────┐
│    AI AGENT LAYER         │   │   DATABASE LAYER            │
│                           │   │                             │
│  ┌──────────────────────┐ │   │  ┌────────────────────────┐ │
│  │  LangGraph Agent     │ │   │  │  PostgreSQL            │ │
│  │  • State Management  │ │   │  │  • Messages Table      │ │
│  │  • Tool Orchestration│ │   │  │  • Summaries Table     │ │
│  │  • Decision Making   │ │   │  └────────────────────────┘ │
│  └──────────────────────┘ │   │                             │
│           │                │   └─────────────────────────────┘
│           ▼                │
│  ┌──────────────────────┐ │
│  │  Tools               │ │
│  │  • flights_finder    │ │
│  │  • hotels_finder     │ │
│  └──────────────────────┘ │
│           │                │
│           ▼                │
│  ┌──────────────────────┐ │
│  │  SerpAPI Client      │ │
│  │  • Google Flights    │ │
│  │  • Google Hotels     │ │
│  └──────────────────────┘ │
└───────────────────────────┘
            │
            ▼
┌───────────────────────────┐   ┌─────────────────────────────┐
│   OPENAI API              │   │   SERPAPI                   │
│   • GPT Models            │   │   • Google Flights Engine   │
│   • Function Calling      │   │   • Google Hotels Engine    │
└───────────────────────────┘   └─────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              SUMMARIZATION AGENT                            │
│                                                             │
│  Triggered every N messages to compress conversation        │
│  history into concise summaries                             │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │  • Preserves travel details and preferences        │    │
│  │  • Removes redundant information                   │    │
│  │  • Maintains context for future interactions       │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Backend Framework
- **FastAPI**: Modern, high-performance web framework
- **Python**: 3.13+
- **Uvicorn**: ASGI server for production

### AI/LLM Stack
- **LangChain**: 1.2.9+ - Framework for building LLM applications
- **LangChain OpenAI**: 1.1.7+ - OpenAI integration
- **LangGraph**: State graph framework for complex agent workflows
- **OpenAI API**: GPT models for natural language understanding

### Database
- **PostgreSQL**: Relational database for message and summary storage
- **SQLAlchemy**: 2.0.46+ - ORM for database operations
- **Psycopg2**: PostgreSQL adapter

### External APIs
- **SerpAPI**: Real-time search for Google Flights and Hotels
- **Google Search Results**: 2.4.2+ - SerpAPI Python client

### Vector Store (Optional)
- **Pinecone**: 8.0.0+ - Vector database for semantic search (configured but not actively used)

### Development Tools
- **Python-dotenv**: 1.2.1+ - Environment variable management
- **UV**: Package manager (pyproject.toml configuration)

## Project Structure

```
Travel_Agent/
├── src/
│   ├── agents/                        # AI Agent Definitions
│   │   ├── __init__.py
│   │   ├── travel_agent.py            # Main LangGraph travel agent
│   │   └── summarize_agent.py         # Conversation summarization agent
│   │
│   ├── apis/                          # API Route Handlers
│   │   └── travel_api.py              # Travel endpoints (chat, history)
│   │
│   ├── core/                          # Core Configuration
│   │   ├── __init__.py
│   │   ├── config.py                  # Environment settings
│   │   └── deps.py                    # Dependency injection
│   │
│   ├── database/                      # Database Setup
│   │   ├── __init__.py
│   │   └── db.py                      # SQLAlchemy engine creation
│   │
│   ├── exceptions/                    # Error Handling
│   │   ├── __init__.py
│   │   ├── exception.py               # Custom exceptions
│   │   └── global_exception_handler.py # Exception handlers
│   │
│   ├── llms/                          # LLM Factory
│   │   ├── __init__.py
│   │   └── factory.py                 # OpenAI model initialization
│   │
│   ├── models/                        # Data Models
│   │   ├── __init__.py
│   │   ├── schema.py                  # Pydantic models (API schemas)
│   │   └── psql.py                    # SQLAlchemy models (Database)
│   │
│   ├── services/                      # Business Logic
│   │   ├── __init__.py
│   │   └── travel_service.py          # Message and summary management
│   │
│   ├── tools/                         # LangChain Tools
│   │   ├── __init__.py
│   │   ├── tool.py                    # Flight and hotel search tools
│   │   └── parsers.py                 # Response parsing utilities
│   │
│   ├── vectorstore/                   # Vector Store (Optional)
│   │   ├── __init__.py
│   │   └── pinecone.py                # Pinecone configuration
│   │
│   └── main.py                        # Application entry point
│
├── pyproject.toml                     # Project dependencies (UV)
├── uv.lock                            # Dependency lock file
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore patterns
└── README.md                          # This file
```

## Prerequisites

### Required Software
- **Python**: 3.13 or higher
- **PostgreSQL**: 14+ (for message storage)
- **UV Package Manager**: For dependency management

### API Keys Required
1. **OpenAI API Key**: For GPT models
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   
2. **SerpAPI Key**: For flight and hotel searches
   - Sign up at [SerpAPI](https://serpapi.com/)
   
3. **Pinecone API Key** (Optional): If using vector storage
   - Sign up at [Pinecone](https://www.pinecone.io/)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Travel_Agent
```

### 2. Set Up PostgreSQL Database

```bash
# Create database
createdb travel_agent

# Or using psql
psql -U postgres
CREATE DATABASE travel_agent;
\q
```

### 3. Install UV Package Manager

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 4. Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

### 5. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` file with your credentials:

```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here
SERPAPI_API_KEY=your-serpapi-key-here
PINECONE_API_KEY=your-pinecone-key-here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/travel_agent
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800

# Server Configuration
SERVER_HOST=localhost
SERVER_PORT=8080
SERVER_DEBUG=true

# Application Configuration
APP_NAME=Travel Agent
APP_VERSION=0.1.0
APP_DESCRIPTION=AI-powered Travel Agent for flights and hotels

# Agent Configuration
SUMMARY_UPDATE_THRESHOLD=20
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | - | Yes |
| `SERPAPI_API_KEY` | SerpAPI key for search | - | Yes |
| `PINECONE_API_KEY` | Pinecone API key (optional) | - | No |
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `DB_POOL_SIZE` | Database connection pool size | 5 | No |
| `DB_MAX_OVERFLOW` | Max overflow connections | 10 | No |
| `DB_POOL_TIMEOUT` | Connection timeout (seconds) | 30 | No |
| `DB_POOL_RECYCLE` | Connection recycle time (seconds) | 1800 | No |
| `SERVER_HOST` | Server host | localhost | No |
| `SERVER_PORT` | Server port | 8080 | No |
| `SERVER_DEBUG` | Debug mode | false | No |
| `SUMMARY_UPDATE_THRESHOLD` | Messages before summarization | 20 | No |

### Database Configuration

The application automatically creates tables on startup. No manual migration needed.

**Tables Created**:
- `conversation_summaries`: Stores conversation summaries
- `messages`: Stores individual messages

### Summary Update Threshold

Controls when conversation summarization occurs:
- **Value**: Number of unsummarized messages before triggering summarization
- **Default**: 20 messages
- **Purpose**: Balances memory efficiency with API call costs

## Running the Application

### Development Mode

```bash
# Using Python directly
python src/main.py

# Or using uvicorn
uvicorn src.main:app --reload --host localhost --port 8080
```

### Production Mode

```bash
# Using uvicorn with production settings
uvicorn src.main:app --host 0.0.0.0 --port 8080 --workers 4

# Or using gunicorn with uvicorn workers
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

### Access the Application

- **API Base URL**: http://localhost:8080/backoffice
- **Health Check**: http://localhost:8080/backoffice/travel/chat (POST)

### Verify Installation

```bash
# Test health endpoint
curl -X POST http://localhost:8080/backoffice/travel/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## API Endpoints

### Base Path: `/backoffice/travel`

### 1. Chat Endpoint

**POST** `/backoffice/travel/chat`

Process a user message and get AI response.

**Request Body**:
```json
{
  "message": "Find me flights from Delhi to Amsterdam on 2026-05-10 returning on 2026-05-17 for 2 adults",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Fields**:
- `message` (string, required): User's message
- `session_id` (UUID, optional): Session ID for conversation continuity. If not provided, a new session is created.

**Response**:
```json
{
  "response": {
    "response_type": "flights",
    "data": [
      {
        "airline": "Air India",
        "departure": "2026-05-10 10:30 AM",
        "arrival": "2026-05-10 3:45 PM",
        "duration": "9h 15m",
        "price": "₹45,000",
        "logo": "https://..."
      }
    ]
  },
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response Types**:

1. **Flights Response**:
```json
{
  "response_type": "flights",
  "data": [/* array of flight objects */]
}
```

2. **Hotels Response**:
```json
{
  "response_type": "hotels",
  "data": [/* array of hotel objects */]
}
```

3. **Message Response** (conversational):
```json
{
  "response_type": "message",
  "message": "I'd be happy to help you find flights. Could you please provide..."
}
```

### 2. History Endpoint

**GET** `/backoffice/travel/history/{session_id}`

Get conversation history for a specific session.

**Path Parameters**:
- `session_id` (UUID, required): Session ID

**Response**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Find flights from Delhi to Amsterdam"
    },
    {
      "role": "ai",
      "content": "{\"response_type\": \"flights\", \"data\": [...]}"
    }
  ]
}
```

## AI Agent Architecture

### LangGraph State Machine

The travel agent uses LangGraph to manage conversation flow:

```python
┌─────────────┐
│  START      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  call_llm   │ ◄─────┐
└──────┬──────┘       │
       │              │
       ▼              │
  [Decision]          │
       │              │
    Has Tools?        │
    /      \          │
  Yes       No        │
   │         │        │
   ▼         ▼        │
┌──────┐   ┌────┐    │
│ tools│──▶│END │    │
└──────┘   └────┘    │
   │                 │
   └─────────────────┘
```

**Nodes**:
1. **call_llm**: Invokes OpenAI model with tools bound
2. **tools**: Executes tool calls (flights_finder, hotels_finder)
3. **END**: Conversation completed

**Edges**:
- **Conditional**: Decides between tools or END based on LLM response
- **Static**: Always returns to call_llm after tool execution

### Agent State

```python
class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    conversation_summary: str
```

**State Fields**:
- `messages`: List of conversation messages (accumulated)
- `conversation_summary`: Compressed summary of past conversations

### System Prompt

The agent uses a structured system prompt that:
- Defines available tools (flights_finder, hotels_finder)
- Specifies response format (JSON)
- Includes conversation context when available
- Guides parameter collection

### Tool Binding

Uses OpenAI function calling to bind tools:
```python
llm = get_openai_model().bind_tools([flights_finder, hotels_finder])
```

## Conversation Memory System

### How It Works

The application uses a two-tier memory system:

1. **Short-term Memory**: Recent unsummarized messages
2. **Long-term Memory**: Compressed conversation summaries

### Memory Flow

```
New Message
    ↓
Check if session exists
    ↓
Load conversation summary (long-term)
    ↓
Load unsummarized messages (short-term)
    ↓
Send to Agent: summary + recent messages + new message
    ↓
Agent responds
    ↓
Save user message + AI response
    ↓
Check message count >= threshold?
    ↓
Yes → Trigger summarization
    ↓
Update summary
Mark messages as summarized
```

### Summarization Agent

**Trigger**: After N unsummarized messages (default: 20)

**Purpose**: Compress conversation history to:
- Save token costs
- Maintain long-term context
- Prevent context window overflow

**What It Preserves**:
- Travel destinations and locations
- Travel dates
- Passenger/guest details
- Preferences (budget, class, etc.)
- Decisions made

**What It Removes**:
- Small talk
- Redundant information
- Irrelevant details

### Summary Update Process

```python
def update_conversation_summary(session, summary_record):
    # Get unsummarized messages
    messages = get_unsummarized_messages(...)
    
    # Update summary using LLM
    new_summary = update_summary(
        current_summary=summary_record.summary,
        new_messages=messages
    )
    
    # Save and mark as summarized
    summary_record.summary = new_summary
    mark_messages_as_summarized(messages)
```

## Database Schema

### Tables

#### 1. conversation_summaries

Stores rolling summaries of conversations.

```sql
CREATE TABLE conversation_summaries (
    id SERIAL PRIMARY KEY,
    session_id UUID UNIQUE NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Fields**:
- `id`: Auto-incrementing primary key
- `session_id`: UUID for session tracking (unique)
- `summary`: Compressed conversation history
- `created_at`: Session creation timestamp
- `updated_at`: Last update timestamp

#### 2. messages

Stores individual user and AI messages.

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_summary_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    is_summarized BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Fields**:
- `id`: Auto-incrementing primary key
- `conversation_summary_id`: Foreign key to conversation_summaries
- `role`: Message role ('user' or 'ai')
- `content`: Message content
- `is_summarized`: Whether message is included in summary
- `created_at`: Message creation timestamp

### Relationships

```
conversation_summaries (1) ──── (Many) messages
```

## Usage Examples

### Example 1: Search for Flights

**Request**:
```bash
curl -X POST http://localhost:8080/backoffice/travel/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me flights from DEL to AMS on 2026-05-10 returning on 2026-05-17 for 2 adults, 0 children, 0 infants"
  }'
```

**Response**:
```json
{
  "response": {
    "response_type": "flights",
    "data": [
      {
        "airline": "Air India",
        "departure": "2026-05-10 10:30 AM",
        "arrival": "2026-05-10 3:45 PM",
        "duration": "9h 15m",
        "price": "₹45,000",
        "logo": "https://..."
      }
    ]
  },
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Example 2: Search for Hotels

**Request**:
```bash
curl -X POST http://localhost:8080/backoffice/travel/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find 5-star hotels in Goa for check-in on 2026-06-01 and check-out on 2026-06-05 for 2 adults and 1 child, 1 room",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Response**:
```json
{
  "response": {
    "response_type": "hotels",
    "data": [
      {
        "name": "Taj Exotica Resort & Spa",
        "description": "Luxury beachfront resort...",
        "rate": "₹12,000",
        "rating": "4.8",
        "check_in": "3:00 PM",
        "check_out": "12:00 PM",
        "hotel_class": "5",
        "logo": "https://..."
      }
    ]
  },
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Example 3: Conversational Interaction

**Request**:
```bash
curl -X POST http://localhost:8080/backoffice/travel/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, I want to plan a trip to Bali"
  }'
```

**Response**:
```json
{
  "response": {
    "response_type": "message",
    "message": "I'd be happy to help you plan your trip to Bali! To find the best flights, I'll need:\n- Your departure city/airport\n- Travel dates (outbound and return)\n- Number of passengers (adults, children, infants)"
  },
  "session_id": "650e8400-e29b-41d4-a716-446655440001"
}
```

### Example 4: Get Conversation History

**Request**:
```bash
curl -X GET http://localhost:8080/backoffice/travel/history/550e8400-e29b-41d4-a716-446655440000
```

**Response**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Find me flights from DEL to AMS on 2026-05-10..."
    },
    {
      "role": "ai",
      "content": "{\"response_type\": \"flights\", \"data\": [...]}"
    },
    {
      "role": "user",
      "content": "Find hotels in Amsterdam..."
    },
    {
      "role": "ai",
      "content": "{\"response_type\": \"hotels\", \"data\": [...]}"
    }
  ]
}
```

## Deployment

### Production Checklist

- [ ] Set `SERVER_DEBUG=false`
- [ ] Use strong database credentials
- [ ] Configure proper `DATABASE_URL` for production
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Use HTTPS
- [ ] Configure CORS properly
- [ ] Set rate limiting
- [ ] Use environment-specific API keys

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --no-dev

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Build and run:
```bash
docker build -t travel-agent .
docker run -p 8080:8080 --env-file .env travel-agent
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: travel_agent
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgresql://postgres:your_password@postgres:5432/travel_agent
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      SERPAPI_API_KEY: ${SERPAPI_API_KEY}
    depends_on:
      - postgres

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up -d
```

### Cloud Deployment

**Options**:
- **AWS**: ECS/Fargate + RDS PostgreSQL
- **Google Cloud**: Cloud Run + Cloud SQL
- **Azure**: App Service + Azure Database for PostgreSQL
- **Heroku**: Heroku Dynos + Heroku Postgres
- **Railway**: Railway deployment

## Troubleshooting

### Common Issues

#### 1. Database Connection Error

```
Error: could not connect to server: Connection refused
```

**Solutions**:
- Verify PostgreSQL is running: `pg_isready`
- Check `DATABASE_URL` in `.env`
- Verify database exists: `psql -l`
- Check firewall settings

#### 2. OpenAI API Error

```
Error: Incorrect API key provided
```

**Solutions**:
- Verify `OPENAI_API_KEY` in `.env`
- Check API key validity on OpenAI dashboard
- Ensure no extra spaces in API key

#### 3. SerpAPI Rate Limit

```
Error: You have reached your monthly search limit
```

**Solutions**:
- Check SerpAPI usage dashboard
- Upgrade SerpAPI plan
- Implement request caching

#### 4. Table Not Found Error

```
Error: relation "messages" does not exist
```

**Solutions**:
- Restart application (tables created on startup)
- Manually create tables using SQLAlchemy:
```python
from src.database import create_db_engine
from src.models.psql import Base
from src.core import settings

engine = create_db_engine(settings["DATABASE_URL"])
Base.metadata.create_all(bind=engine)
```

#### 5. Port Already in Use

```
Error: [Errno 48] Address already in use
```

**Solutions**:
- Change port in `.env`: `SERVER_PORT=8081`
- Kill process using port: 
  ```bash
  lsof -ti:8080 | xargs kill -9
  ```

### Debug Mode

Enable detailed logging:

```env
SERVER_DEBUG=true
```

Check logs for:
- Database queries
- API requests/responses
- Agent state transitions
- Tool invocations

## Best Practices

### Development

1. **Use Virtual Environment**: Always use UV or venv
2. **Environment Variables**: Never commit `.env` file
3. **Database Migrations**: Track schema changes
4. **Testing**: Write tests for critical paths
5. **Logging**: Use structured logging

### Production

1. **Connection Pooling**: Configure proper pool sizes
2. **Error Handling**: Implement comprehensive error handling
3. **Rate Limiting**: Protect against abuse
4. **Monitoring**: Set up health checks
5. **Backup**: Regular database backups

### AI Agent

1. **Token Management**: Monitor token usage
2. **Summarization**: Tune threshold based on usage
3. **Tool Design**: Keep tools focused and simple
4. **Prompt Engineering**: Iterate on system prompts
5. **Error Recovery**: Handle tool failures gracefully

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
uv sync

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## Future Enhancements

- [ ] Add car rental search
- [ ] Implement flight price tracking
- [ ] Add multi-city flight search
- [ ] Implement hotel amenities filtering
- [ ] Add user authentication
- [ ] Implement booking confirmation
- [ ] Add email notifications
- [ ] Create admin dashboard
- [ ] Implement A/B testing for prompts
- [ ] Add multi-language support

## License

This project is licensed under the MIT License.

## Acknowledgments

- **LangChain**: For the amazing LLM framework
- **OpenAI**: For powerful language models
- **SerpAPI**: For real-time search capabilities
- **FastAPI**: For modern Python web framework

## Support

For issues and questions:
- Create an issue on GitHub
- Email: akhil.vathaluru@gmail.com

---

**Built with ❤️ by Akhileswar**

## Appendix

### IATA Airport Codes

Common airport codes for reference:

| City | Airport | Code |
|------|---------|------|
| Delhi | Indira Gandhi International | DEL |
| Mumbai | Chhatrapati Shivaji | BOM |
| Amsterdam | Schiphol | AMS |
| New York | John F. Kennedy | JFK |
| London | Heathrow | LHR |
| Singapore | Changi | SIN |
| Dubai | International | DXB |
| Tokyo | Narita | NRT |

### Hotel Search Parameters

**sort_by values**:
- `8` = Highest rating
- `13` = Lowest price
- `2` = Most reviewed

**hotel_class values**:
- `2` = 2-star
- `3` = 3-star
- `4` = 4-star
- `5` = 5-star

### API Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (external API down) |
