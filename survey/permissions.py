"""
This file defines custom permissions that can be used throughout module
"""
from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):
    """
    Custom permission class that only allows users with different role to perform a given task
    """
    def has_permission(self, request, view):
        """
        Give permission to only user with admin role
        """
        return request.user.role == 'admin'
