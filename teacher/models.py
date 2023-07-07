from django.core import validators
from django.db import models

from core import models as core_models
from core import utils as core_utils

from . import enums

class Teacher(core_models.Model):
    profession = models.TextField(
        max_length=64,
        null=False,
        choices=core_utils.transform_enum_to_tuple(enums.Profession),
    )
    experiences = models.IntegerField(
        null=False,
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
    )
    user = models.OneToOneField(
        to=core_models.User, on_delete=models.CASCADE, primary_key=True
    )
