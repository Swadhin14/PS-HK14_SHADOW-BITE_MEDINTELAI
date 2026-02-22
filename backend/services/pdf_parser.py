import pdfplumber
import os


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text from a PDF file.
    Returns extracted text as a single string.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError("PDF file not found")

    extracted_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

    return extracted_text.strip()