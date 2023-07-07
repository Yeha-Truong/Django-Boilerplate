from rest_framework import permissions

from account import enums as account_enums
from core import models as core_models


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        user: core_models.User = request.user
        is_teacher = user.groups.filter(
            name=account_enums.Group.TEACHER.value
        ).exists()

        return is_teacher


class IsAuthoritativeTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user: core_models.User = request.user
        teacher = obj.user if hasattr(obj, "user") else None

        return user and user == teacher
