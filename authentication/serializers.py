"""
This file contains different serializers for 'ForgetPassword' objects.
They handle serialization and deserialization of these objects,
and also include validation and forget password/rest password logic.
"""
import re

from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from account.constants import REGEX
from account.messages import SIGNUP_VALIDATION_ERROR
from account.models import User
from authentication.messages import FORGET_PASSWORD, RESET_PASSWORD
from authentication.models import ForgetPassword
from authentication.utils import generate_token


class ForgetPasswordSerializer(serializers.ModelSerializer):
    """
    forget password serializer to verify the email of the user
    and send the mail to its register email.
    """
    email = serializers.EmailField()

    @staticmethod
    def validate_email(email):
        """
        Validate the user's email using Django's PasswordResetForm
        """
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(FORGET_PASSWORD['email']['email_not_exist'])

        PasswordResetForm({'email': email})

        return email

    def create(self, validated_data):
        """
        Generate a password reset token and URL for the user
        :param validated_data: email
        :return: validated data
        """
        request = self.context.get('request')
        user = User.objects.get(email=validated_data['email'])
        token = generate_token(user)
        reset_url = request.build_absolute_uri(
            reverse('reset_password-list', kwargs={'token': token})
        )

        ForgetPassword.objects.update_or_create(
            user=user,
            forget_password_token=token,
        )
        send_mail(
            'Password Reset Request',
            f'Please follow this link to reset your password: {reset_url}',
            'projectgalleria5@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return validated_data

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Class meta to define the model and the field
        of that model.
        """
        model = User
        fields = ['email']


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset password serializer to validate the password and if it
    is validated then save the new password with the old one in the database
    """
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(RESET_PASSWORD['password_reset']['do_not_match'])

        return attrs

    @staticmethod
    def validate_new_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return value

    def create(self, validated_data):
        user = self.context.get('user')
        user.set_password(validated_data['new_password'])
        user.save()

        return user

