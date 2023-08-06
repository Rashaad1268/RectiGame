from rest_framework import serializers
from authentication.serializers import UserSerializer

from . import models


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('topic', 'title', 'content')


class PostSerializer(PostCreateSerializer):
    author = UserSerializer()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    def get_like_count(self, post):
        return post.likes.count()

    def get_dislike_count(self, post):
        return post.dislikes.count()

    def get_is_liked(self, post):
        request = self.context.get('request')

        if not request:
            return False

        if request and request.user.is_authenticated:
            return post.likes.contains(request.user)

    def get_is_disliked(self, post):
        request = self.context.get('request')

        if not request:
            return False

        if request and request.user.is_authenticated:
            return post.dislikes.contains(request.user)

    class Meta(PostCreateSerializer.Meta):
        fields = ('id', 'topic', 'title', 'content', 'author',
                  'created_at', 'edited_at', 'like_count', 'dislike_count', 'is_liked', 'is_disliked')
