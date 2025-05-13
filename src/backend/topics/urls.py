from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

# The order matters here
# Put more specific patterns at the top
router.register('tags', views.TopicTagViewSet, basename='topic_tag')
router.register('emojis', views.TopicCustomEmojiViewSet, basename='topic_emojis')
router.register('', views.TopicViewSet, basename='topics')


urlpatterns = router.urls
