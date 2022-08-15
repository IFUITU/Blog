from rest_framework.routers import DefaultRouter
from main.views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename="post-viewset")
router.register(r"comment", CommentViewSet, basename="comment-viewset")
