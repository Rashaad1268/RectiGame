from authentication.serializers import UserSerializer
from rest_framework import serializers


from authentication.models import Notification
from .models import TopicChatChannel, TopicChatMessage
from topics.models import TopicMember


# define the TopicMemberSerializer here instead of in topics/serializers.py
# ...due to circular import issue
class TopicMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TopicMember
        fields = (
            "user",
            "topic",
            "nickname",
            "permissions",
            "joined_at",
            "has_left",
        )


class TopicChatChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatChannel
        fields = ("topic", "name", "description")


class TopicChatChannelSerializer(TopicChatChannelCreateSerializer):
    members = serializers.SerializerMethodField()

    def get_members(self, channel):
        if channel.type == 2:
            return TopicMemberSerializer(
                channel.members.all(), many=True, context={"omit_user": True}
            ).data

        else:
            # if the channel type is not a room, then there can be no members
            # so return an empty list
            return []

    class Meta(TopicChatChannelCreateSerializer.Meta):
        fields = (
            "id",
            "type",
            "name",
            "creator",
            "invite_code",
            "topic",
            "members",
            "created_at",
        )


class TopicChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatMessage
        fields = ("author", "content")
        extra_kwargs = {"author": {"allow_null": False}}


class TopicChatMessageSerializer(TopicChatMessageCreateSerializer):
    author = TopicMemberSerializer(context={"omit_user": True})

    class Meta(TopicChatMessageCreateSerializer.Meta):
        fields = (
            "id",
            "type",
            "author",
            "channel",
            "content",
            "created_at",
            "edited_at",
        )
        extra_kwargs = {"author": {"allow_null": True}}


class TopicRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatChannel
        fields = ("name", "topic", "description")


# creating the notification serializer in authentication/models will cause a circular import error
# so, define the notification serializer here even though it doesn't fully belong here
class NotificationSerializer(serializers.ModelSerializer):
    referenced_message = TopicChatMessageSerializer()

    class Meta:
        model = Notification
        fields = (
            "id",
            "type",
            "created_at",
            "notification_content",
            "referenced_message",
        )


class WebSocketActionSerializer(serializers.Serializer):
    a = serializers.CharField()  # a: action
    d = serializers.JSONField(required=False)  # d: data
