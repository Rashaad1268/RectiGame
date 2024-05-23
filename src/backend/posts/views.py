from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.viewsets import CustomViewSet

from . import permissions
from .models import Post, Reply
from .serializers import (
    PostCreateSerializer,
    PostSerializer,
    ReplyCreateSerializer,
    ReplySerializer,
)


class PostPaginator(pagination.PageNumberPagination):
    page_size = 30


class PostsViewSet(CustomViewSet):
    queryset = Post.objects.all().select_related("topic", "author")
    permission_classes = (permissions.PostViewSetPermissions,)
    pagination_class = PostPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("topic",)
    create_or_update_serializer = PostCreateSerializer
    fetch_serializer = PostSerializer

    def perform_create(self, serializer):
        print()
        return serializer.save(
            author=serializer.validated_data["topic"].topic_members.get(
                user=self.request.user
            )
        )

    @action(
        detail=True,
        methods=("post",),
        url_path="like",
        permission_classes=(IsAuthenticated,),
    )
    def like_post(self, request, pk):
        post = self.get_object()

        if not post.likes.contains(request.user):
            if post.dislikes.contains(request.user):
                post.dislikes.remove(request.user)

            post.likes.add(request.user)

        else:
            return Response(
                {"detail": "User has already liked the post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post",),
        url_path="unlike",
        permission_classes=(IsAuthenticated,),
    )
    def unlike_post(self, request, pk):
        post = self.get_object()

        if post.likes.contains(request.user):
            post.likes.remove(request.user)

        else:
            return Response(
                {"detail": "User has not liked the post to unlike"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=("post",),
        url_path="dislike",
        permission_classes=(IsAuthenticated,),
    )
    def dislike_post(self, request, pk):
        post = self.get_object()

        if not post.dislikes.contains(request.user):
            if post.likes.contains(request.user):
                post.likes.remove(request.user)

            post.dislikes.add(request.user)

        else:
            return Response(
                {"detail": "User has already disliked the post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post",),
        url_path="undo-dislike",
        permission_classes=(IsAuthenticated,),
    )
    def undo_dislike_post(self, request, pk):
        post = self.get_object()

        if post.dislikes.contains(request.user):
            post.dislikes.remove(request.user)

        else:
            return Response(
                {"detail": "User has not disliked the post to undo the dislike"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyViewSet(CustomViewSet):
    queryset = Reply.objects.all()
    permission_classes = (permissions.ReplyViewSetPermissions,)
    pagination_class = PostPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("replying_to", "content", "post", "author")
    create_or_update_serializer = ReplyCreateSerializer
    fetch_serializer = ReplySerializer

    @action(
        detail=True,
        methods=("post",),
        url_path="like",
        permission_classes=(IsAuthenticated,),
    )
    def like_reply(self, request, pk):
        reply = self.get_object()

        if not reply.likes.contains(request.user):
            if reply.dislikes.contains(request.user):
                reply.dislikes.remove(request.user)

            reply.likes.add(request.user)

        else:
            return Response(
                {"detail": "User has already liked the reply"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post",),
        url_path="unlike",
        permission_classes=(IsAuthenticated,),
    )
    def unlike_reply(self, request, pk):
        reply = self.get_object()

        if reply.likes.contains(request.user):
            reply.likes.remove(request.user)

        else:
            return Response(
                {"detail": "User has not liked the reply to unlike"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=("post",),
        url_path="dislike",
        permission_classes=(IsAuthenticated,),
    )
    def dislike_reply(self, request, pk):
        post = self.get_object()

        if not post.dislikes.contains(request.user):
            if post.likes.contains(request.user):
                post.likes.remove(request.user)

            post.dislikes.add(request.user)

        else:
            return Response(
                {"detail": "User has already disliked the reply"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post",),
        url_path="undo-dislike",
        permission_classes=(IsAuthenticated,),
    )
    def undo_dislike_reply(self, request, pk):
        post = self.get_object()

        if post.dislikes.contains(request.user):
            post.dislikes.remove(request.user)

        else:
            return Response(
                {"detail": "User has not disliked the reply to undo the dislike"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
