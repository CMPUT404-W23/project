from rest_framework import serializers
from .models import Author, Post, Comment, Like, Server, Inbox

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # fields = ('id', 'user', 'github', 'profileImg')

        # Update added fields (if it doesn't work just uncomment the line above)
        fields = ('id', 'user', 'github', 'profileImg','isServerAdmin', 'isAuthenticated', 'isFriendWith', 'inServer')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ('postID', 'title', 'content', 'contentType', 'posterID', 'date', 'visibility', 'unlisted')

        # Update added fields (if it doesn't work just uncomment the line above)
        fields = ('postID', 'title', 'content', 'contentType', 'posterID', 'date', 'visibility', 'unlisted', 'server', 'isLiked')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = ('commentID', 'content', 'contentType', 'parentPostID', 'date', 'author')

        # Update added fields (if it doesn't work just uncomment the line above)
        fields = ('commentID', 'content', 'contentType', 'parentPostID', 'date', 'author','isLiked')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('likeID', 'likeType', 'parentPost', 'parentComment')

# Added new serlaizers for Server and Inbox
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Server
        fields=('serverID', 'owner', 'serverName')

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model=Inbox
        fields=('owner','items')