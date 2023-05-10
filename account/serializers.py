"""
This file contains different serializers for 'User' objects.
They handle serialization and deserialization of these objects,
and also include validation and creation/update logic.
"""
import re
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from account.constants import MAX_LENGTH, MIN_LENGTH, REGEX, RESEND_LINK_TIME
from account.messages import SIGNUP_VALIDATION_ERROR, SIGNIN_VALIDATION_ERROR, TOKEN_ERROR, SET_PASSWORD_VALIDATION, \
    EMAIL_SEND
from account.models import User
from authentication.messages import RESET_PASSWORD, FORGET_PASSWORD
from authentication.models import ForgetPassword
from authentication.utils import generate_token
from survey.serializers import SurveyLinkSerializer


class SignupSerializer(serializers.ModelSerializer):
    """
    serializer for Registering requested user
    """
    first_name = serializers.CharField(
        max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'],
        required=True, allow_blank=False, trim_whitespace=True,
        error_messages=SIGNUP_VALIDATION_ERROR['first_name']
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['last_name']
    )
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['username']
    )
    email = serializers.EmailField(
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['email']
    )
    contact = serializers.CharField(
        min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'],
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['contact']
    )

    def validate(self, data):
        """
        Object level validation to check weather the given field exist or not and to match passwords
        """
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['exists'])
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['email']['exists'])
        return data

    @staticmethod
    def validate_first_name(value):
        """
        check that the first_name should contain only alphabets
        :param value:first_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["first_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        return value

    @staticmethod
    def validate_last_name(value):
        """
        check that the last_name should contain only alphabets
        :param value:last_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["last_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        return value

    @staticmethod
    def validate_username(value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['invalid'])
        return value

    @staticmethod
    def validate_contact(value):
        """
        check that the contact should contain only digits
        :param value:contact
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["contact"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['contact']['invalid'])
        return value

    # pylint: disable=too-few-public-methods
    def create(self, validated_data, request):
        """
        creates a user
        """
        user = User.objects.create(**validated_data)
        urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token(user)
        set_url = request.build_absolute_uri(
            reverse('set_password-list', kwargs={'token': token})
        )

        send_mail(
            'Welcome to My Site!',
            f'Hi, this is your registered username: {user.username}'
            f'  Please follow this link to set your password: {set_url}',
            'projectgallery5@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user

    class Meta:
        """
        class Meta for SignupSerializer
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'email', 'contact', 'is_activate']


class SetPasswordSerializer(serializers.Serializer):
    """
    Set password serializer to validate the password and if it
    is validated then save the user password in the database
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context.get('user')
        if attrs['password'] != attrs['confirm_password'] or user.username != attrs['username']:
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
        user.set_password(validated_data['password'])
        user.is_activate = True
        user.save()

        return user


class LoggedInUserSerializer(serializers.ModelSerializer):
    """
    Serializer for listing of user that set their password
    """
    survey_user = SurveyLinkSerializer(many=True, read_only=True)
    first_name = serializers.CharField(
        max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'],
        required=True, allow_blank=False, trim_whitespace=True,
        error_messages=SIGNUP_VALIDATION_ERROR['first_name']
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['last_name']
    )
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['username']
    )
    email = serializers.EmailField(
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['email']
    )
    contact = serializers.CharField(
        min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'],
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['contact']
    )

    class Meta:
        """
        class Meta for SignupSerializer
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'email', 'contact', 'survey_user']


class SigninSerializer(serializers.ModelSerializer):
    """
    Define a serializer for a signin view in Django
    """
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'],
        max_length=MAX_LENGTH['username'],
        required=True,
        allow_blank=False,
        trim_whitespace=False,
        error_messages=SIGNIN_VALIDATION_ERROR['username']
    )
    password = serializers.CharField(
        min_length=MIN_LENGTH['password'],
        max_length=MAX_LENGTH['password'],
        write_only=True,
        required=True,
        trim_whitespace=False,
        error_messages=SIGNIN_VALIDATION_ERROR['password']
    )

    @staticmethod
    def validate_username(value):
        """
        Check that the username is alphanumeric with at least one special character
        """
        if not re.match(REGEX["USERNAME"], value):
            raise serializers.ValidationError(SIGNIN_VALIDATION_ERROR['username']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        Check that the password is valid
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNIN_VALIDATION_ERROR['password']['invalid'])
        return value

    def validate(self, attrs):
        """
        Validate if the username and password are correct
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            raise serializers.ValidationError(SIGNIN_VALIDATION_ERROR['invalid credentials'])

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Generate the access and refresh tokens for the authenticated user
        """
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        user_token = User.objects.get(id=user.id)
        user_token.token = str(refresh.access_token)
        user_token.save()

        role = user.role

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': str(role),
        }

    class Meta:
        """
        Class Meta for SigninSerializer
        """
        model = User
        fields = ['username', 'password']


