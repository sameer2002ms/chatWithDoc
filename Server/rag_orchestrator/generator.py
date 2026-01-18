from typing import List, Dict
import os
from openai import OpenAI


class GPTAnswerGenerator:
    """
    GPT-based answer generator for RAG.
    Uses retrieved chunks as grounded context.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")

    def generate(self, question: str, chunks: List[Dict]) -> Dict:
        # Build context text
        context = "\n\n".join(f"- {c['text']}" for c in chunks)

        system_prompt = (
            "You are a professional document-based assistant. "
            "Answer the question strictly using the provided document context. "
            "Do not add any external knowledge. "
            "If the answer is not present, say: "
            "'The document does not contain this information.' "
            "Answer concisely in 1–2 sentences."
        )

        user_prompt = f"""
Question:
{question}

Document Context:
{context}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,  # low hallucination
        )

        answer_text = response.choices[0].message.content.strip()

        return {
            "answer": answer_text,
            "sources": [
                {
                    "chunk_index": c["chunk_index"],
                    "text": c["text"],
                    "score": c.get("score"),
                }
                for c in chunks
            ],
        }
