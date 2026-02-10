# llms/openai.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.core import settings


def get_openai_model():
    """
    Create and return an OpenAI chat model instance using ChatOpenAI.

    This function provides a direct OpenAI provider binding and is
    well-suited for learning, experimentation, and small to
    medium-sized projects.
    """
    return ChatOpenAI(
        model="gpt-5-mini",
        temperature=0,
        api_key=settings["OPENAI_API_KEY"]
    )


def get_openai_embedding_model():
    """
    Returns an OpenAI embedding model.
    Used for converting text into vectors in RAG.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings["OPENAI_API_KEY"]
    )
