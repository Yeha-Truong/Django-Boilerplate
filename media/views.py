from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from media import serializers

# Create your views here.


class ImageUploadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ImageSerializer
    # parser_classes = [parsers.FileUploadParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image: InMemoryUploadedFile = serializer.validated_data["image"]
        file = default_storage.save(image.name, image)
        url = default_storage.url(file)

        return Response(
            url,
            status=status.HTTP_201_CREATED,
        )
