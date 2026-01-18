from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import TextIngestSerializer
from ingestion.services import ingest_text
from api.serializers import AskRequestSerializer
from ingestion.models import Document
from rag_orchestrator.qdrant_retriever import QdrantRetriever
from rag_orchestrator.generator import GPTAnswerGenerator


class TextIngestView(APIView):
    def post(self, request):
        serializer = TextIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = ingest_text(
            source_name=serializer.validated_data["source_name"],
            text=serializer.validated_data["text"],
        )

        return Response(
            {
                "document_id": str(document.id),
                "status": document.ingestion_status,
            },
            status=status.HTTP_201_CREATED,
        )


class AskAPIView(APIView):
    """
    Ask questions against the latest ingested PDF.
    """

    def post(self, request):
        # 1️⃣ Validate request
        serializer = AskRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        top_k = serializer.validated_data["top_k"]

        # 2️⃣ Get latest ingested document
        latest_document = (
            Document.objects.filter(ingestion_status="INGESTED")
            .order_by("-created_at")
            .first()
        )

        if not latest_document:
            return Response(
                {"error": "No ingested document found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        document_id = str(latest_document.id)

        # 3️⃣ Retrieve relevant chunks
        retriever = QdrantRetriever()
        chunks = retriever.retrieve(
            question=question,
            document_id=document_id,
            top_k=top_k,
        )
        # 🔒 Filter weak chunks (production best practice)
        chunks = [c for c in chunks if c.get("score", 0) >= 0.2]

        if not chunks:
            return Response(
                {
                    "answer": "The document does not contain this information.",
                    "sources": [],
                },
                status=status.HTTP_200_OK,
            )

        # 4️⃣ Generate answer (dummy)
        generator = GPTAnswerGenerator()
        response_payload = generator.generate(question, chunks)

        return Response(response_payload, status=status.HTTP_200_OK)
