"""
This file defines one Django admin ForgetPasswordAdmin.
The admin is associated with its respective model
"""
from django.contrib import admin

from authentication.models import ForgetPassword


@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
    """
    Class UserAdmin display all the fields of User model in panel
    """
    list_display = ('id', 'user', 'forget_password_token', 'created_at', 'updated_at')
