
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
# from rest_framework import status

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentForCommentSerialzier
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


#CRUD of comment & create comment only for post!
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(post=self.kwargs.get('post_id'))


#To create comment for comment and get list of comments via parent_comment_id!
class CommentForCommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentForCommentSerialzier
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(parent_comment=self.kwargs.get('parent_comment_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AuthorCommentView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(author=self.kwargs.get('author_id'))
