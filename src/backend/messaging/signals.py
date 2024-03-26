from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from authentication.serializers import UserSerializer
from authentication.models import User

from . import models
from .serializers import TopicChatChannelSerializer, TopicChatMessageSerializer

channel_layer = get_channel_layer()


@receiver(post_save, sender=models.Topic)
def create_topic_chat_channel(sender, instance, created, **kwargs):
    if created:
        models.TopicChatChannel(
            name="main",
            description=f"The main channel for {instance.name}",
            topic=instance,
        ).save()


@receiver(post_save, sender=models.TopicChatMessage)
def dispatch_message_create_and_edit(sender, instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)(
        instance.channel.topic.channel_name,
        {
            "type": "message_create" if created else "message_update",
            "data": TopicChatMessageSerializer(instance).data,
        },
    )


@receiver(pre_delete, sender=models.TopicChatMessage)
def dispatch_message_delete(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        instance.channel.topic.channel_name,
        {
            "type": "message_delete",
            "data": {"id": instance.id, "channel_id": instance.channel.id},
        },
    )


@receiver(post_save, sender=models.TopicChatChannel)
def dispatch_channel_create_and_edit(sender, instance, created, **kwargs):
    is_topic_room = instance.type == 2

    if is_topic_room and created:
        # there is no ws event for the creation of rooms
        return

    topic_room_or_channel = "topic_room" if is_topic_room else "channel"

    async_to_sync(channel_layer.group_send)(
        instance.room_name if is_topic_room else instance.topic.channel_name,
        {
            "type": (
                "channel_create" if created else f"{topic_room_or_channel}_update"
            ),
            "data": TopicChatChannelSerializer(instance).data,
        },
    )


@receiver(pre_delete, sender=models.TopicChatChannel)
def dispatch_channel_delete(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        instance.topic.channel_name,
        {
            "type": "channel_delete",
            "data": {"id": instance.id, "topic": instance.topic.slug},
        },
    )


@receiver(m2m_changed, sender=models.TopicChatChannel.members.through)
def dispatch_room_member_join(instance, action, pk_set, model, **kwargs):
    if action == "post_add" and model == User:
        # here instance will be the topic chat channel instance
        for user_id in pk_set:
            async_to_sync(channel_layer.group_send)(
                instance.room_name,
                {
                    "type": "room_member_join",
                    "data": {
                        "user": UserSerializer(User.objects.get(id=user_id)).data,
                        "room": TopicChatChannelSerializer(instance).data,
                    },
                },
            )
