"""
This file contains two ViewSets for 'ForgetPasswordViewSets' and 'ResetPasswordViewSets'
for ForgetPassword objects.
All ViewSets requires authentication for all actions and
provides different serializers for different actions.
They also require permissions and filters
"""
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.models import User
from authentication.messages import RESET_PASSWORD
from authentication.models import ForgetPassword
from authentication.serializers import ForgetPasswordSerializer, ResetPasswordSerializer


class ForgotPasswordView(viewsets.ModelViewSet):
    """
    View to perform send mail operation with a
    link attached to it to reset password
    """
    serializer_class = ForgetPasswordSerializer
    queryset = User

    def get_queryset(self):
        return User.objects.filter(email='email').first()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response({'message': 'Password reset email sent'},
                            status=status.HTTP_200_OK)
        return Response(
            {'message': 'Email verification failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResetPasswordViewSet(viewsets.ViewSet):
    """
    View to handle resetting the user's password
    """
    serializer_class = ResetPasswordSerializer

    def create(self, request, token):
        """
        Create method to reset the new password by replacing the old
        password and verifying the token.
        :param request: new password
        :param token: forget password token
        :return: data
        """
        try:
            password_reset_token = ForgetPassword.objects.get(forget_password_token=token)
        except ForgetPassword.DoesNotExist:
            return Response({'error': 'Invalid token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - password_reset_token.created_at
        if time_difference.total_seconds() > (2 * 60):
            password_reset_token.delete()
            return Response({'error': 'Token expired.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = password_reset_token.user
        serializer = self.serializer_class(
            data=request.data, context={'user': user}
        )
        if serializer.is_valid():
            serializer.save()
            password_reset_token.delete()
            return Response(
                {'success': 'Password reset successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Password reset failed.'},
            status=status.HTTP_400_BAD_REQUEST
        )


