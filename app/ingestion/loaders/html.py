"""
HTML Document Loader Module.

This module is responsible for parsing HTML web pages and documents using BeautifulSoup.
It strips away unnecessary code (such as scripts, styling, and metadata tags)
and extracts clean, human-readable text suitable for RAG chunking and embeddings.
"""

from bs4 import BeautifulSoup
import logfire


def parse_html(file_path: str) -> str:
    """
    Parses an HTML file and extracts clean text without scripts or styling tags.

    Parameters:
        file_path (str): The path to the HTML file on disk.

    Returns:
        str: The clean text content extracted from the HTML.

    Raises:
        Exception: If reading or parsing the HTML file fails.
    """
    # Start a Logfire span to track execution time and details for HTML parsing
    with logfire.span("📄 HTML Parsing", filename=file_path):
        try:
            # Step 1: Open and read the raw HTML file with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Step 2: Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")

            # Step 3: Remove noise and junk elements (JavaScript, CSS styling, meta tags, and noscript)
            for script in soup(["script", "style", "meta", "noscript"]):
                script.decompose()

            # Step 4: Extract all visible text, separating HTML blocks with newlines
            text = soup.get_text(separator="\n")

            # Step 5: Clean up whitespace (strip empty spaces and collapse multiple blank lines)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_clean = "\n".join(chunk for chunk in chunks if chunk)

            # Step 6: Return the cleaned, readable plain text
            return text_clean

        except Exception as e:
            # Log parsing errors to Logfire and re-raise
            logfire.error(f"❌ HTML Parse Failed: {e}")
            raise e
