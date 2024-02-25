from django.db import models, transaction
from django.conf import settings
from django.utils import timezone, crypto
from django.core.exceptions import ValidationError

from topics.models import Topic


class TopicChatChannel(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def generate_room_code():
    return crypto.get_random_string(8)


class TopicRoom(models.Model):
    name = models.CharField(null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topic_room_creator",
    )
    code = models.SlugField(
        max_length=20, unique=True, blank=True, default=generate_room_code
    )
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="topic_room_member", blank=True
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_being_created = self._state.adding
        super().save(*args, **kwargs)

        if is_being_created:

            def add_member():
                # Add the creator of the room as a member
                self.members.add(self.creator)

            # https://stackoverflow.com/a/78053539/13953998
            transaction.on_commit(add_member)


class TopicChatMessage(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    channel = models.ForeignKey(
        TopicChatChannel, on_delete=models.CASCADE, null=True, blank=True
    )
    room = models.ForeignKey(TopicRoom, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    message_type = models.PositiveSmallIntegerField(default=0)

    def clean(self) -> None:
        if not self.channel and not self.room:
            raise ValidationError(
                "Either channel or room must be specified when creating a message"
            )

    def save(self, *args, **kwargs):
        if self.id:
            self.edited_at = timezone.now()

        super().save(*args, **kwargs)
