from typing import Optional
from rest_framework import status, viewsets, serializers
from rest_framework.response import Response


class CustomViewSet(viewsets.ModelViewSet):
    create_or_update_serializer: Optional[serializers.Serializer] = None
    fetch_serializer: Optional[serializers.Serializer] = None

    def get_serializer_class(self):
        if (
            self.create_or_update_serializer is None
            or self.fetch_serializer is None
        ):
            raise NotImplementedError(
                "Specify create_or_update_serializer and fetch_serializer or "
                "override the get_serializer_class() method"
            )

        if self.action.lower() in ("create", "partial_update", "update", "delete"):
            return self.create_or_update_serializer
        else:
            return self.fetch_serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.fetch_serializer(instance, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            self.fetch_serializer(instance, context={"request": request}).data
        )

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        return serializer.save()
