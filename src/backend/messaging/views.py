from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import pagination, status

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



class MessagePaginator(pagination.BasePagination):
    page_size = 50
    count: int

    def paginate_queryset(self, queryset, request, view=None):
        # Get the total count
        self.count = queryset.count()

        return list(queryset[:self.page_size])

    def get_paginated_response(self, data):
        # We don't need `previous` and `next` links
        # since we have the `before` url parameter
        return Response({
            "count": self.count,
            "results": data
        })


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

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def get_queryset(self):
        return TopicChatMessage.objects.filter(
                channel__id=int(self.kwargs["channel_pk"])).order_by('-id')

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, channel_id=int(self.kwargs["channel_pk"]))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(status=status.HTTP_201_CREATED)
