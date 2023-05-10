"""
This file contains various functions that can be used throughout the module.
"""
import secrets

from authentication.models import ForgetPassword


def generate_token(user):
    """
    Generate a unique token for the given user.
    """
    token = secrets.token_hex(16)  # generate a 32-character hex string
    # associate the token with the user
    ForgetPassword.objects.update_or_create(
        user=user,
        defaults={'forget_password_token': token})

    return token
