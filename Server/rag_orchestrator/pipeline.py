from typing import List, Tuple

from rag_orchestrator.chunkpdf import FixedSizeChunker
from rag_orchestrator.embedder import Embedder
from rag_orchestrator.chunks import Chunk


class InMemoryRAGPipeline:
    """
    Minimal RAG preparation pipeline:
    Document text -> Chunks -> Embeddings (no storage)
    """

    def __init__(self, chunker: FixedSizeChunker, embedder: Embedder):
        self.chunker = chunker
        self.embedder = embedder

    def process_document(
        self, document_id: str, text: str
    ) -> List[Tuple[Chunk, List[float]]]:
        # 1. Chunk the document
        chunks = self.chunker.chunk_text(document_id=document_id, text=text)

        # 2. Extract chunk texts
        texts = [chunk.text for chunk in chunks]

        # 3. Embed chunks
        embeddings = self.embedder.embed_texts(texts)

        # 4. Pair chunks with embeddings
        return list(zip(chunks, embeddings))



