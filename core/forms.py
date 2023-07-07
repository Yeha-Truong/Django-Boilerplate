from django.contrib.auth import forms

from . import models


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = forms.UserCreationForm.Meta.fields


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = models.User
        fields = forms.UserChangeForm.Meta.fields
