from rest_framework import serializers

from messaging.models import TopicChatChannel
from messaging.serializers import TopicChatChannelSerializer, TopicMemberSerializer

from .models import Topic, TopicTag, TopicMember, CustomTopicEmoji


class TopicTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTag
        fields = ("name",)


class TopicTagSerializer(TopicTagCreateSerializer):
    class Meta(TopicTagCreateSerializer.Meta):
        fields = ("name", "slug")


class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("name", "description", "image", "banner", "tags")


class TopicSerializer(TopicCreateSerializer):
    tags = TopicTagSerializer(many=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    channels = serializers.SerializerMethodField()
    me = serializers.SerializerMethodField()

    def get_member_count(self, topic):
        return TopicMember.objects.filter(topic=topic).count()

    def get_channels(self, topic):
        return TopicChatChannelSerializer(
            TopicChatChannel.objects.filter(topic=topic, type=1),
            many=True,
            context=self.context,
        ).data

    def get_is_member(self, topic):
        request = self.context.get("request")
        if request is not None and request.user.is_authenticated:
            return TopicMember.objects.filter(
                topic=topic, user=self.context["request"].user, has_left=False
            ).exists()
        return False
    
    def get_me(self, topic):
        request = self.context.get("request")
        if request is not None and request.user.is_authenticated:
            member = topic.topic_members.filter(user=request.user, has_left=False).first()

            if member:
                return TopicMemberSerializer(member).data

        return None

    class Meta(TopicCreateSerializer.Meta):
        fields = (
            "name",
            "slug",
            "description",
            "icon",
            "image",
            "banner",
            "created_at",
            "tags",
            "member_count",
            "is_member",
            "channels",
            "me",
        )


class CustomTopicEmojiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTopicEmoji
        fields = ("topic", "name", "image")

class CustomTopicEmojiSerializer(CustomTopicEmojiCreateSerializer):
    class Meta(CustomTopicEmojiCreateSerializer.Meta):
        fields = ("id", "topic", "name", "image", "created_by", "created_at")
