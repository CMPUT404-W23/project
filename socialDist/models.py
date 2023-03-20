# MIT License

# Copyright (c) 2023 Warren Lim

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from django.db import models
from django.contrib.auth.models import User
import hashlib

# Added array field to handle categories in post
# https://stackoverflow.com/questions/4294039/how-can-i-store-an-array-of-strings-in-a-django-model
from django.contrib.postgres.fields import ArrayField

# Sources:
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
# https://www.crunchydata.com/blog/composite-primary-keys-postgresql-and-django
# https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-coupl



# Changes towards Author (02/28)
# - Added authorId, displayName
# - Commented/ (later will delete): isServerAdmin, isAuthenticated
# Current Own Fields: user, authorId, displayName, github, profileImg
# Current foreignkey fields: inServer, isFriendWith (nore sure to keep or not)
class Author(models.Model):
    # user: one to one field 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # authorID: ID of the author
    id=models.CharField(primary_key=True, max_length=200)
    host=models.CharField(max_length=200)
    # Added displayName field, default as empty string
    displayName=models.CharField(default="", max_length=40)
    # github and profileImage fields
    github = models.URLField(null=True, blank=True)
    profileImage = models.URLField(null=True, blank=True)

    # # Fields referenced other models externally
    # # check whether the author in a server or not
    # inServer=models.ForeignKey('Server', blank='True', on_delete=models.SET_NULL, null=True)

    # # Not sure to keep or not
    # # Check friends status; self-reference: Can't set it to false, left it true for now
    # isFriendWith=models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

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

# List of servers authenciated to commuicate with us!
# Source: https://stackoverflow.com/questions/72371106/how-to-auto-generate-a-field-value-with-the-input-field-value-in-django-model
# https://docs.python.org/3/library/hashlib.html
class Server(models.Model):
    # server Address, provided to us by connecting node
    serverAddress=models.URLField(primary_key=True)
    # server key or token used to access API, based on host name
    #TODO: come up with API token generation techinque, right now it is SHA1 hash
    serverKey=models.TextField(blank=True)
    # Is this server the local one?
    isLocalServer=models.BooleanField()

    def save(self):
        hash = hashlib.sha1()
        hash.update(self.serverAddress.encode('utf-8'))
        self.serverKey = hash.hexdigest()


# Model to store relationships between followers
# Source:
# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
class UserFollowing(models.Model):
    user_id = models.ForeignKey(Author, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(Author, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user_id', 'following_user_id')

# Model demonstarting a follow request sent to the inbox of an author on this server:
# Source:
# https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
class FollowRequest(models.Model):
    sender = models.ForeignKey(User, related_name="send_requests", on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name="recievced_requests", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True)

# Model demonstrating a Post stored on this server
# Posts stored on this server are posts made by authors hosted on this server, and any post
# sent to the inbox of an author on this server
class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    title = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)
    description = models.TextField()
    contentType = models.TextField(choices=[
        ("text/plain", "plaintext"),
        ("text/markdown", "markdown"),
        ("application/base64", "binary"),
        ("image/png;base64", "PNG image"),
        ("image/jpeg;base64", "JPEG image")
    ])
    content = models.TextField()
    # author to access the author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    # added categories: use arrayfield from postgres
    # categories=ArrayField(models.CharField(max_length=50), default=list)
    # # OR
    categories=models.CharField(max_length=100)
    published = models.DateTimeField(auto_created=True)
    visibility=models.CharField(max_length=30, choices=[
        ("VISIBLE", "Public"),
        ("FRIENDS","Private")
    ])
    unlisted = models.BooleanField()

    # isLiked=models.BooleanField(default=False)

    # # Foreignkey fields:
    # # the server that the post belongs too
    # inServer=models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    # # whether the post is liked or not
    # isLiked=models.BooleanField(default=False)

# Changes towards Comment (02/28):
# - Added fields: author
# - changed name:  date (to published)
# - Commented/ (later will delete): N/A
# Current Own Fields: author, commentID, content, contentType, published, parentPostID
# Current foreignkey fields: isLiked
class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
  
    content = models.TextField()
    contentType = models.TextField(choices=[
        ("text/plain", "plaintext"),
        ("text/markdown", "markdown")
    ])

    published = models.DateTimeField(auto_created=True)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    
    # # Modified models by added more fields
    # # whether the comment is liked or not
    # isLiked=models.BooleanField(default=False)

# Changes towards Like (02/28):
# - Added fields: summary, author
# - changed: N/A
# - Commented/ (later will delete): N/A
# Current Own Fields: author, commentID, content, contentType, published, parentPostID
# Current foreignkey fields: isLiked
class Like(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    summary=models.TextField()
    likeType = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="liked")
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes",null=True, blank=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    published = models.DateTimeField(auto_created=True)


# Changes towards Inbox (02/28):
# - Added fields: N/A
# - changed name: owner (to author)
# - Commented/ (later will delete): like, comment, content, contentType
# Current Own Fields: inboxID, authorm post
# Current foreignkey fields: isLiked
class Inbox(models.Model):
    # EDIT: 
    inboxID=models.CharField(primary_key=True, max_length=40, default="")

    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    # owner=models.ForeignKey(Author, on_delete=models.CASCADE)

    # Posts
    posts=models.ManyToManyField(Post)
    
