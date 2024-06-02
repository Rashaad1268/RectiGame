from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, pagination, status

from backend.viewsets import CustomViewSet
from messaging.serializers import TopicMemberSerializer

from . import serializers
from .models import Topic, TopicTag, TopicMember, CustomTopicEmoji


class Paginator(pagination.PageNumberPagination):
    page_size = 30


class TopicTagViewSet(CustomViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = TopicTag.objects.all()
    lookup_field = "slug"
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name", "slug")
    create_or_update_serializer = serializers.TopicTagCreateSerializer
    fetch_serializer = serializers.TopicTagSerializer


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Topic.objects.all().order_by("?")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name", "slug", "tags")
    pagination_class = Paginator
    serializer_class = serializers.TopicSerializer

    @action(
        detail=True,
        methods=("POST",),
        url_path="join",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def join_topic(self, request, pk):
        topic = self.get_object()

        try:
            # If a topic member instance already exists for this user
            # then just set joined_at to False
            topic_member = topic.topic_members.get(user=request.user)

            if topic_member.has_left is False:
                return Response({"detail": "User is already a member of this topic"})

            topic_member.has_left = False
            topic_member.joined_at = timezone.now()
            topic_member.save()

        except TopicMember.DoesNotExist:
            # else, create a new topic member instance for this user
            topic_member = topic.topic_members.create(user=request.user)

        return Response(TopicMemberSerializer(topic_member).data)

    @action(
        detail=True,
        methods=("POST",),
        url_path="leave",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def leave_topic(self, request, pk):
        topic = self.get_object()

        try:
            topic_member = topic.topic_members.get(user=request.user, has_left=False)
            topic_member.nickname = None
            topic_member.has_left = True
            topic_member.save()

        except TopicMember.DoesNotExist:
            return Response(
                {"detail": "User is not a member of this topic to be removed from"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class TopicCustomEmojiViewSet(CustomViewSet):
    create_or_update_serializer = serializers.CustomTopicEmojiCreateSerializer
    fetch_serializer = serializers.CustomTopicEmojiSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return CustomTopicEmoji.objects.filter(
            topic__slug=self.kwargs["topic_pk"]
        ).order_by("-id")
