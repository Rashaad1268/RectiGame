from rest_framework import viewsets, permissions, pagination, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from backend.viewsets import CustomViewSet

from . import serializers
from .models import TopicTag, Topic


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
        methods=["post"],
        url_path="join",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def join_topic(self, request, pk):
        topic = self.get_object()

        if not topic.members.contains(request.user):
            topic.members.add(request.user)

        else:
            return Response({"detail": "User is already a member of this topic"})

        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["post"],
        url_path="leave",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def leave_topic(self, request, pk):
        topic = self.get_object()

        if topic.members.contains(request.user):
            topic.members.remove(request.user)

        else:
            return Response(
                {"detail": "User is not a member of this topic to be removed from"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
