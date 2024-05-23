from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.utils import timezone
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from topics.serializers import TopicSerializer
from topics.models import Topic
from messaging.serializers import NotificationSerializer, TopicChatChannelSerializer
from messaging.models import TopicChatChannel
from .permissions import UserViewSetPermissions
from . import models, serializers


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        login_serializer = serializers.LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **login_serializer.data)

        if user is None:
            return Response(
                {"detail": "Account with the given credentials does not exist"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if user.disabled_until is not None:
            if user.disabled_until > timezone.now():
                return Response(
                    {
                        "detail": "Account is disabled until "
                        + user.disabled_until.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        if not user.is_active:
            return Response(
                {"detail": "User is not active"}, status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response(status=status.HTTP_200_OK)


class SignupView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


def serialize_topic_rooms(user, ctx):
    result = {}

    for topic_room in TopicChatChannel.objects.filter(members__user__id=user.id):
        if topic_room.topic.slug not in result:
            result[topic_room.topic.slug] = [
                TopicChatChannelSerializer(topic_room, context=ctx).data
            ]

        else:
            result[topic_room.topic.slug].append(
                TopicChatChannelSerializer(topic_room, context=ctx).data
            )

    return result


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "put", "patch", "options")
    permission_classes = (UserViewSetPermissions,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all().select_related("profile")

    @action(methods=("GET",), detail=False, url_path="me")
    def get_current_user_data(self, request):
        ctx = self.get_serializer_context()
        user = request.user

        return Response(
            {
                "user": serializers.UserSerializer(user, context=ctx).data,
                "joined_topics": {
                    topic.slug: TopicSerializer(topic, context=ctx).data
                    for topic in Topic.objects.filter(topic_members__user__id=user.id)
                },
                "joined_rooms": serialize_topic_rooms(user, ctx),
                "notifications": NotificationSerializer(
                    models.Notification.objects.filter(user=user).order_by("-id"),
                    many=True,
                ).data,
            }
        )

    def list(self, request):
        raise Http404()
