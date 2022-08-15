from django.db import models
from mysite.helpers.helpers import UploadTo


class BaseAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract  = True


class Post(BaseAbstractModel):
    author = models.ForeignKey("client.User", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=256)
    file  = models.FileField(upload_to=UploadTo("post_files"), null=True, blank=True)
    content = models.TextField()


class Comment(BaseAbstractModel):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey("client.User", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.author.email


class Images(BaseAbstractModel):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=UploadTo('post_imges'), blank=True, null=True)
    image_title = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.post.title
