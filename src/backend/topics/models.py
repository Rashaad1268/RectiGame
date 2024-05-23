from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

from . import topic_permissions as topic_perms


class TopicTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, blank=True, primary_key=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="topic/images")
    icon = models.ImageField(upload_to="topic/icons", null=True, blank=True)
    banner = models.ImageField(upload_to="topic/banners", null=True, blank=True)
    tags = models.ManyToManyField(TopicTag, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def channel_name(self):
        """The named used for channel groups"""
        return f"Topic-{self.slug}"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_being_created = not self.slug

        if is_being_created:
            # New instance being created
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        if is_being_created:
            # Create a main chat channel for topic after saving
            from messaging.models import TopicChatChannel

            TopicChatChannel(
                name="main",
                description=f"The main channel for {self.name}",
                topic=self,
            ).save()


class TopicMember(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="topic_members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topic_member",
    )
    nickname = models.CharField(max_length=30, null=True, blank=True)
    permissions = models.PositiveBigIntegerField(
        default=topic_perms.default_permissions,
    )
    joined_at = models.DateTimeField(default=timezone.now)
    has_left = models.BooleanField(default=False)

    class Meta:
        unique_together = ("topic", "user")


class CustomTopicEmoji(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="topic/custom_emojis")
    created_by = models.ForeignKey(
        TopicMember, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(default=timezone.now)
