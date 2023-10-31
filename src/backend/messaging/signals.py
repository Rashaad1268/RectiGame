from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from topics.models import Topic

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
def dispatch_mesage_delete(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        instance.channel.topic.channel_name,
        {"type": "message_delete", "data": {"id": instance.id, "channel_id": instance.channel.id}},
    )


@receiver(post_save, sender=models.TopicChatChannel)
def dispatch_channel_create_and_edit(sender, instance, created, **kwargs):
    async_to_sync(channel_layer.group_send)(
        instance.topic.channel_name,
        {
            "type": "channel_create" if created else "channel_update",
            "data": TopicChatChannelSerializer(instance).data,
        },
    )


@receiver(pre_delete, sender=models.TopicChatChannel)
def dispatch_channel_delete(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        instance.topic.channel_name,
        {"type": "channel_delete", "data": {"id": instance.id, "topic": instance.topic.slug}},
    )
