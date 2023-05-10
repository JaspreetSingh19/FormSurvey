"""
This file defines Django model representing Notification.
All models are associated with its respective database table specified in its `Meta` class.
"""
from django.db import models

from account.models import User


# Create your models here.
# class Notification(models.Model):
#     """
#      The Notification model with 'message' and two foreign keys to
#      User model representing the users
#     """
#     from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_notification')
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_notification')
#     message = models.CharField(max_length=255)
#     send_at = models.DateField(auto_now_add=True)
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.message
#
#     class Meta:
#         """
#         Use the Meta class to specify the database table
#         for Notification model
#         """
#         db_table = 'Notification'
