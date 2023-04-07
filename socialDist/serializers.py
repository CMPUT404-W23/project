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

from rest_framework import serializers
from .models import Author, Post, Comment, Like, Server, Inbox, Connection, FollowRequest

# File contains serializers for the different models of our appilcation

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id',
                  'host',
                  'displayName', 
                  'github', 
                  'profileImage')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 
                  'title', 
                  'source',
                  'origin',
                  'description', 
                  'content',
                  'contentType', 
                  'author', 
                  'published', 
                  'visibility', 
                  'categories',
                  'unlisted')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 
                  'comment', 
                  'contentType', 
                  'parentPost', 
                  'published', 
                  'author')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 
                  'author',
                  'published')

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = (
            'apiAddress',
            'apiCreds',
            'hostName'
        )

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Server
        fields=('serverID', 'owner', 'serverName')

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inbox
        fields=('inboxID', 'author', 'posts', 'requests', 'comments', 'likes')

class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=FollowRequest
        fields=('sender', 'target', 'date')