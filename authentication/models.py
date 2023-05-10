"""
This file defines Django models representing ForgetPassword.
All models are associated with its respective database table specified in its `Meta` class.
"""
from django.db import models

from account.models import User


class ForgetPassword(models.Model):
    """
    The Survey model with ' forget_password_token',
    and foreign key to User model representing the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255, unique=True, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.user.email)

    class Meta:
        """
        Use the Meta class to specify the database table
        for ForgetPassword model
        """
        db_table = 'ForgetPassword'
