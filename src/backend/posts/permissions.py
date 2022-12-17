from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSetPermissions(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, instance):
        if view.action in ('update', 'partial_update', 'destroy'):
            if instance.author != request.user and not request.user.is_staff:
                return False

        return super().has_object_permission(request, view, instance)
