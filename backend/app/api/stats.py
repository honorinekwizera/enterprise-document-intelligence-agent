from fastapi import APIRouter

from app.services.vector_store_service import get_database_stats

router = APIRouter()


@router.get("/stats")
def stats():
    """
    Returns database statistics.
    """

    return get_database_stats()