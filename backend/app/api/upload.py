from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from botocore.exceptions import ClientError

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.services.vector_store_service import store_document_chunks
from app.services.s3_service import upload_file_to_s3


# Router groups all upload-related endpoints together.
router = APIRouter()


# Local folder used while processing uploaded PDFs.
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Receives a PDF file, saves it locally for processing,
    uploads the original document to AWS S3,
    extracts and chunks the text,
    and stores searchable embeddings in ChromaDB.
    """

    # Reject files that are not PDFs.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Build the temporary/local destination path.
    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded PDF locally.
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Define where the original PDF will live inside S3.
    s3_object_key = f"documents/{file.filename}"

    # Upload the original PDF to AWS S3.
    try:
        upload_file_to_s3(
            file_path=str(file_path),
            object_name=s3_object_key
        )
    except ClientError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to upload document to AWS S3: {str(error)}"
        )

    # Extract readable text from the locally saved PDF.
    extracted_text = extract_text_from_pdf(str(file_path))

    # Split extracted text into smaller searchable chunks.
    chunks = chunk_text(extracted_text)

    # Generate embeddings and store chunks in ChromaDB.
    stored_chunk_count = store_document_chunks(
        file.filename,
        chunks
    )

    return {
        "message": (
            "File uploaded to AWS S3, text extracted, "
            "chunked, and indexed successfully"
        ),
        "filename": file.filename,

        # Location of the original document inside S3.
        "s3_object_key": s3_object_key,

        # Total amount of text extracted from the PDF.
        "character_count": len(extracted_text),

        # Number of chunks created.
        "chunk_count": len(chunks),

        # Number of chunks stored in ChromaDB.
        "stored_chunk_count": stored_chunk_count,

        # First 500 characters of extracted text.
        "text_preview": extracted_text[:500],

        # Preview of the first chunk.
        "first_chunk_preview": chunks[0][:500] if chunks else ""
    }