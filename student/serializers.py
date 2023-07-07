from rest_framework import serializers

from core import serializers as core_serializers

from . import models



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"


class StudentViewSerializer(StudentSerializer):
    user = core_serializers.UserSerializer()


class StudentUpdateSerializer(StudentSerializer):
    class Meta(StudentSerializer.Meta):
        read_only_fields = ["user"]
