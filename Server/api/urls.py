from django.urls import path
from api.views import AskAPIView, TextIngestView

urlpatterns = [
    path("ingest/text", TextIngestView.as_view()),
    path("ask/", AskAPIView.as_view()),
]
