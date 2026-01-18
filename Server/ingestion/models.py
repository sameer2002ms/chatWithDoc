import uuid
from django.db import models


class Document(models.Model):
    """
    Minimal source-of-truth document model for the RAG system.

    This model tracks document identity and ingestion status.
    The actual searchable content lives in the vector database (Qdrant).
    """

    STATUS_INGESTED = "INGESTED"
    STATUS_FAILED = "FAILED"

    STATUS_CHOICES = [
        (STATUS_INGESTED, "Ingested"),
        (STATUS_FAILED, "Failed"),
    ]

    # This UUID is your canonical document_id (used everywhere: DB, Qdrant, APIs)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # What kind of source this document came from
    source_type = models.CharField(
        max_length=20,
        help_text="pdf | text",
    )

    # Filename or user-provided name
    source_name = models.CharField(
        max_length=255,
        help_text="Filename or user-defined document name",
    )

    # Ingestion lifecycle status
    ingestion_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_INGESTED,
    )

    # Used to determine the latest document for /ask
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_name} [{self.ingestion_status}]"
