# """
# This file defines Django admins for Notification model
# # These admins are associated with their respective model
# # """
# from django.contrib import admin
#
# from notification.models import Notification
#
#
# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     """
#     Class NotificationAdmin display all the fields of Notification model in panel
#     """
#     list_display = ('id', 'from_user', 'to_user', 'message', 'send_at')
