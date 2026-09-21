# Production Ready RAG System

An Enterprise Agentic Retrieval-Augmented Generation (RAG) system built with FastAPI, Qdrant Vector Database, Groq LLM (Llama 3.3), HuggingFace embeddings, and Logfire observability.

---

## 📁 Project Structure

```text
├── app/
│   ├── config.py                     # Environment variables and system configuration
│   ├── ingestion/                    # Document ingestion and loading pipeline
│   │   ├── loaders/                  # File format loaders (PDF, Office, HTML, TXT)
│   │   │   ├── pdf.py                # PDF loader using pypdf with pdfplumber fallback
│   │   │   ├── office.py             # Word (.docx) & PowerPoint (.pptx) loader using unstructured
│   │   │   ├── html.py               # HTML parser and text cleaner using BeautifulSoup
│   │   │   └── text.py               # Plain text file loader
│   │   ├── chucking/                 # Document chunking strategies
│   │   └── processor.py              # Ingestion pipeline processor
│   ├── services/                     # Business logic and retrieval services
│   │   └── retrieval/
│   │       └── embeddings.py         # Embedding generation and Qdrant retrieval
│   └── DATA/                         # Data samples (noisy and true datasets)
├── .env.example                      # Example environment variables template
├── requirements.txt                  # Python dependencies
└── README.md                         # Project overview and documentation
```

---

## 🚀 Getting Started

1. **Set up Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   - `GROQ_API_KEY`: Groq API key for Llama 3.3 LLM
   - `QDRANT_API_KEY` & `QDRANT_CLUSTER_ENDPOINT`: Qdrant vector database credentials
   - `LOGFIRE_TOKEN`: Pydantic Logfire token for observability
   - `HUGGINGFACEHUB_API_TOKEN`: HuggingFace Hub token for embeddings