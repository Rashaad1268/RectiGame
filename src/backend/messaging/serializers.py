from authentication.serializers import UserSerializer
from rest_framework import serializers

from .models import TopicChatChannel, TopicChatMessage


class TopicChatChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatChannel
        fields = ("topic", "name", "description")


class TopicChatChannelSerializer(TopicChatChannelCreateSerializer):
    class Meta(TopicChatChannelCreateSerializer.Meta):
        fields = ("id", "topic", "name", "description", "created_at")


class TopicChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatMessage
        fields = ("author", "content")


class TopicChatMessageSerializer(TopicChatMessageCreateSerializer):
    author = UserSerializer()

    class Meta(TopicChatMessageCreateSerializer.Meta):
        fields = ("id", "author", "channel", "content", "created_at", "edited_at")
