from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSetPermissions(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if view.action == 'create':
            serializer = view.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if not serializer.validated_data['topic'].members.contains(request.user) \
               and not request.user.is_staff:
                raise PermissionDenied("You are not a member of this topic. "
                                       "You have to join this topic in order to create posts")

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, instance):
        if view.action in ('update', 'partial_update', 'destroy'):
            if instance.author != request.user and not request.user.is_staff:
                return False

        return True

class ReplyViewSetPermissions(PostViewSetPermissions):
    def has_permission(self, request, view):
        return IsAuthenticatedOrReadOnly.has_permission(self, request, view)
