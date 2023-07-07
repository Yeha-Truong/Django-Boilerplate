from rest_framework import serializers

from core import serializers as core_serializers

from . import models


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = "__all__"


class TeacherViewSerializer(TeacherSerializer):
    user = core_serializers.UserSerializer()


class TeacherUpdateSerializer(TeacherSerializer):
    class Meta(TeacherSerializer.Meta):
        read_only_fields = ["user"]
