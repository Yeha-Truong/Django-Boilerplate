from django.db import models

from core import models as core_models
from core import utils as core_utils

from . import enums



class Student(core_models.Model):
    stereotype = models.TextField(
        max_length=64,
        null=True,
        choices=core_utils.transform_enum_to_tuple(enums.Stereotype),
    )
    user = models.OneToOneField(
        to=core_models.User, on_delete=models.CASCADE, primary_key=True
    )
