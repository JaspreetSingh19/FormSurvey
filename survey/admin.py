"""
This file defines different Django admins.
These admins are associated with their respective model
"""
from django.contrib import admin
from survey.models import Survey, Block, Question, DefaultQuestion, SurveyLink


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    """
    Class SurveyAdmin display all the fields of Survey model in panel
    """
    list_display = ('id', 'name', 'description', 'created_by', 'created_at', 'updated_at')


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    """
    Class BlockAdmin display all the fields of Block model in panel
    """
    list_display = ('id', 'name', 'created_at', 'updated_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Class QuestionAdmin display all the fields of Question model in panel
    """
    list_display = ('id', 'name', 'question_type', 'properties', 'marks', 'created_at', 'updated_at')


@admin.register(DefaultQuestion)
class DefaultQuestionAdmin(admin.ModelAdmin):
    """
    Class DefaultQuestionAdmin display all the fields of Question model in panel
    """
    list_display = ('id', 'name', 'question_type', 'properties', 'marks', 'created_at', 'updated_at')


@admin.register(SurveyLink)
class SurveyLinkAdmin(admin.ModelAdmin):
    """
    Class DefaultQuestionAdmin display all the fields of Question model in panel
    """
    list_display = ('id', 'survey', 'user', 'is_submitted', 'assigned_at')
