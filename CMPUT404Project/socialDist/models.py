from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
# https://www.crunchydata.com/blog/composite-primary-keys-postgresql-and-django
# https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
# https://buildatscale.tech/model-inheritance-in-django/
# https://stackoverflow.com/questions/65895225/django-many-to-one-relationship-with-abstract-entities

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

# Model to store relationships between followers
# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user_id', 'following_user_id')

# Model for a follow request:
class FollowRequest(models.Model):
    sender = models.ForeignKey(User, related_name="send_requests", on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name="recievced_requests", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True)

class Post(models.Model):
    postID = models.CharField(primary_key=True, max_length=40)
    title = models.CharField(max_length=50)
    content = models.BinaryField()
    contentType = models.TextField()
    posterID = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    date = models.DateField()
    visibility = models.CharField(max_length=30)
    unlisted = models.BooleanField()
    isLiked=models.BooleanField(default=False)

    # Modified models by added more fields
    # the server that the post belongs too
    server=models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
 
class Comment(models.Model):
    commentID = models.CharField(primary_key=True, max_length=40)
    content = models.TextField()
    contentType = models.TextField()
    parentPostID = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    date = models.DateField(auto_created=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
    isLiked=models.BooleanField(default=False)

# Model to store a like:
class Like(models.Model):
    likeID = models.CharField(primary_key=True, max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=True)
    dateTime = models.DateTimeField(auto_created=True)

class Inbox(models.Model):
    owner=models.ForeignKey(Author, on_delete=models.CASCADE, related_name="inbox", primary_key=True)
    post=models.ManyToManyField(Post)





