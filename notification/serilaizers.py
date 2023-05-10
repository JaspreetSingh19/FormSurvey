# from rest_framework import serializers
#
# from account.models import User
# from notification.models import Notification
#
#
# class NotificationSerializer(serializers.ModelSerializer):
#     """
#     Serializer to get notification details send to particular users
#     """
#
#     class Meta:
#         """
#         Class Meta for NotificationSerializer with
#         model and fields serializer should work with
#         """
#         model = Notification
#         fields = ['id', 'from_user', 'to_user', 'message']
#
#
# class NotificationCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer to send notification to different users
#     """
#
#     def validate(self, attrs):
#         user = self.context['request'].user
#         if user.role != 'admin':
#             raise serializers.ValidationError('You do not have permission to send notifications.')
#         return attrs
#
#     def create(self, validated_data):
#         """
#         Override create() method to send notification to user's dashboard
#         """
#         user = self.context['request'].user
#
#         if user.role != 'admin':
#             raise serializers.ValidationError('You do not have permission to send notifications.')
#
#         to_user_id = validated_data['to_user']
#         to_user = User.objects.get(id=to_user_id)
#
#         notification = Notification.objects.crreate(
#             from_user=user,
#             to_user=to_user,
#             message=validated_data['message']
#         )
#         notification.save()
#
#         return notification
#
#     class Meta:
#         """
#         Class Meta for NotificationCreateSerializer with
#         model and fields serializer should work with
#         """
#         model = Notification
#         fields = ['id', 'from_user', 'to_user', 'message']
