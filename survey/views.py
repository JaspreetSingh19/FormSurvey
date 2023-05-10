from rest_framework import viewsets, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from survey.messages import VALIDATION, SUCCESS_MESSAGES
from survey.models import Survey, Block, Question, DefaultQuestion, SurveyLink
from survey.permissions import AdminOnlyPermission
from survey.serializers import SurveyCreateSerializer, SurveyUpdateSerializer, SurveySerializer, \
    BlockCreateSerializer, BlockUpdateSerializer, BlockSerializer, QuestionCreateSerializer, QuestionUpdateSerializer, \
    QuestionSerializer, DefaultQuestionSerializer, SurveyLinkCreateSerializer, SurveyLinkSerializer


# pylint: disable=too-many-ancestors
class SurveyViewSet(viewsets.ModelViewSet):
    """
    The SurveySet handles CRUD operations for the Survey model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Survey
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, AdminOnlyPermission]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id']

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns SurveyCreateSerializer,
        for 'update' action, it returns SurveyUpdateSerializer,
        and for all other actions, it returns the default serializer, SurveySerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return SurveyCreateSerializer
        if self.action == 'update':
            return SurveyUpdateSerializer
        return SurveySerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Survey Model objects
        filtered based on the user.
        It orders the queryset based on the ID of the objects.
        :return: Survey objects
        """
        user = self.request.user.id
        return self.filter_queryset(Survey.objects.filter(created_by=user)).order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the Survey model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Survey instances
        """
        if not self.get_queryset().exists():
            return Response(
                {"message": VALIDATION['forms']['no_forms']}, status=status.HTTP_200_OK
            )
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the Survey model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Survey instance
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Survey model using validated serializer data
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            survey = serializer.create(serializer.validated_data)

            blocks = Block.objects.filter(survey=survey)
            if len(blocks) == 1 and len(blocks[0].block_questions.all()) == 1:
                survey.is_published = True
                survey.save()
                return Response({'message': SUCCESS_MESSAGES['FORM']['PUBLISHED_SUCCESSFULLY'],
                                 'data': {
                                     'id': survey.id,
                                     'name': survey.name,
                                     'description': survey.description,
                                     'is_published': survey.is_published,
                                     'created_at': survey.created_at,
                                 }}, status=status.HTTP_201_CREATED)

            if request.data.get('is_published', False):
                raise ValidationError(VALIDATION['is_published']['False'])

            survey.is_published = False
            survey.save()
            return Response({'message': SUCCESS_MESSAGES['FORM']['SAVED_AS_DRAFT'],
                             'data': {
                                 'id': survey.id,
                                 'name': survey.name,
                                 'description': survey.description,
                                 'is_published': survey.is_published,
                                 'created_at': survey.created_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Survey model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            survey = serializer.update(instance, serializer.validated_data)
            blocks = Block.objects.filter(survey=survey)
            if len(blocks) == 1 and len(blocks[0].block_questions.all()) == 1:
                survey.is_published = True
                survey.save()

                return Response({'message': SUCCESS_MESSAGES['FORM']['UPDATED_SUCCESSFULLY'],
                                 'data': {
                                     'id': survey.id,
                                     'name': survey.name,
                                     'description': survey.description,
                                     'updated_at': survey.updated_at,
                                 }}, status=status.HTTP_201_CREATED)

            survey.is_published = False
            survey.save()
            return Response({'message': SUCCESS_MESSAGES['FORM']['SAVED_AS_DRAFT'],
                             'data': {
                                 'id': survey.id,
                                 'name': survey.name,
                                 'description': survey.description,
                                 'is_published': survey.is_published,
                                 'created_at': survey.updated_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Survey model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            survey = serializer.update(instance, serializer.validated_data)
            blocks = Block.objects.filter(survey=survey)
            if len(blocks) == 1 and len(blocks[0].block_questions.all()) == 1:
                survey.is_published = True
                survey.save()

                return Response({'message': SUCCESS_MESSAGES['FORM']['UPDATED_SUCCESSFULLY'],
                                 'data': {
                                     'id': survey.id,
                                     'name': survey.name,
                                     'description': survey.description,
                                     'updated_at': survey.updated_at,
                                 }}, status=status.HTTP_201_CREATED)

            survey.is_published = False
            survey.save()
            return Response({'message': SUCCESS_MESSAGES['FORM']['SAVED_AS_DRAFT'],
                             'data': {
                                 'id': survey.id,
                                 'name': survey.name,
                                 'description': survey.description,
                                 'is_published': survey.is_published,
                                 'created_at': survey.updated_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the Survey model using the primary key
        It returns a success response with a message after the deletion is complete.
        return: success response
        """
        instance = self.get_object()
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['FORM']['DELETED_SUCCESSFULLY']},
                        status=status.HTTP_200_OK)


