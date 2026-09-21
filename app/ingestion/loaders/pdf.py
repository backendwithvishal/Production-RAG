"""
PDF Document Loader Module.

This module is responsible for extracting text from PDF documents.
It first attempts to extract text quickly using 'pypdf'. If any pages are blank
(e.g., scanned or complex layout pages), it falls back to 'pdfplumber' for those specific pages.
"""

import logfire
from pypdf import PdfReader


def parse_pdf(file_path: str) -> str:
    """
    Extract readable text from a PDF file.

    Parameters:
        file_path (str): The path to the PDF file on disk.

    Returns:
        str: The full combined text extracted from all pages of the PDF.

    Raises:
        Exception: If reading or parsing the PDF fails completely.
    """
    # Start a Logfire observability span to track and monitor the PDF parsing process
    with logfire.span("PDF Parsing (local)", filename=file_path):
        try:
            # Step 1: Open and read the PDF file using pypdf
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            logfire.info(f"PDF has {total_pages} pages.")

            # List to store the extracted text from each page
            text_parts: list[str] = []
            # List to keep track of page numbers that returned empty/blank text
            blank_pages: list[int] = []

            # Step 2: Loop through each page in the PDF and extract its text
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    # If text was found, add it to our list of text parts
                    text_parts.append(text)
                else:
                    # If no text was found on this page, mark the page number (1-indexed) for fallback parsing
                    blank_pages.append(i + 1)

            # Step 3: Fallback Mechanism - If any pages were blank, retry them with pdfplumber
            if blank_pages:
                logfire.info(f"pypdf returned blank on pages {blank_pages} — retrying with pdfplumber.")
                try:
                    import pdfplumber

                    # Open the PDF using pdfplumber to attempt a deeper extraction
                    with pdfplumber.open(file_path) as pdf:
                        for page_num in blank_pages:
                            # Access the specific blank page (convert 1-indexed to 0-indexed)
                            page = pdf.pages[page_num - 1]
                            fallback_text = page.extract_text() or ""
                            if fallback_text.strip():
                                text_parts.append(fallback_text)
                except Exception as plumber_err:
                    # If fallback fails, log a warning and proceed with the text we already have
                    logfire.warning(f"pdfplumber fallback failed: {plumber_err}")

            # Step 4: Join all extracted text parts into one single string separated by newlines
            full_text = "\n".join(text_parts)

            # Step 5: Check if any text was extracted at all
            if not full_text.strip():
                logfire.warning(f"No text extracted from {file_path}. File may be fully image-based.")
            else:
                logfire.info(f"Extracted {len(full_text)} characters from {file_path}.")

            # Return the extracted text
            return full_text

        except Exception as e:
            # Log the error details with Logfire and re-raise the exception
            logfire.error(f"PDF Parse Failed for {file_path}: {e}")
            raise
