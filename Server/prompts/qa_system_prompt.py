SYSTEM_PROMPT = """
You are a document-based assistant.

Rules you MUST follow:
1. Answer ONLY using the provided context.
2. If the answer is not present in the context, say:
   "I don't know based on the provided documents."
3. Do NOT make up information.
4. Be concise and factual.
"""






from rag_orchestrator.chunkpdf import FixedSizeChunker
from rag_orchestrator.embedder import DummyEmbedder
from rag_orchestrator.pipeline import InMemoryRAGPipeline
from rag_orchestrator.vector_store import QdrantVectorStore
from rag_orchestrator.retriever import Retriever
from rag_orchestrator.generator import AnswerGenerator

# ---- TEST DATA ----
text = "Employee leave policy allows sick leave and casual leave. " * 50

# ---- CHUNK + EMBED ----
chunker = FixedSizeChunker(chunk_size=50, overlap=10)
embedder = DummyEmbedder()

pipeline = InMemoryRAGPipeline(chunker, embedder)
results = pipeline.process_document("doc-001", text)

chunks = [c for c, _ in results]
vectors = [v for _, v in results]

# ---- STORE IN QDRANT ----
store = QdrantVectorStore(
    collection_name="documents",
    vector_size=len(vectors[0]),
)

store.upsert_chunks(chunks, vectors)
print("Stored chunks:", len(chunks))

# ---- RETRIEVE ----
retriever = Retriever(
    embedder=embedder,
    vector_store=store,
    top_k=3,
)

context = retriever.retrieve("What is the sick leave policy?")
print("Retrieved context count:", len(context))

# ---- BUILD PROMPT ----
generator = AnswerGenerator()
prompt = generator.build_prompt(
    context_chunks=context,
    question="What is the sick leave policy?",
)

print("\\n--- FINAL PROMPT ---")
print(prompt)