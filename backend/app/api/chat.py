from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.vector_store_service import search_relevant_chunks
from app.services.llm_service import generate_answer


router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    filename: Optional[str] = None


@router.post("/chat")
def chat_with_documents(request: ChatRequest):
    """
    Answers questions about uploaded documents.

    Workflow:
    1. Convert question into an embedding.
    2. Search ChromaDB for the most relevant chunks.
    3. Send retrieved chunks to the LLM.
    4. Return answer and supporting sources.
    """

    results = search_relevant_chunks(
        question=request.question,
        filename=request.filename
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    answer = generate_answer(
        question=request.question,
        context_chunks=documents
    )

    sources = []

    for metadata, distance in zip(metadatas, distances):
        sources.append({
            "filename": metadata["filename"],
            "chunk_index": metadata["chunk_index"],
            "distance": round(distance, 4)
        })

    return {
        "question": request.question,
        "answer": answer,
        "source_count": len(sources),
        "sources": sources
    }