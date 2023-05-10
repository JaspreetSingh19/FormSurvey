# from rest_framework import status, viewsets
# from rest_framework.response import Response
#
# from notification.messages import SUCCESS_MESSAGES
# from notification.models import Notification
# from notification.serilaizers import NotificationSerializer, NotificationCreateSerializer
#
#
# class NotificationViewSet(viewsets.ModelViewSet):
#     """
#     The SurveyLinkViewSet handles form assigning to users
#     with authentication required for all actions.
#     It provides a serializer class for each action and
#     filters queryset based on the authenticated user.
#     """
#     queryset = Notification
#     http_method_names = ['get', 'post']
#
#     def get_serializer_class(self):
#         """
#         The get_serializer_class returns a serializer class based on the action being performed.
#         For 'create' action, it returns SurveyLinkCreateSerializer,
#         and for all other actions, it returns the default serializer, SurveyLinkSerializer.
#         :return:serializer class
#         """
#         if self.action == 'create':
#             return NotificationCreateSerializer
#         return NotificationSerializer
#
#     def get_queryset(self):
#         """
#         The get_queryset method returns a queryset of SurveyLink Model objects
#         filtered based on the user.
#         :return: SurveyLink objects
#         """
#         user = self.request.user.id
#         return Notification.objects.all().order_by('id')
#
#     def create(self, request, *args, **kwargs):
#         """
#         This method creates a new instance of the SurveyLink model using validated serializer data
#         If the data is valid, it creates a new instance and
#         returns a success response with a status code of 201.
#         If the data is invalid, it returns an error response with a status code of 400.
#         :return: response object
#         """
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             notifications = serializer.create(serializer.validated_data)
#             response_data = []
#             for notification in notifications:
#                 response_data.append({
#                     'from_user': notification.user.username,
#                     'to_user': notification.user.username,
#                     'message': notification.message,
#                     'assigned_at': notification.send_at
#                 })
#             return Response({'message': SUCCESS_MESSAGES['NOTIFICATION']['SEND_SUCCESSFULLY'],
#                              'data': response_data}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
