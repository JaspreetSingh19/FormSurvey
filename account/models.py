"""
This file defines Django models representing User.
All models are associated with its respective database table specified in its `Meta` class.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

from account.constants import ROLES


class User(AbstractUser):
    """
    Custom user model that extends the built-in Django User model
    with additional fields for User model

    * username and email are unique
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=16, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    is_activate = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for User model
        """
        db_table = 'User'
