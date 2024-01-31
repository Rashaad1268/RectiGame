import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from topics.models import Topic
from .serializers import WebSocketActionSerializer
# from .serializers import UserSerializer, ChatGroupSerializer



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            return self.close()

        user.is_online = True
        user.channel_name = self.channel_name
        user.save()

        for topic in Topic.objects.filter(members__id=user.id):
            async_to_sync(self.channel_layer.group_add)(
                topic.channel_name,
                self.channel_name
            )

        self.accept()

    def disconnect(self, close_code):
        user = self.scope["user"]

        if user.is_anonymous:
            return

        for topic in Topic.objects.filter(members__id=user.id):
            async_to_sync(self.channel_layer.group_discard)(
                topic.channel_name,
                self.channel_name
            )

        user.is_online = False
        user.last_online = timezone.now()
        user.save()

    def dispatch_named_event(self, event_name, payload, extra_params={}):
        """A helper function to dispatch an event with a name specified"""
        data = {
            "e": event_name.upper(),
            "d": payload,
            **extra_params
        }
        self.send(text_data=json.dumps(data))

    def message_create(self, event):
        self.dispatch_named_event("MESSAGE_CREATE", event["data"])

    def message_delete(self, event):
        self.dispatch_named_event("MESSAGE_DELETE", event["data"])

    def message_update(self, event):
        self.dispatch_named_event("MESSAGE_UPDATE", event["data"])

    def channel_create(self, event):
        self.dispatch_named_event("CHANNEL_CREATE", event["data"])

    def channel_update(self, event):
        self.dispatch_named_event("CHANNEL_UPDATE", event["data"])

    def channel_delete(self, event):
        self.dispatch_named_event("CHANNEL_DELETE", event["data"])

    def member_join(self, event):
        self.dispatch_named_event("MEMBER_JOIN", event["data"])

    def member_update(self, event):
        self.dispatch_named_event("MEMBER_UPDATE", event["data"])

    def member_leave(self, event):
        self.dispatch_named_event("MEMBER_LEAVE", event["data"])

    def receive(self, text_data=None, bytes_data=None):
        try:
            serializer = WebSocketActionSerializer(data=json.loads(text_data))
        except json.decoder.JSONDecodeError:
            return

        if not serializer.is_valid():
            return

        data = serializer.data

        match data["a"].upper():
            case "SUBSCRIBE_TO_TOPIC":
                topic_slug = data["d"].get("topic_slug")

                if topic_slug and Topic.objects.filter(slug=topic_slug).exists():
                    async_to_sync(self.channel_layer.group_add)(
                        f"Topic-{topic_slug}",
                        self.channel_name
                    )

            case "UNSUBSCRIBE_FROM_TOPIC":
                topic_slug = data["d"].get("topic_slug")

                if topic_slug and Topic.objects.filter(slug=topic_slug).exists():
                    async_to_sync(self.channel_layer.group_discard)(
                        f"Topic-{topic_slug}",
                        self.channel_name
                    )
