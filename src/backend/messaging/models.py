from django.db import models, transaction
from django.conf import settings
from django.utils import timezone, crypto
from django.core.exceptions import ValidationError

from topics.models import Topic


class TopicChatChannel(models.Model):
    type = models.PositiveSmallIntegerField(choices=((1, "Text Channel"), (2, "Room")), default=1)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="topic_room_member")
    invite_code = models.SlugField(
        max_length=20, unique=True, null=True, blank=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="topic_room_creator",
    )

    def save(self, *args, **kwargs):
        is_being_created = self._state.adding

        if self.type == 2 and not self.invite_code and is_being_created:
            self.invite_code = crypto.get_random_string(8)

        super().save(*args, **kwargs)

        if self.type == 2 and is_being_created:

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
