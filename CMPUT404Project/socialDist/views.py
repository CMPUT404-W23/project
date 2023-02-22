from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import QueryDict
from rest_framework import status
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer
from .serializers import LikeSerializer, InboxSerializer
from .models import Author, Post, Comment, Like, Inbox, FollowRequest

# Create your views here.
# class AuthorViewSet(viewsets.ModelViewSet):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     permission_classes = [DjangoModelPermissions]

#     def create(self, request):
#         serializer = AuthorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def list(self, request):
#         queryset = Author.objects.all()
#         serializer = AuthorSerializer(queryset, context={"type":"author"}, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Author.objects.all()
#         author = get_object_or_404(queryset, pk=pk)
#         serializer = AuthorSerializer(author)
#         return Response(serializer.data)

#     def destroy(self,request, pk=None):
#         author = Author.objects.get(pk=pk)
#         author.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def update(self, request, pk=None):
#         author = Author.objects.get(pk=pk)
#         serializer = AuthorSerializer(author, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [DjangoModelPermissions]

#     def create(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def list(self, request):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Post.objects.all()
#         post = get_object_or_404(queryset, pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def destroy(self,request, pk=None):
#         post = Post.objects.get(pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def update(self, request, pk=None):
#         post = Post.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [DjangoModelPermissions]

#     def create(self, request):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def list(self, request):
#         queryset = Comment.objects.all()
#         serializer = CommentSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Comment.objects.all()
#         comment = get_object_or_404(queryset, pk=pk)
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)

#     def destroy(self,request, pk=None):
#         comment = Comment.objects.get(pk=pk)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def update(self, request, pk=None):
#         comment = Comment.objects.get(pk=pk)
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LikeViewSet(viewsets.ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = [DjangoModelPermissions]

#     def create(self, request):
#         serializer = LikeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def list(self, request):
#         queryset = Like.objects.all()
#         serializer = LikeSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Like.objects.all()
#         like = get_object_or_404(queryset, pk=pk)
#         serializer = LikeSerializer(like)
#         return Response(serializer.data)

#     def destroy(self,request, pk=None):
#         like = Like.objects.get(pk=pk)
#         like.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def update(self, request, pk=None):
#         like = Like.objects.get(pk=pk)
#         serializer = LikeSerializer(like, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_authors(request):
    # query string provided
    if (request.META["QUERY_STRING"] != ""):
        queryDict = QueryDict(request.META["QUERY_STRING"])
        pageNum = 0
        sizeNum = 0
        if "page" in queryDict:
            try:
                pageNum = int(queryDict["page"])
            except ValueError:
                return Response(status=status.HTTP_404_NOT_FOUND)
        if "size" in queryDict:
            try:
                sizeNum= int(queryDict["size"])
            except ValueError:
                return Response(status=status.HTTP_404_NOT_FOUND)
    # query string not provided
    else:
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={"type":"author"})
        authorListDict = {}
        authorListDict["type"] = "authors"
        authorListDict["items"] = serializer.data
        return Response(authorListDict)

@api_view(['GET'])
def get_author(request, id):
    try:
        author = Author.objects.get(pk=id)
        serialzer = AuthorSerializer(author)
        return Response(serialzer.data)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post(request, author_id, post_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        post = Post.objects.filter(posterID=author).get(pk=post_id)
        serialzer = PostSerializer(post, context={"type":"post"})
        return Response(serialzer.data)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_posts(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    posts = Post.objects.filter(posterID=author)
    serializer = PostSerializer(posts, many=True, context={"type":"post"})
    postListDict = {}
    postListDict["type"] = "posts"
    postListDict["items"] = serializer.data
    return Response(postListDict)

@api_view(['POST'])
def edit_post(request, author_id, post_id):
    return Response(status=status.HTTP_301)

@api_view(['GET'])
def get_comments(request, author_id, post_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        post = Post.objects.filter(posterID=author).get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    comments = Comment.objects.filter(parentPostID=post_id)
    serializer = CommentSerializer(comments, many=True, context={"type":"comment"})
    commentListDict = {}
    commentListDict["type"] = "comments"
    commentListDict["items"] = serializer.data
    return Response(commentListDict)

@api_view(['GET'])
def get_comment(request, author_id, post_id, comment_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        post = Post.objects.filter(posterID=author).get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    comment = Comment.objects.filter(parentPostID=post_id).get(pk=comment_id)
    serialzer = CommentSerializer(comment, context={"type":"comment"})
    return Response(serialzer.data)

@api_view(['GET'])
def get_likes_for_post(request, author_id, post_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        post = Post.objects.filter(posterID=author).get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    likes = Like.objects.filter(parentPost=post_id)
    serializer = LikeSerializer(likes, many=True, context={"type":"like"})
    likeListDict = {}
    likeListDict["type"] = "likes"
    likeListDict["items"] = serializer.data
    return Response(likeListDict)

@api_view(['GET'])
def get_likes_for_comment(request, author_id, post_id, comment_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        post = Post.objects.filter(posterID=author).get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try: 
        comment = Comment.objects.filter(parentPostID=post_id).get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    likes = Like.objects.filter(parentComment=comment)
    serializer = LikeSerializer(likes, many=True, context={"type":"like"})
    likeListDict = {}
    likeListDict["type"] = "likes"
    likeListDict["items"] = serializer.data
    return Response(likeListDict)

@api_view(['GET'])
def get_inbox(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    inbox = Inbox.objects.get(owner=author)
    serializer = LikeSerializer(inbox, context={"type":"inbox"})
    return Response(serializer.data)

@api_view(['GET'])
def get_likes_for_author(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    likes = Like.objects.filter(author=author_id)
    serializer = LikeSerializer(likes, many=True, context={"type":"likes"})
    likeListDict = {}
    likeListDict["type"] = "liked"
    likeListDict["items"] = serializer.data
    return Response(likeListDict)
        

@api_view(['GET'])
def get_followers_for_authors(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user_followers = author.followers.all()
    followersList = []
    for user_follower in user_followers:
        followersList.append(user_follower.following)
    serializer = AuthorSerializer(followersList, many=True, context={"type":"author"})
    followerListDict = {}
    followerListDict["type"] = "followers"
    followerListDict["items"] = serializer.data
    return Response(followerListDict)

@api_view(['GET'])
def get_inbox(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    requests = FollowRequest.objects.filter(target=author_id)
    # TO DO: convert into list using serializer
    authorPosts = Post.objects.filter(author=author_id)
    authorComments = Post.objects.filter(author=author_id)
    likeList = []
    commentList = []
    for post in authorPosts:
        likeList += post.likes
        commentList += post.comments
    for comment in authorComments:
        likeList += comment.likes
    likeSerializer = LikeSerializer(likeList, many=True, context={"type":"like"})
    commentSerializer = CommentSerializer(commentList, many=True, context={"type":"comment"})
