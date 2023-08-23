from django.urls import path

from .consumers import ChatConsumer


urlpatterns = []

websocket_urlpatterns = [
    path("api/ws/", ChatConsumer.as_asgi())
]
