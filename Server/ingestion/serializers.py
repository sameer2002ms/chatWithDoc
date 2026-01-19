from rest_framework import serializers


MAX_FILES = 2
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


class IngestRequestSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    def validate_files(self, files):
        # 1. Max number of files
        if len(files) > MAX_FILES:
            raise serializers.ValidationError(
                f"Maximum {MAX_FILES} PDF files are allowed per request."
            )

        for file in files:
            # 2. File size validation
            if file.size > MAX_FILE_SIZE_BYTES:
                raise serializers.ValidationError(
                    f"File '{file.name}' exceeds {MAX_FILE_SIZE_MB} MB size limit."
                )

            # 3. File type validation (PDF)
            if not file.name.lower().endswith(".pdf"):
                raise serializers.ValidationError(
                    f"File '{file.name}' is not a PDF."
                )

            # Optional: basic content-type check (not 100% reliable)
            if file.content_type != "application/pdf":
                raise serializers.ValidationError(
                    f"File '{file.name}' has invalid content type."
                )

        return files
