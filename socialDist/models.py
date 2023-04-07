# MIT License

# Copyright (c) 2023 Warren Lim, Junhyeon Cho, Alex Mak, Jason Kim, Filippo Ciandy

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

# Models used in our appilcation

# Sources:
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
# https://www.crunchydata.com/blog/composite-primary-keys-postgresql-and-django
# https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-coupl
# https://stackoverflow.com/questions/4294039/how-can-i-store-an-array-of-strings-in-a-django-model


# Model representing an author
class Author(models.Model):
    # user: one to one field 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # authorID: ID of the author
    id=models.CharField(primary_key=True, max_length=1000)
    host=models.CharField(max_length=500)
    # Added displayName field, default as empty string
    displayName=models.CharField(default="", max_length=40)
    # github and profileImage fields
    github = models.URLField(null=True, blank=True)
    profileImage = models.URLField(null=True, blank=True)

# Model representing servers authenciated to commuicate with us!
class Server(models.Model):
    # server Address, provided to us by connecting node
    serverAddress=models.URLField(primary_key=True)
    # server key or token used to access API, based on host name (SHA1 hash)
    serverKey=models.TextField(blank=True)
    # Is this server the local one?
    isLocalServer=models.BooleanField()

# Model to store the auth info of all servers we are connecting with
class Connection(models.Model):
    # API address, provided to us by node we want to connect to, 
    # simply append API endpoint path to the end of this
    apiAddress=models.URLField(primary_key=True)
    # Creditentals used to connect to API of node, add this to Authorization header
    # when sending HTTP requests to fetch external data
    apiCreds=models.TextField(blank=True)
    hostName=models.URLField()

# Model to store relationships between followers
# Source:
# StackOverflow
# Author: Enthusiast Martin
# Author URL: https://stackoverflow.com/users/9987957/enthusiast-martin
# Title: How to make follower following system with django model
# URL: https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# Date: November 11, 2019
#
# StackOverflow
# Author: Jens
# Author URL: https://stackoverflow.com/users/190823/jens 
# Title: How to define two fields "unique" as couple
# URL: https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
# Date: Feb 4, 2010
class UserFollowing(models.Model):
    user_id = models.ForeignKey(Author, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(Author, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user_id', 'following_user_id')

# Model demonstarting a follow request sent to the inbox of an author on this server:
# Source:
# Author: Abhik
# Date: Oct 25, 2020
# Title: Step by Step guide to add friends with Django
# URL: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
class FollowRequest(models.Model):
    sender = models.ForeignKey(Author, related_name="send_requests", on_delete=models.CASCADE)
    target = models.ForeignKey(Author, related_name="recievced_requests", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True)

# Model demonstrating a Post stored on this server
# Posts stored on this server are posts made by authors hosted on this server, and any post
# sent to the inbox of an author on this server
class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=1000)
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.TextField()
    contentType = models.TextField(choices=[
        ("text/plain", "plaintext"),
        ("text/markdown", "markdown"),
        ("application/base64", "binary"),
        ("image/png;base64", "PNG image"),
        ("image/jpeg;base64", "JPEG image"),
        ("image/jpg;base64", "JPG image")
    ])
    content = models.TextField()
    # author to access the author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    categories=models.CharField(max_length=250)
    published = models.DateTimeField(auto_created=True)
    visibility=models.CharField(max_length=50, choices=[
        ("VISIBLE", "Public"),
        ("FRIENDS","Private")
    ])
    unlisted = models.BooleanField()

# Model representing a comment
class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
  
    comment = models.TextField()
    contentType = models.TextField(choices=[
        ("text/plain", "plaintext"),
        ("text/markdown", "markdown")
    ])

    published = models.DateTimeField(auto_created=True)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    

# Model representing a like
class Like(models.Model):
    id = models.CharField(primary_key=True, max_length=500)
    likeType = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="liked")
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes",null=True, blank=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    published = models.DateTimeField(auto_created=True)


# Model representing an inbox
class Inbox(models.Model):
    inboxID=models.CharField(primary_key=True, max_length=500, default="")
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    posts=models.ManyToManyField(Post, blank=True)
    requests = models.ManyToManyField(FollowRequest, blank=True)
    comments= models.ManyToManyField(Comment, blank=True)
    likes=models.ManyToManyField(Like, blank=True)
    
