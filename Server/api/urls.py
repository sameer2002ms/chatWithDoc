from django.urls import path
from api.views import TextIngestView

urlpatterns = [
    path("ingest/text", TextIngestView.as_view()),
]
