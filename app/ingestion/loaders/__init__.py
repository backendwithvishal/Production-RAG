"""
Document Loaders Package.

This package contains modular document parsers and loaders for various file types:
- PDF (pdf.py): Extracts text from PDF files using pypdf and pdfplumber.
- Office (office.py): Extracts text from .docx and .pptx using unstructured.
- HTML (html.py): Extracts clean text from HTML web pages using BeautifulSoup.
- Text (text.py): Reads plain text files.
"""

from app.ingestion.loaders.pdf import parse_pdf
from app.ingestion.loaders.office import parse_office
from app.ingestion.loaders.html import parse_html
from app.ingestion.loaders.text import parse_text

__all__ = ["parse_pdf", "parse_office", "parse_html", "parse_text"]
