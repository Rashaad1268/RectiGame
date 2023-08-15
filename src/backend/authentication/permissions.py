from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserSetPermissions(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, instance):
        if request.user.is_authenticated and view.action in ('update', 'partial_update', 'destroy'):
            if instance.id  != request.user.id and not request.user.is_staff:
                return False

        return super().has_object_permission(request, view, instance)
