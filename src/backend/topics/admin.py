from django.contrib import admin

from . import models


@admin.register(models.TopicTag)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
