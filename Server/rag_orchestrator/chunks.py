from dataclasses import dataclass


@dataclass
class Chunk:
    """
    Logical chunk used for embedding and retrieval.
    Not stored in PostgreSQL.
    """

    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    start_token: int
    end_token: int
