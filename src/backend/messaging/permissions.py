from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class TopicChatChannelViewSetPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if view.action in SAFE_METHODS:
                return True

        # Only staff members can modify topic channels
        return request.user.is_staff


class TopicChatMessageViewSetPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        try:
            int(view.kwargs["channel_pk"])
            return super().has_permission(request, view)
        except ValueError:
            raise ValidationError("Invalid channel ID")
