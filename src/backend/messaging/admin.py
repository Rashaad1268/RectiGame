from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.TopicChatChannel)
class TopicChatChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'created_at')


@admin.register(models.TopicChatMessage)
class TopicChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')


@admin.register(models.TopicRoom)
class TopicRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
