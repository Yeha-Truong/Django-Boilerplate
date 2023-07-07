from django.contrib.auth import models as auth_models
from django.db import models

from . import managers


class Model(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Model, auth_models.AbstractUser):
    email = models.EmailField(unique=True)
    objects = managers.UserManager()
