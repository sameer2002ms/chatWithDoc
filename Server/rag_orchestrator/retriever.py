from typing import List

from rag_orchestrator.embedder import Embedder
from rag_orchestrator.vector_store import QdrantVectorStore


class Retriever:
    """
    Retrieves top-k relevant chunks from vector store.
    """

    def __init__(
        self,
        embedder: Embedder,
        vector_store: QdrantVectorStore,
        top_k: int = 5,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str) -> List[str]:
        # 1. Embed the query
        query_vector = self.embedder.embed_texts([query])[0]

        # 2. Search vector DB
        results = self.vector_store.search(
            query_vector=query_vector,
            limit=self.top_k,
        )

        # 3. Extract chunk texts
        return [hit.payload["text"] for hit in results]



