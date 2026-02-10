# vectorstore/pinecone.py

import logging
from pinecone import Pinecone
from src.core import settings

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMBEDDING_DIMENSION = 1536  # text-embedding-3-small


def get_pinecone_index(index_name: str):
    """
    Connects to Pinecone and returns an index.
    If the index does not exist, it will be created.
    """

    logger.info("Connecting to Pinecone...")
    pc = Pinecone(api_key=settings["PINECONE_API_KEY"])

    existing_indexes = pc.list_indexes().names()

    if index_name in existing_indexes:
        logger.info(f"Pinecone index '{index_name}' already exists. Reusing it.")
    else:
        logger.info(f"Pinecone index '{index_name}' not found. Creating new index...")

        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            }
        )

        logger.info(f"Pinecone index '{index_name}' created successfully.")

    logger.info(f"Connecting to Pinecone index '{index_name}'.")
    return pc.Index(index_name)