"""
Embeddings and Retrieval Service.

This module handles:
1. Loading embedding models (e.g., HuggingFace sentence-transformers).
2. Generating vector embeddings for document chunks and user search queries.
3. Interacting with the Qdrant vector database for semantic similarity search and retrieval.
"""

# Placeholder for embedding model initialization and vector search functions

import time
import logfire
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

HUGGINGFACE_MODEL = settings.huggingface_model 

BATCH_SIZE = 100
_HUGGINGFACE_DIMENSIONS = 3072
_FALLBACK_DIMENSIONS = 560

