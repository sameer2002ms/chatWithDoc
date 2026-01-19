from abc import ABC, abstractmethod
from typing import List

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

