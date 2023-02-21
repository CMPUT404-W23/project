from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.TextField()
    profileImg = models.TextField()

    # Modified models by added more fields
    # classify admin from other regualar authors
    isServerAdmin=models.BooleanField(default=False)
    # future admin fucntionalities (to be added)

    # check authenticatd user
    isAuthenticated=models.BooleanField(default=False)
    # check friends status
    # Self-reference: Can't set it to false, left it true for now
    isFriendWith=models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    # check whether the author in a server or not
    inServer=models.ForeignKey('Server', blank='True', on_delete=models.SET_NULL, null=True)

# Added server class for admins to host content
class Server(models.Model):
    # server id as primary key
    serverID=models.Field(primary_key=True)
    # owner=server admin
    owner=models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    # server name
    serverName=models.CharField(max_length=50)

class Post(models.Model):
    postID = models.CharField(primary_key=True, max_length=40)
    title = models.CharField(max_length=50)
    content = models.BinaryField()
    contentType = models.TextField()
    posterID = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    visibility = models.CharField(max_length=30)
    unlisted = models.BooleanField()

    # Modified models by added more fields
    # the server that the post belongs too
    server=models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    # whether the post is liked or not
    isLiked=models.BooleanField(default=False)

class Comment(models.Model):
    commentID = models.CharField(primary_key=True, max_length=40)
    content = models.TextField()
    contentType = models.TextField()
    parentPostID = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # Modified models by added more fields
    # whether the comment is liked or not
    isLiked=models.BooleanField(default=False)

class Like(models.Model):
    likeID = models.CharField(primary_key=True, max_length=40)
    likeType = models.CharField(max_length=20)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

class Inbox(models.Model):
    # EDIT: 
    owner=models.ForeignKey(Author, on_delete=models.CASCADE)
    # likes, posts
    post=models.ManyToManyField(Post)
    like=models.ManyToManyField(Like)
    comment=models.ManyToManyField(Comment)

    # inbox content and its type
    content = models.TextField()
    contentType = models.TextField()