import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:

    # Hugging Face API token used for Hugging Face services
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Qdrant API key used to connect with Qdrant
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    # Qdrant cluster URL
    QDRANT_URL = os.getenv("QDRANT_CLUSTER_ENDPOINT")

    # Name of the Qdrant collection used by the application
    QDRANT_COLLECTION = "Production_RAG"

    # Groq API key used to access the Groq LLM
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Main Groq model used by the application
    GROQ_MODEL = "llama-3.3-70b-versatile"

    # Backup Groq API key used if the main key is unavailable
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")


# Create one settings object for use across the application
settings = Settings()