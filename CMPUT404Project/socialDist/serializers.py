from rest_framework import serializers
from .models import Author, Post, Comment, Like

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'url', 'host', 'username', 'github', 'profileImg')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'contentType', 'posterID', 'date', 'visibility', 'unlisted')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('commentID', 'content', 'contentType', 'parentPostID', 'date', 'author')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('likeID', 'likeType', 'parentPost', 'parentComment')