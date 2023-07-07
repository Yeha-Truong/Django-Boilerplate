from rest_framework import permissions, viewsets

from core import permissions as core_permissions

from . import models
from . import permissions as _permissions
from . import serializers

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAdminUser
        | _permissions.IsAuthoritativeStudent
        | core_permissions.ReadOnly
    ]
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "list" | "retrieve":
                return serializers.StudentViewSerializer
            case "update" | "partial_update":
                return serializers.StudentUpdateSerializer
            case _:
                return serializers.StudentSerializer