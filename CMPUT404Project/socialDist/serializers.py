from rest_framework import serializers
from .models import Author, Post, Comment, Like

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'username', 'url', 'github', 'profileImg', 'host')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'contentType', 'posterID', 'date', 'visibility', 'unlisted')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'contentType', 'parentPostID', 'date', 'author')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'target', 'sender', 'date')