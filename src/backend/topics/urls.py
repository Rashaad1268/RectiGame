from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

# The order matters here
# Put more specific patterns at the top
router.register('tags', views.TopicTagViewSet, basename='topic_tag')
router.register('', views.TopicViewSet, basename='topics')

topics_router = routers.NestedSimpleRouter(router, r"", lookup="topic")
topics_router.register(
    r"emojis", views.TopicCustomEmojiViewSet, basename="topic_custom_emoji_viewset"
)


urlpatterns = router.urls + topics_router.urls
