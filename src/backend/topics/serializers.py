from rest_framework import serializers

from messaging.models import TopicChatChannel
from messaging.serializers import TopicChatChannelSerializer

from .models import Topic, TopicTag


class TopicTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTag
        fields = ('name',)


class TopicTagSerializer(TopicTagCreateSerializer):
    class Meta(TopicTagCreateSerializer.Meta):
        fields = ('name', 'slug')


class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name', 'description', 'image', 'banner', 'tags')


class TopicSerializer(TopicCreateSerializer):
    tags = TopicTagSerializer(many=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    channels = serializers.SerializerMethodField()

    def get_member_count(self, topic):
        return topic.members.count()
    
    def get_channels(self, topic):
        return TopicChatChannelSerializer(TopicChatChannel.objects.filter(topic=topic), many=True).data

    def get_is_member(self, topic):
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            return topic.members.contains(self.context['request'].user)
        return False

    class Meta(TopicCreateSerializer.Meta):
        fields = ('name', 'slug', 'description', 'image', 'banner',
                  'created_at', 'tags', 'member_count', 'is_member', 'channels')
