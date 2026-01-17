import hashlib
from ingestion.models import Document
import uuid
import pdfplumber

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
    """
    Ingest a PDF file entirely in memory.
    Steps:
    - Read PDF from uploaded file object
    - Extract text from all pages
    - Return document_id + extracted text
    """

    document_id = str(uuid.uuid4())

    extracted_text = []

    try:
        # pdfplumber can read file-like objects directly
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

    # TEMPORARY return — next step we send this to chunker
    return {
        "document_id": document_id,
        "status": "INGESTED",
        "text_length": len(full_text)
    }
