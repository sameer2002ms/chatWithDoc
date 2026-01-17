from typing import List


class DummyAnswerGenerator:
    """
    Dummy generator used when no LLM / API key is available.
    """

    def generate_answer(self, context_chunks: List[str], question: str) -> str:
        if not context_chunks:
            return "I don't know based on the provided documents."

        # Simple deterministic behavior
        return " ".join(context_chunks)
