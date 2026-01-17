import hashlib
from ingestion.models import Document
import uuid
import pdfplumber
from rag_orchestrator.chunkpdf import FixedSizeChunker
from rag_orchestrator.chunkpdf import FixedSizeChunker
from rag_orchestrator.embedder import OpenAIEmbedder
from rag_orchestrator.vector_store import QdrantVectorStore



def generate_checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ingest_text(source_name: str, text: str) -> Document:
    checksum = generate_checksum(text)

    document = Document.objects.create(
        source_type="text",
        source_name=source_name,
        raw_text=text,
        checksum=checksum,
        ingestion_status="INGESTED",
    )

    return document

def ingest_pdf_in_memory(file_obj):
    document_id = str(uuid.uuid4())
    extracted_text = []

    # 1️⃣ Extract text
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {str(e)}")

    full_text = "\n".join(extracted_text).strip()

    if not full_text:
        raise RuntimeError("No extractable text found in PDF")

    # 2️⃣ Chunk text
    chunker = FixedSizeChunker(
        chunk_size=500,
        overlap=50,
        model_name="gpt-4.1-mini",
    )

    chunks = chunker.chunk_text(
        document_id=document_id,
        text=full_text,
    )

    # 3️⃣ Embed chunks using OpenAI (REAL)
    embedder = OpenAIEmbedder()

    texts = [chunk.text for chunk in chunks]
    embeddings = embedder.embed_texts(texts)

    # 🔒 HARD GUARD — keep this forever
    assert len(embeddings[0]) == 1536, "❌ OpenAI embeddings NOT being used"

    # 4️⃣ Store in Qdrant
    store = QdrantVectorStore(
        collection_name="documents",
        vector_size=len(embeddings[0]),
    )
    store.upsert_chunks(chunks, embeddings)

    return {
        "document_id": document_id,
        "status": "INGESTED",
        "text_length": len(full_text),
        "chunk_count": len(chunks),
        "embedding_dim": len(embeddings[0]),  # temporary for verification
    }
