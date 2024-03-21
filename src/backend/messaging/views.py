from django.http import Http404
from rest_framework import pagination, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from backend.viewsets import CustomViewSet

from .models import TopicChatMessage, TopicChatChannel
from .serializers import (
    TopicChatMessageSerializer,
    TopicChatMessageCreateSerializer,
    TopicChatChannelSerializer,
    TopicChatChannelCreateSerializer,
    TopicRoomCreateSerializer,
    TopicChatChannelSerializer,
)
from . import permissions


class TopicChatChannelViewSet(CustomViewSet):
    create_or_update_serializer = TopicChatChannelCreateSerializer
    fetch_serializer = TopicChatChannelSerializer
    permission_classes = (permissions.TopicChatChannelViewSetPermissions,)

    def get_queryset(self):
        return (
            TopicChatChannel.objects.filter(type=1)
            | self.request.user.topic_room_member.all()
        )

    def list(self, request, *args, **kwargs):
        raise Http404()


class MessagePaginator(pagination.BasePagination):
    page_size = 50
    count: int

    def paginate_queryset(self, queryset, request, view=None):
        # Get the total count
        self.count = queryset.count()

        return list(queryset[: self.page_size])

    def get_paginated_response(self, data):
        # We don't need `previous` and `next` links
        # since we have the `before` url parameter
        return Response({"count": self.count, "results": data})


class ChatMessageFilter(filters.FilterSet):
    # Get the messages sent before a certain message
    before = filters.NumberFilter(field_name="id", lookup_expr="lt")

    class Meta:
        model = TopicChatMessage
        fields = ("content", "author", "created_at", "edited_at")


class TopicChatMessageViewSet(CustomViewSet):
    create_or_update_serializer = TopicChatMessageCreateSerializer
    fetch_serializer = TopicChatMessageSerializer
    permission_classes = (permissions.TopicChatMessageViewSetPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChatMessageFilter
    pagination_class = MessagePaginator

    def get_queryset(self):
        return TopicChatMessage.objects.filter(
            channel__id=int(self.kwargs["channel_pk"])
        ).order_by("-id")

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            channel=get_object_or_404(
                TopicChatChannel, id=int(self.kwargs["channel_pk"])
            ),
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # No need to return anything from this endpoint
        return Response(status=status.HTTP_201_CREATED)


class TopicRoomViewSet(CustomViewSet):
    create_or_update_serializer = TopicRoomCreateSerializer
    fetch_serializer = TopicChatChannelSerializer
    permission_classes = (permissions.TopicRoomViewSetPermissions,)

    def get_queryset(self):
        return self.request.user.topic_room_member.all()

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if not topic.members.contains(self.request.user):
            raise exceptions.PermissionDenied(
                "You need to join a topic in order to create a room in that topic"
            )

        # type=2 means that the channel is a room channel
        return serializer.save(creator=self.request.user, type=2)

    @action(detail=True, methods=("POST",), url_path="join")
    def join_topic_room(self, request, pk):
        # pk is actually the invite code of the topic room
        room = get_object_or_404(TopicChatChannel, invite_code=pk)

        if not room.topic.members.contains(request.user):
            # add the user to the rooms topic if they already aren't one
            room.topic.members.add(request.user)

        if not room.members.contains(request.user):
            room.members.add(self.request.user)

        return Response(
            TopicChatChannelSerializer(
                room, context=self.get_serializer_context()
            ).data
        )

    @action(detail=True, methods=("POST",), url_path="leave")
    def leave_topic_room(self, request, pk):
        topic_room = get_object_or_404(TopicChatChannel, invite_code=pk)

        if topic_room.creator == request.user:
            return Response(
                {"detail": "Topic room creator cannot leave their room"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if topic_room.members.contains(request.user):
            topic_room.members.remove(self.request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=("GET",), url_path="invite-details")
    def get_invite_details(self, request, pk):
        topic_room = get_object_or_404(TopicChatChannel, invite_code=pk)

        return Response(
            {
                **TopicChatChannelSerializer(
                    topic_room, context=self.get_serializer_context()
                ).data,
                "is_member": topic_room.members.contains(request.user),
            }
        )
