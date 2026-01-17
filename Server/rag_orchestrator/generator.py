from typing import List
import os
from openai import OpenAI

from prompts.qa_system_prompt import SYSTEM_PROMPT


class AnswerGenerator:
    """
    Generates grounded answers using retrieved context and an LLM.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")

    def build_prompt(self, context_chunks: List[str], question: str) -> str:
        context = "\n\n".join(context_chunks)

        return f"""
CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    def generate_answer(self, context_chunks: List[str], question: str) -> str:
        # 🔒 Guardrail 1: no context → safe failure
        if not context_chunks:
            return "I don't know based on the provided documents."

        user_prompt = self.build_prompt(context_chunks, question)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,        # 🔒 Low hallucination
            max_tokens=300,         # 🔒 Cost control
        )

        return response.choices[0].message.content.strip()


