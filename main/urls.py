from django.urls import path
from .views import PostCommentView, AuthorCommentView, CommentForCommentView

app_name = "main"

urlpatterns = [
    path('post-comments/<int:post_id>/', PostCommentView.as_view(), name="post-comment"),
    path("author-comments/<int:author_id>/", AuthorCommentView.as_view(), name="author-comment"),
    path("comment-for-comments/<int:parent_comment_id>/", CommentForCommentView.as_view(), name="comment-for-comment"),
]