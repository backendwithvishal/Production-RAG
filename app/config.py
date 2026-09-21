"""
Application Configuration Module.

This file loads environment variables from a .env file and sets up
configuration settings used across the entire application (e.g., API keys,
vector database connection details, and LLM model names).
"""

import os
from dotenv import load_dotenv

# Load all environment variables from the local .env file into the system environment
load_dotenv()


class Settings:
    """
    Settings class to hold and provide access to all application configuration values.
    Values are fetched from environment variables.
    """

    # Hugging Face API token: Used for authenticating with Hugging Face Hub (e.g., embeddings or models)
    HUGGINGFACEHUB_API_TOKEN: str = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

    # Qdrant Vector Database API key: Used for authenticating with the hosted Qdrant cluster
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Qdrant cluster endpoint URL: The address where the Qdrant vector database is hosted
    QDRANT_URL: str = os.getenv("QDRANT_CLUSTER_ENDPOINT", "")

    # Qdrant collection name: The name of the collection where vector embeddings and document chunks are stored
    QDRANT_COLLECTION: str = "Production_RAG"

    # Groq API key: Primary API key used to authenticate and make requests to Groq LLM services
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Groq Model: The name of the primary Large Language Model used for reasoning and generation
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Groq Fallback API key: Secondary API key used if the primary key runs out of quota or fails
    GROQ_FALLBACK_API_KEY: str = os.getenv("GROQ_FALLBACK_API_KEY", "")


# Create a single shared settings instance to be imported and used across the entire project
settings = Settings()