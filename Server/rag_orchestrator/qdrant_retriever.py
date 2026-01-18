from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from rag_orchestrator.embedding.embedder import OpenAIEmbedder


class QdrantRetriever:
    def __init__(self):
        self.client = QdrantClient(host="qdrant", port=6333)
        self.embedder = OpenAIEmbedder()
        self.collection_name = "documents"

    def retrieve(
        self,
        question: str,
        document_id: str,
        top_k: int = 3,
    ) -> List[dict]:
        """
        Retrieve top-k relevant chunks for a question
        scoped to a single document.
        """

        # 1️⃣ Embed the question
        query_vector = self.embedder.embed_texts([question])[0]

        # 🔒 Guard (never remove)
        assert len(query_vector) == 1536, "Invalid embedding size"

        # 2️⃣ Filter by latest document
        doc_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        )

        # 3️⃣ Query Qdrant (NEW API)
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=doc_filter,
            limit=top_k,
        )

        # 4️⃣ Normalize results
        results = []
        for hit in response.points:
            results.append(
                {
                    "chunk_index": hit.payload.get("chunk_index"),
                    "text": hit.payload.get("text"),
                    "score": hit.score,
                }
            )

        return results
