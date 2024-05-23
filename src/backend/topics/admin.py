from django.contrib import admin

from . import models


@admin.register(models.TopicTag)
class TopicTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(models.TopicMember)
class TopicMemberAdmin(admin.ModelAdmin):
    list_display = ("topic", "user")
