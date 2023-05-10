"""
This file contains URL patterns for Account
It uses a DefaultRouter to generate views
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
"""
Routing for Signup and Signin
"""
router.register('signup', views.SignupView, basename='signup')
router.register('signin', views.SigninView, basename='signin')
router.register('sign-out', views.SignOutView, basename='sign_out')
router.register(
    r'set_password/(?P<token>[^/.]+)', views.SetPasswordViewSet, basename='set_password'
)
router.register('logged-in-users', views.LoggedInUserView, basename='logged_in_users')
router.register('userprofile', views.UserProfileView, basename='userprofile')
router.register('resend-setpassword', views.ResendSetPasswordViewSet, basename='resend_setpassword')

urlpatterns = [
    path('', include(router.urls)),
]
