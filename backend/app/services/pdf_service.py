# Service responsible for reading PDF files and extracting text from them.

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads a PDF file from disk and returns all extracted text.
    """

    reader = PdfReader(file_path)
    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages)