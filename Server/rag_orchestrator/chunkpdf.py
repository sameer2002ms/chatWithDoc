import uuid
import tiktoken
from typing import List

from rag_orchestrator.chunks import Chunk


class FixedSizeChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        model_name: str = "gpt-4.1-mini",
    ):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoder = tiktoken.encoding_for_model(model_name)

    def chunk_text(self, document_id: str, text: str) -> List[Chunk]:
        tokens = self.encoder.encode(text)

        chunks: List[Chunk] = []
        start = 0
        chunk_index = 0

        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]

            chunk_text = self.encoder.decode(chunk_tokens)

            chunk = Chunk(
                chunk_id=str(uuid.uuid4()),
                document_id=document_id,
                chunk_index=chunk_index,
                text=chunk_text,
                start_token=start,
                end_token=min(end, len(tokens)),
            )

            chunks.append(chunk)

            chunk_index += 1
            start = end - self.overlap

        return chunks




