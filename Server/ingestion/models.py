import uuid
from django.db import models


class Document(models.Model):
    """
    Source-of-truth document for the RAG system.
    Raw content is always stored here before any chunking or embeddings.
    """

    STATUS_PENDING = "PENDING"
    STATUS_INGESTED = "INGESTED"
    STATUS_FAILED = "FAILED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_INGESTED, "Ingested"),
        (STATUS_FAILED, "Failed"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    source_type = models.CharField(
        max_length=50, help_text="pdf | docx | text | url | manual"
    )

    source_name = models.CharField(
        max_length=255, help_text="Filename, URL, or user-defined name"
    )

    raw_text = models.TextField(help_text="Original extracted text (pre-chunking)")

    checksum = models.CharField(
        max_length=64, help_text="SHA-256 hash for deduplication"
    )

    ingestion_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source_name} [{self.ingestion_status}]"
