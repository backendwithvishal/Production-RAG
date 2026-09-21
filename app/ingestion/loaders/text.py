"""
Plain Text Document Loader Module.

This module handles loading and reading standard plain text (.txt, .md, etc.) files.
"""

import logfire


def parse_text(file_path: str) -> str:
    """
    Reads a plain text file from disk and returns its contents as a string.

    Parameters:
        file_path (str): The path to the text file on disk.

    Returns:
        str: The full text content of the file.

    Raises:
        Exception: If reading the file fails.
    """
    # Start a Logfire span to monitor the plain text parsing process
    with logfire.span("📄 Text Parsing", filename=file_path):
        try:
            # Open the file using UTF-8 encoding (ignoring any decoding errors) and read the text
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            # Log the error if the file cannot be read and re-raise the exception
            logfire.error(f"❌ Text Parse Failed: {e}")
            raise e
