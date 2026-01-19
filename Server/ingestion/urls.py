from django.urls import path
from ingestion.views import IngestAPIView

urlpatterns = [
    path("ingest/", IngestAPIView.as_view(), name="ingest"),
]
