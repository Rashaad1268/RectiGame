from authentication.serializers import UserSerializer
from rest_framework import serializers

from authentication.models import Notification
from .models import TopicChatChannel, TopicChatMessage, TopicRoom


class TopicChatChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatChannel
        fields = ("topic", "name", "description")


class TopicChatChannelSerializer(TopicChatChannelCreateSerializer):
    class Meta(TopicChatChannelCreateSerializer.Meta):
        fields = ("id", "name", "description", "created_at")


class TopicChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatMessage
        fields = ("author", "content")
        extra_kwargs = {"author": {"allow_null": False}} 


class TopicChatMessageSerializer(TopicChatMessageCreateSerializer):
    author = UserSerializer()

    class Meta(TopicChatMessageCreateSerializer.Meta):
        fields = ("id", "author", "channel", "content", "created_at", "edited_at")
        extra_kwargs = {"author": {"allow_null": True}} 


class TopicRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicRoom
        fields = ("name", "topic")


class TopicRoomSerializer(TopicRoomCreateSerializer):
    members = UserSerializer(many=True)

    class Meta(TopicRoomCreateSerializer.Meta):
        fields = ("id", "name", "creator", "code", "topic", "members", "created_at")


# creating the notification serializer in authentication/models will cause a recursive import error
# so, define the notification serializer here even though it doesn't fully belong here
class NotificationSerializer(serializers.ModelSerializer):
    referenced_message = TopicChatMessageSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'type', 'created_at', 'notification_content', 'referenced_message')


class WebSocketActionSerializer(serializers.Serializer):
    a = serializers.CharField()  # a: action
    d = serializers.JSONField(required=False)  # d: data
