from django.db import models, transaction
from django.conf import settings
from django.utils import timezone, crypto

from topics.models import Topic, TopicMember


class TopicChatChannel(models.Model):
    type = models.PositiveSmallIntegerField(
        choices=((1, "Text Channel"), (2, "Room")), default=1
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    members = models.ManyToManyField(
        TopicMember, blank=True, related_name="room_member"
    )
    invite_code = models.SlugField(max_length=20, unique=True, null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="room_creator",
    )

    def save(self, *args, **kwargs):
        is_being_created = self._state.adding

        if self.type == 2 and not self.invite_code and is_being_created:
            self.invite_code = crypto.get_random_string(8)

        super().save(*args, **kwargs)

        if self.type == 2 and is_being_created:

            def add_member():
                # Add the creator of the room as a member
                creator_member, created = TopicMember.objects.get_or_create(
                    topic=self.topic, user=self.creator
                )
                self.members.add(creator_member)

            # https://stackoverflow.com/a/78053539/13953998
            transaction.on_commit(add_member)

    @property
    def room_name(self):
        return f"Channel-{self.id}"


class TopicChatMessage(models.Model):
    author = models.ForeignKey(TopicMember, null=True, on_delete=models.SET_NULL)
    channel = models.ForeignKey(
        TopicChatChannel, on_delete=models.CASCADE, null=True, blank=True
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)

    MESSAGE_TYPES = [
        ("System Message", 0),
        ("Normal Message", 1),
        ("Reply", 2),
        ("Reply System message", 3),
    ]
    type = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.id:
            self.edited_at = timezone.now()

        super().save(*args, **kwargs)
