import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


from topics.models import Topic
# from .serializers import UserSerializer, ChatGroupSerializer



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            return self.close()

        user.is_online = True
        user.save()
        self.accept()

        for topic in Topic.objects.filter(members__id=user.id):
            async_to_sync(self.channel_layer.group_add)(
                topic.channel_name,
                self.channel_name
            )

    def disconnect(self, close_code):
        user = self.scope["user"]
        
        if user.is_anonymous:
            return

        for topic in Topic.objects.filter(members__id=user.id):
            async_to_sync(self.channel_layer.group_add)(
                topic.channel_name,
                self.channel_name
            )

        self.scope["user"].is_online = False
        self.scope["user"].save()

    def dispatch_named_event(self, event_name, payload, extra_params={}):
        """A helper function to dispatch an event with a name specified"""
        print(self.scope)
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
