from rest_framework import viewsets, pagination, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer, PostCreateSerializer
from .models import Post
from . import permissions


class PostPaginator(pagination.PageNumberPagination):
    page_size = 30


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (permissions.PostViewSetPermissions,)
    pagination_class = PostPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('topic',)

    def get_serializer_class(self):
        if self.action.lower() in ('create', 'partial_update', 'update', 'delete'):
            return PostCreateSerializer
        else:
            return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data['topic'].members.contains(request.user) and not request.user.is_staff:
            return Response({'detail': 'You are not a member of this topic'}, status=status.HTTP_403_FORBIDDEN)

        instance = serializer.save(author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(PostSerializer(instance).data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(PostSerializer(instance).data)

    @action(detail=True, methods=('post',), url_path='like', permission_classes=(IsAuthenticated,))
    def like_post(self, request, pk):
        post = self.get_object()

        if not post.likes.contains(request.user):
            if post.dislikes.contains(request.user):
                post.dislikes.remove(request.user)

            post.likes.add(request.user)

        else:
            return Response({'detail': "User has already liked the post"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('post',), url_path='unlike', permission_classes=(IsAuthenticated,))
    def unlike_post(self, request, pk):
        post = self.get_object()

        if post.likes.contains(request.user):
            post.likes.remove(request.user)

        else:
            return Response({'detail': "User has not liked the post to unlike"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post',), url_path='dislike', permission_classes=(IsAuthenticated,))
    def dislike_post(self, request, pk):
        post = self.get_object()

        if not post.dislikes.contains(request.user):
            if post.likes.contains(request.user):
                post.likes.remove(request.user)

            post.dislikes.add(request.user)

        else:
            return Response({'detail': "User has already disliked the post"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
 
    @action(detail=True, methods=('post',), url_path='undo-dislike', permission_classes=(IsAuthenticated,))
    def undo_dislike_post(self, request, pk):
        post = self.get_object()

        if post.dislikes.contains(request.user):
            post.dislikes.remove(request.user)

        else:
            return Response({'detail': "User has not disliked the post to undo the dislike"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
