from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.viewsets import CustomViewSet

from .models import TopicChatMessage, TopicChatChannel
from .serializers import (TopicChatMessageSerializer,
                          TopicChatMessageCreateSerializer,
                          TopicChatChannelSerializer,
                          TopicChatChannelCreateSerializer)
from . import permissions


class TopicChatChannelViewSet(CustomViewSet):
    queryset = TopicChatChannel.objects.all()
    create_or_update_serializer = TopicChatChannelCreateSerializer
    fetch_serializer  = TopicChatChannelSerializer
    permission_classes = (permissions.TopicChatChannelViewSetPermissions,)


class TopicChatMessageViewSet(CustomViewSet):
    create_or_update_serializer = TopicChatMessageCreateSerializer
    fetch_serializer = TopicChatMessageSerializer
    permission_classes = (permissions.TopicChatMessageViewSetPermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("content", "author", "created_at", "edited_at")

    def get_queryset(self):
        # Order by id instead
        return TopicChatMessage.objects.filter(
                    channel__id=int(self.kwargs["channel_pk"])).order_by('-id')[:50]

    def perform_create(self, serializer):
        return serializer.save(channel_id=int(self.kwargs["channel_pk"]))

    @action(detail=True, url_path="before", methods=("GET",))
    def get_messages_before(self, request, pk, channel_pk):
        """Returns the messages sent before a given message"""
        # Just do the filtering by id instead of created_at
        return Response(
                TopicChatMessageSerializer(
                    TopicChatMessage.objects.filter(channel__id=int(channel_pk),
                    id__lt=self.get_object().id).order_by('-id')[:50],
                    many=True, context={"request": request}).data)
