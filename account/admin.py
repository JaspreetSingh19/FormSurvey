"""
This file defines one Django admin UserAdmin.
The admin is associated with its respective model
"""
from django.contrib import admin

from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Class UserAdmin display all the fields of User model in panel
    """
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'contact',
                    'role', 'is_activate', 'password', 'created_at', 'updated_at')
