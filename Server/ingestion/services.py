import hashlib
from ingestion.models import Document


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
