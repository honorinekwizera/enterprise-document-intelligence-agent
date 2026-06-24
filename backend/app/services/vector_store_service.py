# Service responsible for storing document chunks in ChromaDB.
# ChromaDB is our local vector database for semantic search.

from typing import List
import uuid

import chromadb

from app.services.embedding_service import create_embeddings
from app.services.embedding_service import create_embedding, create_embeddings

# Creates a persistent local ChromaDB database folder.
# This folder is ignored by Git because it is runtime data.
chroma_client = chromadb.PersistentClient(path="chroma_db")


# A collection is similar to a table/index for related chunks.
document_collection = chroma_client.get_or_create_collection(
    name="document_chunks"
)

def search_relevant_chunks(
    question: str,
    top_k: int = 5,
    filename: str = None
):
    """
    Searches ChromaDB for chunks most relevant
    to the user's question.
    """

    question_embedding = create_embedding(question)

    query_args = {
        "query_embeddings": [question_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    if filename:
        query_args["where"] = {
            "filename": filename
        }

    results = document_collection.query(**query_args)

    return results

def store_document_chunks(filename: str, chunks: List[str]) -> int:
    """
    Stores document chunks in ChromaDB with metadata.
    """

    if not chunks:
        return 0

    # One unique document ID per upload prevents duplicate Chroma IDs.
    document_id = str(uuid.uuid4())

    ids = []
    metadatas = []

    for index, _chunk in enumerate(chunks):
        ids.append(f"{document_id}-chunk-{index}")
        metadatas.append({
            "document_id": document_id,
            "filename": filename,
            "chunk_index": index
        })

    embeddings = create_embeddings(chunks)

    document_collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)
def get_uploaded_documents():
    """
    Returns unique filenames stored in ChromaDB.
    """

    results = document_collection.get(
        include=["metadatas"]
    )

    filenames = set()

    for metadata in results["metadatas"]:
        if metadata and "filename" in metadata:
            filenames.add(metadata["filename"])

    return sorted(list(filenames))
def get_database_stats():
    """
    Returns basic ChromaDB statistics.
    """

    results = document_collection.get(
        include=["metadatas"]
    )

    filenames = set()

    for metadata in results["metadatas"]:
        filenames.add(metadata["filename"])

    return {
        "document_count": len(filenames),
        "chunk_count": len(results["ids"]),
        "collection_name": document_collection.name
    }