from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import TextIngestSerializer
from ingestion.services import ingest_text


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
