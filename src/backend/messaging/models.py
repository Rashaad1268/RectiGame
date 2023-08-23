from django.conf import settings
from django.utils import timezone
from django.db import models
from topics.models import Topic


class TopicChatChannel(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TopicChatMessage(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    channel = models.ForeignKey(TopicChatChannel, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    message_type = models.PositiveSmallIntegerField(default=0)

    def edit(self, *args, **kwargs):
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)
