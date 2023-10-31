from django.urls import path, include
from rest_framework_nested import routers

from .views import TopicChatMessageViewSet, TopicChatChannelViewSet
from .consumers import ChatConsumer

router = routers.SimpleRouter()
router.register('', TopicChatChannelViewSet)

messages_router = routers.NestedSimpleRouter(router, r'', lookup='channel')
messages_router.register(r'messages', TopicChatMessageViewSet, basename='topic_chat_messages_viewset')

urlpatterns = router.urls + messages_router.urls

websocket_urlpatterns = [
    path("api/ws/", ChatConsumer.as_asgi())
]
