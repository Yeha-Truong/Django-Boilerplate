from rest_framework import permissions, viewsets

from core import permissions as core_permissions

from . import models
from . import permissions as _permissions
from . import serializers


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAdminUser
        | _permissions.IsAuthoritativeTeacher
        | core_permissions.ReadOnly
    ]
    serializer_class = serializers.TeacherSerializer
    queryset = models.Teacher.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "list" | "retrieve":
                return serializers.TeacherViewSerializer
            case "update" | "partial_update":
                return serializers.TeacherUpdateSerializer
            case _:
                return serializers.TeacherSerializer