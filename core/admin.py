from django.contrib import admin
from core import forms, models
from django.contrib.auth import admin as auth_admin


class UserAdmin(auth_admin.UserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    model = models.User
    search_fields = ['username', 'email']
    ordering = ['username', 'email']
    filter_horizontal = ['groups']


admin.site.register(models.User, UserAdmin)
