from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.PostsViewSet)

post_replies_router = NestedDefaultRouter(router, "", lookup="posts")
post_replies_router.register("reply", views.ReplyViewSet, basename="post_reply_viewset")

urlpatterns = router.urls + post_replies_router.urls
