"""
This file contains different ViewSets for User objects.
All ViewSets requires authentication for all actions and
provides different serializers for different actions.
They also require permissions and filters
"""
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.constants import LINK_EXPIRE_TIME
from account.messages import SUCCESS_MESSAGE, ERROR_MESSAGE, TOKEN_ERROR, PASSWORD_MESSAGE, SIGNUP_MESSAGE, EMAIL_SEND
from account.models import User
from account.serializers import SignupSerializer, SigninSerializer, SignOutSerializer, \
    SetPasswordSerializer, LoggedInUserSerializer, UserProfileSerializer, ReSendLinkSerializer
from authentication.models import ForgetPassword
from survey.permissions import AdminOnlyPermission


class SignupView(viewsets.ModelViewSet):
    """
    SignupView class to register a new user
    """
    queryset = User
    serializer_class = SignupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOnlyPermission]
    http_method_names = ['post', 'get', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'contact']
    ordering_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        user = self.filter_queryset(User.objects.all()).order_by('-id')
        return user

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        creates a new requested user
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data, request)
            return Response({
                'data': serializer.data,
                'success': SIGNUP_MESSAGE['created'],
                'message': SIGNUP_MESSAGE['email']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': SIGNUP_MESSAGE['delete']},
            status=status.HTTP_200_OK
        )


class SetPasswordViewSet(viewsets.ViewSet):
    """
    View to handle resetting the user's password
    """
    serializer_class = SetPasswordSerializer
    http_method_names = ['post']

    def create(self, request, token):
        """
        Create method to reset the new password by replacing the old
        password and verifying the token.
        :param request: new password
        :param token: forget password token
        :return: data
        """
        try:
            password_set_token = ForgetPassword.objects.get(forget_password_token=token)
        except ForgetPassword.DoesNotExist:
            return Response({'error': TOKEN_ERROR['Invalid']},
                            status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - password_set_token.created_at
        if time_difference.total_seconds() > LINK_EXPIRE_TIME:
            password_set_token.delete()
            return Response({'error': TOKEN_ERROR['Expired']},
                            status=status.HTTP_400_BAD_REQUEST)

        user = password_set_token.user
        serializer = self.serializer_class(
            data=request.data, context={'user': user}
        )
        if serializer.is_valid():
            serializer.save()
            password_set_token.delete()
            return Response(
                {'message': PASSWORD_MESSAGE['Success']},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': PASSWORD_MESSAGE['failed']},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoggedInUserView(viewsets.ModelViewSet):
    queryset = User
    serializer_class = LoggedInUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOnlyPermission]
    http_method_names = ['get']
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'contact']
    ordering_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        return self.filter_queryset(User.objects.exclude(password='')).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return Response(serializer.data)


class SigninView(viewsets.ModelViewSet):
    """
    Allow only authenticated user to signin.
    If the user is valid provide him the access and refresh token
    and save it to the database.
    """
    queryset = User.objects.filter()
    serializer_class = SigninSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.create(serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class SignOutView(viewsets.ModelViewSet):
    """
    Allow only signin user to sign out
    This Api perform the functionality to blacklist the refresh
    token to avoid access of unauthenticated user
    """
    serializer_class = SignOutSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.create(serializer.validated_data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ModelViewSet):
    """
    This view perform retrieving the data of the logged-in user
    and update their data according to their provided values.
    """
    queryset = User
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of User objects that
        includes only the currently authenticated user.
        """
        return User.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        """
        Display the single instance of the User
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        :param request: It gets the data that is requested by the user
        :param args: This returns the validated data in the form of list
        :param kwargs: This return the validated data in the form of dictionary
        :return: This return the updated data to the user with status
        """
        userprofile = self.get_object()
        serializer = self.serializer_class(userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(userprofile, serializer.validated_data)
            return Response({
                'message': SUCCESS_MESSAGE['success'],
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response({
            'error': ERROR_MESSAGE['error']
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        :param request: It gets the data that is requested by the user
        :param args: This returns the validated data in the form of list
        :param kwargs: This return the validated data in the form of dictionary
        :return: This return the updated data to the user with status
        """
        userprofile = self.get_object()
        serializer = self.serializer_class(userprofile, data=request.data)
        if serializer.is_valid():
            serializer.update(userprofile, serializer.validated_data)
            return Response({
                'message': SUCCESS_MESSAGE['success'],
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response({
            'error': ERROR_MESSAGE['error']
        }, status=status.HTTP_400_BAD_REQUEST)


class ResendSetPasswordViewSet(viewsets.ModelViewSet):
    queryset = User
    serializer_class = ReSendLinkSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOnlyPermission]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return User.objects.filter(email='email').first()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response({'message': EMAIL_SEND['success']},
                            status=status.HTTP_200_OK)
        return Response(
            {'message': EMAIL_SEND['failed']},
            status=status.HTTP_400_BAD_REQUEST
        )
