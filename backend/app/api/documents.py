from fastapi import APIRouter

from app.services.vector_store_service import get_uploaded_documents

router = APIRouter()


@router.get("/documents")
def list_documents():
    """
    Returns a list of documents currently stored in ChromaDB.
    """

    return {
        "documents": get_uploaded_documents()
    }