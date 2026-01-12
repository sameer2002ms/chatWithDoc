from rest_framework import serializers


class TextIngestSerializer(serializers.Serializer):
    source_name = serializers.CharField(max_length=255)
    text = serializers.CharField()
