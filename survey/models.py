"""
This file defines Django models representing Survey.
All models are associated with its respective database table specified in its `Meta` class.
"""
from django.db import models
from account.models import User


# Create your models here.
class Survey(models.Model):
    """
    The Survey model with 'name', 'description', 'is_published',
    and foreign key to User model representing the user who owns the form.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_survey')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for Survey model
        """
        db_table = 'Survey'


class Block(models.Model):
    """
    The Block model with 'name' and foreign key to Survey model
    representing the form in which block is.
    """
    name = models.CharField(max_length=100)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_block')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for Block model
        """
        db_table = 'Block'


class Question(models.Model):
    """
    The Question model with 'name', 'question_type', 'properties', 'marks'
    and foreign key to Block model representing the block in which question is.
    """
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='block_questions', null=True)
    name = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50)
    properties = models.JSONField(default=dict)
    marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for Question model
        """
        db_table = 'Question'


class DefaultQuestion(models.Model):
    """
    The Question model with 'name', 'question_type', 'properties', 'marks'
    for default questions
    """
    name = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50)
    properties = models.JSONField(default=dict)
    marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for DefaultQuestion model
        """
        db_table = 'DefaultQuestion'


class SurveyLink(models.Model):
    """
    The Block model with 'is_submitted' and twp foreign keys to
    Survey model representing the form and User model representing
    the user to which form is assigned
    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_link')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_user')
    is_submitted = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.survey

    class Meta:
        """
        Use the Meta class to specify the database table
        for SurveyLink model
        """
        db_table = 'SurveyLink'

