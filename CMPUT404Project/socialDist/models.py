from django.db import models
from django.contrib.auth.models import User
# Added array field to handle categories in post
# https://stackoverflow.com/questions/4294039/how-can-i-store-an-array-of-strings-in-a-django-model
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/


# Changes towards Author (02/28)
# - Added authorId, displayName
# - Commented/ (later will delete): isServerAdmin, isAuthenticated
# Current Own Fields: user, authorId, displayName, github, profileImg
# Current foreignkey fields: inServer, isFriendWith (nore sure to keep or not)

class Author(models.Model):
    # user: one to one field 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # authorID: ID of the author
    authorId=models.CharField(primary_key=True, max_length=40)
    # Don't need host and url field, those come from authorId

    # Added displayName field, default as empty string
    displayName=models.CharField(default="", max_length=40)

    # github and profileImage fields
    github = models.TextField()
    profileImage = models.TextField()


    # Fields referenced other models externally
    # check whether the author in a server or not
    inServer=models.ForeignKey('Server', blank='True', on_delete=models.SET_NULL, null=True)

    # Not sure to keep or not
    # Check friends status; self-reference: Can't set it to false, left it true for now
    isFriendWith=models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    """
    # PLAN TO DELETE isServerAdmin, not sure is it safe to delete so will keep it for now
    # No longer need because server admin will be a superuser

    # Modified models by added more fields
    # classify admin from other regualar authors
    isServerAdmin=models.BooleanField(default=False)
    # future admin fucntionalities (to be added)
    """
    """
    # PLAN TO DELETE isAuthenticated, not sure is it safe to delete so will keep it for now
    # No longer need because the authentication will be handled elsewhere
    # check authenticatd user (TO BE REMOVE)
    isAuthenticated=models.BooleanField(default=False)
    """

# Changes towards Server (02/28):
# No changes this time
# Current Own Fields: user, serverID, owner, serverName
# Current foreignkey fields: N/A
class Server(models.Model):
    # server id as primary key
    serverID=models.CharField(primary_key=True, max_length=40)
    # owner=server admin
    owner=models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    # server name
    serverName=models.CharField(max_length=50)

# Changes towards Post (02/28):
# - Added fields: source, origin, categories, count
# - changed name: content (to description), date (to published), server (to inServer), posterID (to author)
# - Commented/ (later will delete): N/A
# Current Own Fields: postID, title, source, origin, description, contentType, posterID, categories, count, published, visibility, unlisted, inServer, isLiked
# Current foreignkey fields: inServer, isLiked
class Post(models.Model):
    postID = models.CharField(primary_key=True, max_length=40)
    title = models.CharField(max_length=50)
    # Added source, origin
    source=models.CharField(max_length=50)
    origin=models.CharField(max_length=50)
    # change name from content to description to fit with requirements
    # content = models.BinaryField()
    description = models.TextField()
    contentType = models.TextField()

    # author to access the author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # added categories: use arrayfield from postgres
    # categories=ArrayField(models.CharField(max_length=50), default=list)
    # OR
    categories=models.CharField(max_length=100)

    # Added count
    count=models.IntegerField()

    # changed date to published to fit the requirement
    # date=models.DateField()
    published = models.DateField()
    # changed the field from CharField to ArrayField
    # visibility = ArrayField(models.CharField(max_length=50), default=list)
    # OR
    visibility=models.CharField(max_length=100)
    unlisted = models.BooleanField()

    # Foreignkey fields:
    # the server that the post belongs too
    inServer=models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    # whether the post is liked or not
    isLiked=models.BooleanField(default=False)

# Changes towards Comment (02/28):
# - Added fields: author
# - changed name:  date (to published)
# - Commented/ (later will delete): N/A
# Current Own Fields: author, commentID, content, contentType, published, parentPostID
# Current foreignkey fields: isLiked
class Comment(models.Model):
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    commentID = models.CharField(primary_key=True, max_length=40)
    content = models.TextField()
    contentType = models.TextField()
    # date = models.DateField()
    published=models.DateField()
    parentPostID = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    # Modified models by added more fields
    # whether the comment is liked or not
    isLiked=models.BooleanField(default=False)

# Changes towards Like (02/28):
# - Added fields: summary, author
# - changed: parentPost, parentComment
# - Commented/ (later will delete): N/A
# Current Own Fields: author, commentID, content, contentType, published, parentPostID
# Current foreignkey fields: isLiked
class Like(models.Model):
    likeID = models.CharField(primary_key=True, max_length=40)

    summary=models.TextField()
    likeType = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # changed parentPost and parentComment, on_delete from models.CASACADE to models.SET_NULL because one can like a post or comment
    parentPost = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    """
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    """
    # object can be obtained without additional fields

# Changes towards Like (02/28):
# - Added fields: 
# - changed name: owner (to author)
# - Commented/ (later will delete): like, comment, content, contentType
# Current Own Fields: author, commentID, content, contentType, published, parentPostID
# Current foreignkey fields: isLiked
class Inbox(models.Model):
    # EDIT: 
    inboxID=models.CharField(primary_key=True, max_length=40, default="")

    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    # owner=models.ForeignKey(Author, on_delete=models.CASCADE)

    # likes, posts
    post=models.ManyToManyField(Post)
    """
    like=models.ManyToManyField(Like)
    comment=models.ManyToManyField(Comment)
    """
    # inbox content and its type
    """
    content = models.TextField()
    contentType = models.TextField()
    """