from django.db import models
from django.conf import settings
from django.utils import timezone

from topics.models import Topic, TopicMember


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(TopicMember, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="post_likes"
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="post_dislikes"
    )

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.edited_at = timezone.now()

        return super().save(*args, **kwargs)


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="reply_likes"
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="reply_dislikes"
    )

    # Replies can reply to other replies
    replying_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.edited_at = timezone.now()

        return super().save(*args, **kwargs)
