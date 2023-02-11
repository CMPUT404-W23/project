from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.TextField()
    profileImg = models.TextField()

class Post(models.Model):
    postID = models.CharField(primary_key=True, max_length=40)
    title = models.CharField(max_length=50)
    content = models.BinaryField()
    contentType = models.TextField()
    posterID = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    visibility = models.CharField(max_length=30)
    unlisted = models.BooleanField()

class Comment(models.Model):
    commentID = models.CharField(primary_key=True, max_length=40)
    content = models.TextField()
    contentType = models.TextField()
    parentPostID = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Like(models.Model):
    likeID = models.CharField(primary_key=True, max_length=40)
    likeType = models.CharField(max_length=20)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)