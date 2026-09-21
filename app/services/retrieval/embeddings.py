"""
Embeddings and Retrieval Service.

This module handles:
1. Loading embedding models (e.g., HuggingFace sentence-transformers).
2. Generating vector embeddings for document chunks and user search queries.
3. Interacting with the Qdrant vector database for semantic similarity search and retrieval.
"""

# Placeholder for embedding model initialization and vector search functions

from sentence_transformers import SentenceTransformer

import time

import logfire

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import settings

# HuggingFace embedding model name from the application settings.
HUGGINGFACE_MODEL = settings.huggingface_model

# Number of texts processed in one batch.
BATCH_SIZE = 100

# Stores the HuggingFace vector size.
_HUGGINGFACE_DIMENSIONS = None

# Vector size used by the fallback model.
_FALLBACK_DIMENSIONS = 384

# Stores the currently active embedding model.
_active_model = None

# Stores which embedding model is currently active.
_model_type: str | None = None  # "huggingface" or "fallback"

def _probe_huggingface():
    """Try one embed call to check if HuggingFace is reachable."""
    try:
        # Create the HuggingFace embedding model.
        model = HuggingFaceEmbeddings(
            model="model_name",
            huggingfaceapi_key=settings.huggingface_api_key
        )

        # Make a small test request to check the model.
        model.embed_query("probe")

        logfire.info("HuggingFace embedding model is reachable")
        return model

    except Exception as e:
        # Use the local fallback model if HuggingFace is not available.
        logfire.warning(
            f"Huggingface probe failed: {e}. "
            "Will use sentence-transformers fallback."
        )
        return None

def _load_fallback():
    """Load the fallback embedding model."""
    
    # Import the model used for local embeddings.
    from sentence_transformers import SentenceTransformer

    logfire.info("Loading fallback sentence-transformers model.")

    # Load the local fallback model.
    return SentenceTransformer("all-MiniLM-L6-v2")

def _init():
    """Initialize the active embedding model."""
    
    global _active_model, _model_type

    # Do not initialize the model again if it is already loaded.
    if _active_model is not None:
        return

    # Try to use the HuggingFace embedding model first.
    HuggingFaceEmbeddings = _probe_huggingface()

    if HuggingFaceEmbeddings:
        # Use HuggingFace when it is available.
        _active_model = HuggingFaceEmbeddings
        _model_type = "huggingface"

    else:
        # Use the local model when HuggingFace is not available.
        _active_model = _load_fallback()
        _model_type = "fallback"

    return

def get_embedding_dim() -> int:
    """Return the vector dimension for the active model."""
    
    # Make sure the embedding model is initialized.
    _init()

    # Return the dimension based on the active model.
    return (
        _HUGGINGFACE_DIMENSIONS
        if _model_type == 'huggingface'
        else _FALLBACK_DIMENSIONS
    )

def _embed_batch(batch: list[str]) -> list[list[float]]:
    """Create embeddings for a batch of texts."""
    
    # Use HuggingFace embeddings when HuggingFace is active.
    if _model_type == "HuggingFaceEmbeddings":

        # Try the request up to four times.
        for attempt in range(4):
            try:
                # Create embeddings for all texts in the batch.
                return _active_model.embed_documents(batch)

            except Exception as e:
                # Convert the error to lowercase for easier checking.
                err = str(e).lower()

                # Check if the error looks like a rate limit error.
                is_rate_limit = any(
                    x in err
                    for x in ("429", "rate", "quota", "resource_exhausted")
                )

                if is_rate_limit and attempt < 3:
                    # Wait longer after each failed attempt.
                    wait = 2 ** attempt

                    logfire.warning(
                        f"HuggingFace rate limit hit — retrying in {wait}s "
                        f"(attempt {attempt + 1}/4)."
                    )

                    time.sleep(wait)

                else:
                    # Log the error and stop when the request cannot be retried.
                    logfire.error(f"HuggingFace embedding failed: {e}")
                    raise

        # Raise an error if all retry attempts fail.
        raise RuntimeError(
            "HuggingFace rate limit persisted after 4 attempts."
        )

    else:
        # Use the local fallback model for batch embeddings.
        return _active_model.encode(
            batch,
            show_progress_bar=False
        ).tolist()

def _embed_query(query: str) -> list[list[float]]:
    # Make sure the embedding model is initialized.
    _init()

    # Use HuggingFace for the query when it is active.
    if _model_type == "HuggingFaceEmbeddings":
        return _active_model.embed_query(query)

    # Otherwise, create the query embedding with the fallback model.
    return _active_model.encode([query])[0].tolist()

def embed_texts(texts: list[str]) -> list[list[float]]:

    # Make sure the embedding model is initialized.
    _init()

    # Store embeddings from all batches.
    all_embeddings: list[list[float]] = []

    # Process the texts in batches.
    for i in range(0, len(texts), BATCH_SIZE):

        # Get the current batch of texts.
        batch = texts[i:i + BATCH_SIZE]

        # Track each embedding batch in Logfire.
        with logfire.span(
            "Embedding batch",
            model=_model_type,
            start=i,
            size=len(batch)
        ):
            # Create embeddings and add them to the final list.
            all_embeddings.extend(_embed_batch(batch))

    # Return embeddings for all input texts.
    return all_embeddings