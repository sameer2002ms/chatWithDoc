from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ingestion.serializers import IngestRequestSerializer
from ingestion.services import ingest_pdf_in_memory


class IngestAPIView(APIView):
    """
    POST /ingest
    Accepts one or more PDF files and ingests them in memory.
    """

    def post(self, request):
        serializer = IngestRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        files = serializer.validated_data["files"]
        results = []

        for file in files:
            try:
                result = ingest_pdf_in_memory(file)

                results.append({
                    "filename": file.name,
                    "document_id": result["document_id"],
                    "status": result["status"],
                    "text_length": result["text_length"]
                })


            except Exception as e:
                results.append({
                    "filename": file.name,
                    "status": "FAILED",
                    "error": str(e)
                })

        return Response(
            {"documents": results},
            status=status.HTTP_200_OK
        )
