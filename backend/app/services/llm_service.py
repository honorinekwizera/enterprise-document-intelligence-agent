# Service responsible for generating final answers using retrieved document context.

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(question: str, context_chunks: list[str]) -> str:
    """
    Uses retrieved document chunks as context
    and asks the LLM to answer the user's question.
    """

    context = "\n\n---\n\n".join(context_chunks)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise document assistant. "
                    "Answer only using the provided context. "
                    "If the answer is not in the context, say you do not know."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    )

    return response.choices[0].message.content