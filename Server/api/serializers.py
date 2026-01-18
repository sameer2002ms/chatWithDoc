from rest_framework import serializers

class TextIngestSerializer(serializers.Serializer):
    source_name = serializers.CharField(max_length=255)
    text = serializers.CharField()


class AskRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1000,
        help_text="User question for the document",
    )

    top_k = serializers.IntegerField(
        required=False,
        default=3,
        min_value=1,
        max_value=10,  # 🔒 guardrail for cost & noise
        help_text="Number of relevant chunks to retrieve",
    )
