"""
Office Document Loader Module.

This module handles parsing Microsoft Office documents such as Word files (.docx)
and PowerPoint presentations (.pptx) using the Unstructured library.
"""

import logfire
from unstructured.partition.auto import partition


def parse_office(file_path: str) -> str:
    """
    Parses Office documents (.docx, .pptx) into plain text.

    Parameters:
        file_path (str): The path to the Office file on disk.

    Returns:
        str: The full text extracted from the Office document.

    Raises:
        Exception: If reading or partitioning the file fails.
    """
    # Start a Logfire span to monitor and log the Office document parsing step
    with logfire.span("📄 Office Document Parsing", filename=file_path):
        try:
            # Step 1: Use partition() which automatically detects document format (.docx or .pptx)
            # and extracts text elements, tables, and titles from the file
            elements = partition(filename=file_path)

            # Step 2: Combine all document elements into a single string separated by newlines
            full_text = "\n".join([str(el) for el in elements])

            # Step 3: Check whether any readable text was extracted
            if not full_text.strip():
                logfire.warning(f"⚠️ Unstructured returned empty text for {file_path}")
            else:
                logfire.info(f"✅ Successfully parsed {len(full_text)} characters")

            # Step 4: Return the combined text content
            return full_text

        except Exception as e:
            # Log any error encountered during parsing and re-raise the exception
            logfire.error(f"❌ Office Parse Failed: {e}")
            raise e
