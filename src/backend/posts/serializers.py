from rest_framework import serializers
from authentication.serializers import UserSerializer
from messaging.serializers import TopicMemberSerializer

from . import models


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ("topic", "title", "content")


class PostSerializer(PostCreateSerializer):
    author = TopicMemberSerializer()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    def get_like_count(self, post):
        return post.likes.count()

    def get_dislike_count(self, post):
        return post.dislikes.count()

    def get_is_liked(self, post):
        request = self.context.get("request")

        if not request:
            return False

        if request and request.user.is_authenticated:
            return post.likes.contains(request.user)

    def get_is_disliked(self, post):
        request = self.context.get("request")

        if not request:
            return False

        if request and request.user.is_authenticated:
            return post.dislikes.contains(request.user)

    class Meta(PostCreateSerializer.Meta):
        fields = (
            "id",
            "topic",
            "title",
            "content",
            "author",
            "created_at",
            "edited_at",
            "like_count",
            "dislike_count",
            "is_liked",
            "is_disliked",
        )


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reply
        fields = ("post", "content")


class ReplySerializer(ReplyCreateSerializer):
    # post = PostSerializer()
    author = UserSerializer()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    replying_to = serializers.SerializerMethodField()

    def get_replying_to(self, reply):
        return ReplySerializer(reply.replying_to, context=self.context).data

    def get_like_count(self, reply):
        return reply.likes.count()

    def get_dislike_count(self, reply):
        return reply.dislikes.count()

    def get_is_liked(self, reply):
        request = self.context.get("request")

        if not request:
            return False

        if request and request.user.is_authenticated:
            return reply.likes.contains(request.user)

    def get_is_disliked(self, reply):
        request = self.context.get("request")

        if not request:
            return False

        if request and request.user.is_authenticated:
            return reply.dislikes.contains(request.user)

    class Meta(ReplyCreateSerializer.Meta):
        # No need to include the post, I think
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "edited_at",
            "replying_to",
            "like_count",
            "dislike_count",
            "is_liked",
            "is_disliked",
        )
