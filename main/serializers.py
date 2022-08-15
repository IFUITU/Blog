from rest_framework import serializers
from .models import Post, Comment, Images
# from mysite.helpers.helpers import clean_slug  #to take titel as clear slug


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("id","author",)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("parent_comment",)
        read_only_fields = ("id","author",)

    def validate(self, attrs):
        if not attrs['post']:
            raise serializers.ValidationError("Post field can not be empty!")
        return super().validate(attrs)


class CommentForCommentSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("post",)
        read_only_fields = ("id", "author", )

    def validate(self, attrs):
        if not attrs['parent_comment']:
            raise serializers.ValidationError("Parent comment field can not be empty!")
        return super().validate(attrs)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"