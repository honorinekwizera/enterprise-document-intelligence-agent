from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.services.vector_store_service import store_document_chunks

# Router groups all upload-related endpoints together.
router = APIRouter()

# Folder where uploaded PDF files are saved.
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Receives a PDF file, saves it, extracts text,
    and returns a short preview of the extracted content.
    """

    # Reject files that are not PDFs.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Build the destination path inside the uploads folder.
    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file to disk.
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract readable text from the saved PDF.
    extracted_text = extract_text_from_pdf(str(file_path))
    # Split the extracted text into smaller searchable chunks.
    chunks = chunk_text(extracted_text)
    #calls the vector_store_service.py function for ChromaDB
    stored_chunk_count = store_document_chunks(file.filename, chunks)

    return {
    "message": "File uploaded, text extracted, and chunked successfully",
    "filename": file.filename,
    # Total amount of text extracted from the PDF
    "character_count": len(extracted_text),
    # Number of chunks created
    "chunk_count": len(chunks),
    #ChromaDb vector stored chunks
    "stored_chunk_count": stored_chunk_count,
    # First 500 characters of the extracted text
    "text_preview": extracted_text[:500],
    # Preview of the first chunk
    "first_chunk_preview": chunks[0][:500] if chunks else ""
}