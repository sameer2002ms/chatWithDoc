from abc import ABC, abstractmethod
from typing import List

import os
from typing import List
from openai import OpenAI


class Embedder(ABC):
    """
    Abstract base class for embedding providers.
    """

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Takes a list of texts and returns a list of embedding vectors.
        """
        pass


class OpenAIEmbedder(Embedder):
    """
    Real embedder using OpenAI embedding models.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of texts using OpenAI embeddings API.
        """

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        # OpenAI guarantees order preservation
        return [item.embedding for item in response.data]