class SignOutSerializer(serializers.Serializer):
    """
    Serializer for user logout
    It blacklisted the refresh token after
    the authenticated user is logged-out
    """
    refresh = serializers.CharField(max_length=255)

    def validate(self, attrs):
        """
        Validate the refresh token from the user
        :param attrs: refresh
        :return: attrs
        """
        try:
            token = RefreshToken(attrs['refresh'])
            token_type = token.__class__.__name__
            if token_type != 'RefreshToken':
                raise serializers.ValidationError(TOKEN_ERROR['Invalid'])
            attrs['refresh_token'] = token
        except (InvalidToken, TokenError) as e:
            raise serializers.ValidationError(str(e))
        return attrs

    def create(self, validated_data):
        """
        Override create method to add refresh token
        to blacklist
        :param validated_data: refresh
        :return: success and error message
        """
        refresh_token = self.validated_data['refresh_token']
        refresh_token.blacklist()
        return {'success': True}


class UserProfileSerializer(serializers.ModelSerializer):
    """
    serializer for User model that return the authenticated
    user details and update them
    """
    first_name = serializers.CharField(
        max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'],
        required=True, allow_blank=False, trim_whitespace=True,
        error_messages=SIGNUP_VALIDATION_ERROR['first_name']
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['last_name']
    )
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['username']
    )
    email = serializers.EmailField(
        required=True, allow_blank=False, error_messages=SIGNUP_VALIDATION_ERROR['email']
    )
    contact = serializers.CharField(
        min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'],
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['contact']
    )
    password = serializers.CharField(
        write_only=True, min_length=MIN_LENGTH['password'], max_length=MAX_LENGTH['password'],
        allow_blank=False, error_messages=SIGNUP_VALIDATION_ERROR['password']
    )

    @staticmethod
    def validate_first_name(value):
        """
        check that the first_name should contain only alphabets
        :param value:first_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["first_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        return value

    @staticmethod
    def validate_last_name(value):
        """
        check that the last_name should contain only alphabets
        :param value:last_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["last_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        return value

    @staticmethod
    def validate_username(value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['invalid'])
        return value

    @staticmethod
    def validate_contact(value):
        """
        check that the contact should contain only digits
        :param value:contact
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["contact"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['contact']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return make_password(value)

    def update(self, instance, validated_data):
        """
        Override update method to modify the user details
        :param instance: id
        :param validated_data: validated data
        :return: userprofile
        """

        userprofile = User.objects.filter(id=instance.id).update(**validated_data)
        return userprofile

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        class Meta for UserProfileSerializer that take first name,
        last name, username, email, contact and password fields.
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'email', 'contact', 'password']


class ReSendLinkSerializer(serializers.Serializer):
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
        email = validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(FORGET_PASSWORD['email']['email_not_exist'])

        if user.password:
            raise serializers.ValidationError(SET_PASSWORD_VALIDATION['exists'])

        forget_password = ForgetPassword.objects.filter(user=user).first()

        if forget_password and forget_password.updated_at > timezone.now() - timedelta(hours=RESEND_LINK_TIME):
            raise serializers.ValidationError(SET_PASSWORD_VALIDATION['time'])

        request = self.context.get('request')
        token = generate_token(user)
        reset_url = request.build_absolute_uri(
            reverse('set_password-list', kwargs={'token': token})
        )

        ForgetPassword.objects.update_or_create(
            user=user,
            forget_password_token=token,
        )
        send_mail(
            'Password Reset Request',
            f'Please follow this link to set your password: {reset_url}',
            'projectgalleria5@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return {'message': EMAIL_SEND['success']}