class BlockViewSet(viewsets.ModelViewSet):
    """
    The BlockViewSet handles CRUD operations for the Block model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Survey
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOnlyPermission]

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns SurveyCreateSerializer,
        for 'update' action, it returns SurveyUpdateSerializer,
        and for all other actions, it returns the default serializer, SurveySerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return BlockCreateSerializer
        if self.action == 'update':
            return BlockUpdateSerializer
        return BlockSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Block Model objects
        filtered based on the user.
        It orders the queryset based on the ID of the objects.
        :return: Survey objects
        """
        user = self.request.user.id
        return Block.objects.filter(survey__created_by=user).order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the Block model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Survey instances
        """
        if not self.get_queryset().exists():
            return Response(
                {"message": VALIDATION['blocks']['no_blocks']}, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the Block model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Survey instance
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Block model using validated serializer data
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            block = serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['BLOCK']['CREATED_SUCCESSFULLY'],
                             'data': {
                                 'id': block.id,
                                 'name': block.name,
                                 'survey_id': block.survey_id,
                                 'created_at': block.created_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Block model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            block = serializer.update(instance, serializer.validated_data)

            return Response({'message': SUCCESS_MESSAGES['BLOCK']['UPDATED_SUCCESSFULLY'],
                             'data': {
                                 'id': block.id,
                                 'name': block.name,
                                 'survey_id': block.survey_id,
                                 'updated_at': block.updated_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Block model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            block = serializer.update(instance, serializer.validated_data, partial=True)

            return Response({'message': SUCCESS_MESSAGES['BLOCK']['UPDATED_SUCCESSFULLY'],
                             'data': {
                                 'id': block.id,
                                 'name': block.name,
                                 'survey_id': block.survey_id,
                                 'updated_at': block.updated_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the Survey model using the primary key
        It returns a success response with a message after the deletion is complete.
        :return: success response
        """
        instance = self.get_object()
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['BLOCK']['DELETED_SUCCESSFULLY']},
                        status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    The QuestionViewSet handles CRUD operations for the Question model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = Question
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOnlyPermission]

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns QuestionCreateSerializer,
        for 'update' action, it returns QuestionUpdateSerializer,
        and for all other actions, it returns the default serializer, QuestionSerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return QuestionCreateSerializer
        if self.action == 'update':
            return QuestionUpdateSerializer
        return QuestionSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Question Model objects
        filtered based on the user.
        It orders the queryset based on the question_no of the objects.
        :return: Survey objects
        """
        user = self.request.user.id
        return Question.objects.filter(block__survey__created_by=user).order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the Question model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Question instances
        """
        if not self.get_queryset().exists():
            return Response(
                {"message": VALIDATION['question']['no_questions']}, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the Question model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Question instance
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Question model using validated serializer data
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            question = serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['QUESTION']['CREATED_SUCCESSFULLY'],
                             'data': {
                                 'id': question.id,
                                 'name': question.name,
                                 'question_type': question.question_type,
                                 'properties': question.properties,
                                 'marks': question.marks,
                                 'block_id': question.block_id,
                                 'created_at': question.created_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Question model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            question = serializer.update(instance, serializer.validated_data)

            return Response({'message': SUCCESS_MESSAGES['QUESTION']['UPDATED_SUCCESSFULLY'],
                             'data': {
                                 'id': question.id,
                                 'name': question.name,
                                 'question_type': question.question_type,
                                 'properties': question.properties,
                                 'block_id': question.block_id,
                                 'marks': question.marks,
                                 'updated_at': question.updated_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Question model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            question = serializer.update(instance, serializer.validated_data)

            return Response({'message': SUCCESS_MESSAGES['QUESTION']['UPDATED_SUCCESSFULLY'],
                             'data': {
                                 'id': question.id,
                                 'name': question.name,
                                 'question_type': question.question_type,
                                 'properties': question.properties,
                                 'block_id': question.block_id,
                                 'marks': question.marks,
                                 'updated_at': question.updated_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the Question model using the primary key
        It returns a success response with a message after the deletion is complete.
        :return: success response
        """
        instance = self.get_object()
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['QUESTION']['DELETED_SUCCESSFULLY']},
                        status=status.HTTP_200_OK)


class DefaultQuestionViewSet(viewsets.ModelViewSet):
    """
    The DefaultQuestionViewSet handles List operations for the DefaultQuestion model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    http_method_names = ['get']
    queryset = Question
    serializer_class = DefaultQuestionSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of DefaultQuestion Model objects
        filtered based on the user.
        :return: DefaultQuestion objects
        """
        return DefaultQuestion.objects.filter()

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the DefaultQuestion model.
        serializes them using the serializer returned by the serializer_class method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: DefaultQuestion instances
        """
        if not self.get_queryset().exists():
            return Response(
                {"message": VALIDATION['default_question']['no_questions']}, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the DefaultQuestion model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Question instance
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SurveyLinkViewSet(viewsets.ModelViewSet):
    """
    The SurveyLinkViewSet handles form assigning to users
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    http_method_names = ['get', 'post']
    queryset = SurveyLink
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminOnlyPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['survey', 'user']
    ordering_fields = ['id']

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns SurveyLinkCreateSerializer,
        and for all other actions, it returns the default serializer, SurveyLinkSerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return SurveyLinkCreateSerializer
        return SurveyLinkSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of SurveyLink Model objects
        filtered based on the user.
        :return: SurveyLink objects
        """
        user = self.request.user.id
        return SurveyLink.objects.filter(survey__created_by=user).order_by('id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the SurveyLink model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: SurveyLink instances
        """
        queryset = self.get_queryset()
        if not self.get_queryset().exists():
            return Response(
                {"message": VALIDATION['forms']['no_forms_assigned']}, status=status.HTTP_200_OK
            )
        assign = []
        for survey_link in queryset:
            assign.append({
                'form': survey_link.survey.name,
                'user': survey_link.user.username,
                'assigned_at': survey_link.assigned_at
            })

        self.get_serializer(assign)
        return Response(assign, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the SurveyLink model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single QuestionType instance
        """
        instance = self.get_object()
        self.get_serializer(instance)
        return Response(
            {'data': {
                'form': instance.survey.name,
                'user': instance.user.username,
                'assigned_at': instance.assigned_at
            }}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the SurveyLink model using validated serializer data
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            survey_links = serializer.create(serializer.validated_data)
            response_data = []
            for survey_link in survey_links:
                response_data.append({
                    'form': survey_link.survey.name,
                    'user': survey_link.user.username,
                    'assigned_at': survey_link.assigned_at
                })
            return Response({'message': SUCCESS_MESSAGES['FORM']['ASSIGNED_SUCCESSFULLY'],
                             'data': response_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)