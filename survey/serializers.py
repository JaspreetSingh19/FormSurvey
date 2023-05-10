"""
This file contains different serializers for 'Survey', 'Block', 'Question', 'DefaultQuestion'
and SurveyLink objects.
They handle serialization and deserialization of these objects,
and also include validation and creation/update logic.
"""
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from account.models import User
from survey.constants import MIN_LENGTH, MAX_LENGTH, QUESTION_MARKS
from survey.messages import VALIDATION
from survey.models import Survey, Block, Question, DefaultQuestion, SurveyLink


class SurveyLinkSerializer(serializers.ModelSerializer):
    """
    Serializer to get form details assigned to particular users
    """

    class Meta:
        """
        Class Meta for SurveyLinkSerializer with
        model and fields serializer should work with
        """
        model = SurveyLink
        fields = ['id', 'survey', 'user']


class SurveyLinkCreateSerializer(serializers.ModelSerializer):
    """
    Serializer with 'users' to assign form to different users
    """
    users = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=User.objects.exclude(password='')
        )
    )

    def create(self, validated_data):
        """
        Override create() method to send form link to user's email
        """
        survey = validated_data['survey']
        users = validated_data.pop('users')
        survey_links = []
        for user in users:
            survey_link = SurveyLink.objects.create(
                survey=survey, user=user
            )
            survey_links.append(survey_link)
            form_url = f'http://127.0.0.1:8000/survey/form/'

            # form_url = self.context['request'].build_absolute_uri(reverse('form_link-list', args=[survey_link.pk]))
            # user = validated_data['user']

            subject = 'Survey Link'
            message = 'Please fill out the form at {}'.format(form_url)
            from_email = 'projectgalleria5@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return survey_links

    class Meta:
        """
        Class Meta for SurveyLinkSerializer with
        model and fields serializer should work with
        """
        model = SurveyLink
        fields = ['id', 'survey', 'users']


class DefaultQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model with two required fields:
    'name', 'question_type', 'properties', 'marks'
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['name'], max_length=MAX_LENGTH['name'],
        required=True, error_messages=VALIDATION['name']
    )
    question_type = serializers.CharField(
        min_length=MIN_LENGTH['type'], max_length=MAX_LENGTH['type']
    )
    properties = serializers.JSONField(default=dict)
    marks = serializers.IntegerField(required=True, error_messages=VALIDATION['marks'])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the QuestionSerializer should work with
        """
        model = DefaultQuestion
        fields = ['id', 'name', 'question_type', 'properties', 'marks']


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model with two required fields:
    'name', 'block_id', 'question_type', 'properties', 'marks'
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['name'], max_length=MAX_LENGTH['name'],
        required=True, error_messages=VALIDATION['name']
    )
    block_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['block_id']
    )
    question_type = serializers.CharField(
        min_length=MIN_LENGTH['type'], max_length=MAX_LENGTH['type']
    )
    properties = serializers.JSONField(default=dict)
    marks = serializers.IntegerField(required=True, error_messages=VALIDATION['marks'])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the QuestionSerializer should work with
        """
        model = Question
        fields = ['id', 'name', 'block_id', 'question_type', 'properties', 'marks']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model with two required fields:
    'name', 'block_id', 'question_type', 'properties', 'marks'
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['name'], max_length=MAX_LENGTH['name'],
        required=True, error_messages=VALIDATION['name']
    )
    block_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['block_id'], allow_null=True
    )
    question_type = serializers.CharField(
        min_length=MIN_LENGTH['type'], max_length=MAX_LENGTH['type']
    )
    properties = serializers.JSONField(default=dict)
    marks = serializers.IntegerField(required=True, error_messages=VALIDATION['marks'])

    @staticmethod
    def validate_marks(value):
        """
        Validation to check marks cannot be less than 0
        :param value: marks
        :return: if valid return value, else return Validation error
        """
        if value < QUESTION_MARKS:
            raise serializers.ValidationError(VALIDATION['marks']['valid'])
        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Block instance
        """
        block = get_object_or_404(
            Block, id=validated_data['block_id']
        )
        obj = Question.objects.create(block=block, **validated_data)
        return obj

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the QuestionSerializer should work with
        """
        model = Question
        fields = ['id', 'name', 'block_id', 'question_type', 'properties', 'marks']


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model with two required fields:
    'name', 'block_id', 'question_type', 'properties', 'marks'
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['name'], max_length=MAX_LENGTH['name'],
        required=True, error_messages=VALIDATION['name']
    )
    block_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['block_id']
    )
    question_type = serializers.CharField(
        min_length=MIN_LENGTH['type'], max_length=MAX_LENGTH['type']
    )
    properties = serializers.JSONField(default=dict)
    marks = serializers.IntegerField(required=True, error_messages=VALIDATION['marks'])

    @staticmethod
    def validate_marks(value):
        """
        Validation to check marks cannot be less than 0
        :param value: marks
        :return: if valid return value, else return Validation error
        """
        if value < QUESTION_MARKS:
            raise serializers.ValidationError(VALIDATION['marks']['valid'])
        return value

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing Block instance
        """
        Question.objects.filter(id=instance.id).update(**validated_data)
        updated_instance = Question.objects.get(id=instance.id)

        return updated_instance

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the QuestionSerializer should work with
        """
        model = Question
        fields = ['id', 'name', 'block_id', 'question_type', 'properties', 'marks']


class BlockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model with two required fields:
    'name' and 'survey_id'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    block_questions = QuestionSerializer(many=True)
    name = serializers.CharField(
        min_length=MIN_LENGTH['block_name'], max_length=MAX_LENGTH['block_name'],
        required=True, error_messages=VALIDATION['block_name']
    )
    survey_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['survey_id']
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the BlockSerializer should work with
        """
        model = Block
        fields = ['id', 'name', 'survey_id', 'created_at', 'updated_at', 'block_questions']


class BlockCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model with two required fields:
    'name' and 'survey_id'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['block_name'], max_length=MAX_LENGTH['block_name'],
        required=True, error_messages=VALIDATION['block_name'])
    survey_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['survey_id'])

    @staticmethod
    def validate_name(value):
        """
        Validation to check if block already exists
        :param value: name
        :return: if valid return value, else return Validation error
        """
        if Block.objects.filter(name=value).exists():
            raise serializers.ValidationError(VALIDATION['block_name']['exists'])

        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Block instance
        """
        user = self.context['request'].user
        survey = get_object_or_404(
            Survey, id=validated_data['survey_id'], created_by=user
        )
        obj = Block.objects.create(survey=survey, **validated_data)
        return obj

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the BlockCreateSerializer should work with
        """
        model = Block
        fields = ['id', 'name', 'survey_id', 'created_at', 'updated_at']


class BlockUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model with two required fields:
    'name' and 'survey_id'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['block_name'], max_length=MAX_LENGTH['block_name'],
        required=True, error_messages=VALIDATION['block_name'])
    survey_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['survey_id'])

    @staticmethod
    def validate_name(value):
        """
        Validation to check if block already exists
        :param value: name
        :return: if valid return value, else return Validation error
        """
        if Block.objects.filter(name=value).exists():
            raise serializers.ValidationError(VALIDATION['block_name']['exists'])

        return value

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing Block instance
        """
        Block.objects.filter(id=instance.id).update(**validated_data)
        updated_instance = Block.objects.get(id=instance.id)

        return updated_instance

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the BlockUpdateSerializer should work with
        """
        model = Block
        fields = ['id', 'name', 'survey_id', 'created_at', 'updated_at']


class SurveySerializer(serializers.ModelSerializer):
    """
    Serializer for the Survey model with two required fields:
    'name' and 'description'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['form_name'], max_length=MAX_LENGTH['form_name'], required=True,
        error_messages=VALIDATION['form_name']
    ),
    description = serializers.CharField(
        min_length=MIN_LENGTH['description'], max_length=MAX_LENGTH['description'], required=True,
        error_messages=VALIDATION['description']
    )
    survey_block = BlockSerializer(many=True, read_only=True)
    survey_link = SurveyLinkSerializer(many=True, read_only=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the SurveySerializer should work with
        """
        model = Survey
        fields = [
            'id', 'name', 'description', 'is_published', 'created_at', 'updated_at', 'survey_block',
            'survey_link',
        ]


class SurveyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Survey model creating a new Survey instance with
    two required field:'name' & 'description' .
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['form_name'], max_length=MAX_LENGTH['form_name'],
        required=True, error_messages=VALIDATION['form_name']),
    description = serializers.CharField(
        min_length=MIN_LENGTH['description'], max_length=MAX_LENGTH['description'],
        required=True, error_messages=VALIDATION['description'])

    def validate_name(self, value):
        """
        Validation to check if form already exists
        :param value: name
        :return: if valid return value, else return Validation error
        """
        user = self.context['request'].user
        if Survey.objects.filter(created_by=user, name=value).exists():
            raise serializers.ValidationError(VALIDATION['form_name']['exists'])

        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Survey instance
        """
        user = self.context['request'].user
        obj = Survey.objects.create(created_by=user, **validated_data)
        return obj

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the SurveySerializer should work with
        """
        model = Survey
        fields = ['id', 'name', 'description', 'is_published', 'created_at', 'updated_at']


class SurveyUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Survey model updating an existing Survey instance with
    two required field:'name' & 'description' .
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    name = serializers.CharField(
        min_length=MIN_LENGTH['form_name'], max_length=MAX_LENGTH['form_name'],
        required=True, error_messages=VALIDATION['form_name']
    ),
    description = serializers.CharField(
        min_length=MIN_LENGTH['description'], max_length=MAX_LENGTH['description'],
        required=True, error_messages=VALIDATION['description']
    )

    def validate_name(self, value):
        """
        Validation to check if form already exists
        :param value: name
        :return: if valid return value, else return Validation error
        """
        user = self.context['request'].user
        if Survey.objects.filter(created_by=user, name=value).exists():
            raise serializers.ValidationError(VALIDATION['form_name']['exists'])

        return value

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing Survey instance
        """
        Survey.objects.filter(id=instance.id).update(**validated_data)
        updated_instance = Survey.objects.get(id=instance.id)

        return updated_instance

        # pylint: disable=too-few-public-methods

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the SurveySerializer should work with
        """
        model = Survey
        fields = ['id', 'name', 'description', 'is_published', 'created_at', 'updated_at']


class SurveyStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Survey model updating an existing Survey instance with
     required field:'is_published'.
    """
    survey_block = BlockSerializer(many=True, read_only=True)
    block_questions = QuestionSerializer(many=True, read_only=True)
    is_published = serializers.BooleanField(default=False)

    def validate(self, attrs):
        """
        Validation to check if survey has at least one block with at least one question
        """
        survey = self.instance
        if not survey.survey_block.exists() or not survey.survey_block.first().block_questions.exists():
            raise serializers.ValidationError(VALIDATION['blocks_or_questions']['not_found'])

        return attrs

    def update(self, instance, validated_data):
        """
        Override update() method to update the status of survey
        """
        is_published = validated_data.get('is_published', False)
        Survey.objects.filter(id=instance.id).update(is_published=is_published)
        updated_instance = Survey.objects.get(id=instance.id)
        return updated_instance

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the SurveyStatusUpdateSerializer should work with
        """
        model = Survey
        fields = ['id', 'is_published', 'block_questions', 'survey_block', 'updated_at']
