from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from rag_orchestrator.chunks import Chunk


class QdrantVectorStore:
    def __init__(
        self,
        collection_name: str,
        vector_size: int,
        host: str = "qdrant",
        port: int = 6333,
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)

        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int):
        collections = self.client.get_collections().collections
        names = [c.name for c in collections]

        if self.collection_name not in names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_chunks(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]],
    ):
        points = []

        for chunk, vector in zip(chunks, embeddings):
            points.append(
                PointStruct(
                    id=chunk.chunk_id,
                    vector=vector,
                    payload={
                        "document_id": chunk.document_id,
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_vector: List[float], limit: int = 5):
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )
