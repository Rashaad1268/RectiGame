from django.urls import path
from rest_framework_nested import routers

from .views import TopicChatMessageViewSet, TopicChatChannelViewSet, TopicRoomViewSet
from .consumers import ChatConsumer

router = routers.DefaultRouter()
router.register(
    "rooms", TopicRoomViewSet, basename="topic_chat_room_viewset"
)  # register the room viewset first, so it is given priority
router.register("", TopicChatChannelViewSet, basename="topic_chat_channels")

channels_router = routers.NestedSimpleRouter(router, r"", lookup="channel")
channels_router.register(
    r"messages", TopicChatMessageViewSet, basename="topic_chat_messages_viewset"
)
urlpatterns = router.urls + channels_router.urls

websocket_urlpatterns = [path("api/ws/", ChatConsumer.as_asgi())]
