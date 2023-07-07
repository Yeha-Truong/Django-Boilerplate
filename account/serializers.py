from django.contrib.auth import models as auth_models
from rest_framework import serializers

from core import models as core_models, utils as core_utils
from teacher import models as teacher_models, enums as teacher_enums
from student import models as student_models, enums as student_enums

from . import enums as enums
from . import models as models


class UserSignupSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=core_utils.transform_enum_to_tuple(enums.Group),
        allow_blank=False,
    )

    class Meta:
        model = core_models.User
        fields = ["username", "email", "password", "first_name", "last_name", "type"]

    def validate_type(self, value):
        try:
            group = auth_models.Group.objects.get(name=value)
            if group is None:
                raise serializers.ValidationError("Invalid type!")
        except:
            raise serializers.ValidationError("Invalid type!")

        return value

    def create(self, validated_data):
        type = validated_data.pop("type")
        group = auth_models.Group.objects.get(name=type)
        user: core_models.User = core_models.User.objects.create_user(**validated_data)
        user.groups.add(group)
        match type:
            case enums.Group.TEACHER.value:
                teacher_models.Teacher.objects.create(
                    user=user,
                    profession=teacher_enums.Profession.UNKNOWN.value,
                    experiences=0,
                )
            case enums.Group.STUDENT.value:
                student_models.Student.objects.create(
                    user=user,
                    stereotype=student_enums.Stereotype.UNKNOWN.value,
                )
            case _:
                pass
        return user


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(trim_whitespace=True, required=True)
    password = serializers.CharField(trim_whitespace=False, min_length=6, required=True)
