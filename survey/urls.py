"""
This file contains URL patterns for a Survey
It uses a DefaultRouter to generate views
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from survey import views

router = DefaultRouter()
router.register('form', views.SurveyViewSet, basename='form')
# router.register('survey-status', views.SurveyStatusViewSet, basename='survey-status')
router.register('block', views.BlockViewSet, basename='block')
router.register('question', views.QuestionViewSet, basename='question')
router.register('default-question', views.DefaultQuestionViewSet, basename='default-question')
router.register('survey-link', views.SurveyLinkViewSet, basename='survey-link')


urlpatterns = [
    path('', include(router.urls)),
              ]
