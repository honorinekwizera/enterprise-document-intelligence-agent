# Service responsible for creating embeddings using OpenAI.
# An embedding turns text into a numerical vector used for semantic search.

import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_embedding(text: str) -> List[float]:
    """
    Converts one text string into one embedding vector.
    Used for user questions.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def create_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Converts multiple text chunks into embedding vectors.
    Used when storing uploaded document chunks.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [item.embedding for item in response.data]