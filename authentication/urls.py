"""
This file contains URL patterns for authentication
It uses a DefaultRouter to generate views
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()

router.register('forget_password', views.ForgotPasswordView, basename='forget_password')
router.register(
    r'reset_password/(?P<token>[^/.]+)', views.ResetPasswordViewSet, basename='reset_password'
)

urlpatterns = [
    path('', include(router.urls)),
]
