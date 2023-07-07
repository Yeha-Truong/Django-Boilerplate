from rest_framework import permissions

from account import enums as account_enums
from core import models as core_models


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user: core_models.User = request.user
        is_student = user.groups.filter(name=account_enums.Group.STUDENT.value).exists()

        return is_student


class IsAuthoritativeStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user: core_models.User = request.user
        student = obj.user if hasattr(obj, "user") else None

        return user and user == student

