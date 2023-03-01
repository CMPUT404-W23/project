from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import QueryDict
from rest_framework import status
from django.utils.crypto import get_random_string
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer

from .models import Author, Post, Comment, Like, Server, Inbox

# https://testdriven.io/blog/drf-views-part-1/
# https://docs.djangoproject.com/en/4.1/topics/db/queries/#:~:text=Creating%20objects&text=To%20create%20an%20object%2C%20instantiate,save%20it%20to%20the%20database.&text=This%20performs%20an%20INSERT%20SQL,method%20has%20no%20return%20value.
# https://docs.djangoproject.com/en/4.1/ref/request-response/
# https://www.geeksforgeeks.org/adding-permission-in-api-django-rest-framework/
# https://stackoverflow.com/questions/25943850/django-package-to-generate-random-alphanumeric-string

class APIAuthor(APIView):
    def get(self, request, id):
        try:
            author = Author.objects.get(pk=id)
            serialzer = AuthorSerializer(author)
            return Response(status=200, data=serialzer.data)
        except Author.DoesNotExist:
            return Response(status=404)

    def post(self, request, id):
        try:
            author = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(status=404)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=serializer.errors)
    
class APIListAuthors(APIView):
    def get(self, request):
         # query string provided
        if (request.META["QUERY_STRING"] != ""):
            queryDict = QueryDict(request.META["QUERY_STRING"])
            pageNum = 0
            sizeNum = 0
            if "page" in queryDict:
                try:
                    pageNum = int(queryDict["page"])
                except ValueError:
                    return Response(status=404)
            if "size" in queryDict:
                try:
                    sizeNum= int(queryDict["size"])
                except ValueError:
                    return Response(status=404)
        # query string not provided
        else:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True, context={"type":"author"})
            authorListDict = {}
            authorListDict["type"] = "authors"
            authorListDict["items"] = serializer.data
            return Response(status=200, data=authorListDict)
 
class APIPost(APIView):
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(posterID=author).get(pk=post_id)
            serialzer = PostSerializer(post, context={"type":"post"})
            return Response(status=200, data=serialzer.data)
        except Post.DoesNotExist:
            return Response(status=404)

    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=serializer.errors)

    def put(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.get(pk=post_id)
            return Response(status=404)
        except Post.DoesNotExist:
            serializer = PostSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=serializer.data)
            return Response(status=400, data=serializer.errors)

    def delete(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        post.delete()
        return Response(status=200)

class APIListPosts(APIView):
    def get(self, request, author_id):
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

    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        while True:
            post_id = get_random_string(40)
            try:
                post = Post.objects.get(postID=post_id)
                continue
            except:
                request.data["postID"] = post_id
                serializer = PostSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, data=serializer.data)
                return Response(status=400, data=serializer.errors)
    

class APIComment(APIView):
    def get(self, request, author_id, post_id, comment_id):
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

class APIListComments(APIView):
    def get(self, request, author_id, post_id):
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

    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.filter(posterID=author).get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        while True:
            comment_id = get_random_string(40)
            try:
                comment = Comment.objects.get(commentID=post_id)
                continue
            except:
                request.data["commentID"] = comment_id
                serializer = CommentSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, data=serializer.data)
                return Response(status=400, data=serializer.errors)

class APIListLikesPost(APIView):
    def get(self, request, author_id, post_id):
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

class APIListLikesComments(APIView):
    def get(self, request, author_id, post_id, comment_id):
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

class APILiked(APIView):
    def get(request, author_id):
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
        
class APIFollowers(APIView):
    def get(self, request, author_id):
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

class APIFollower(APIView):
    def get(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
            return Response(status=404)
        if followingAuthor in targetAuthor.followers:
            return Response(status=200)
        else:
            return Response(status=400)

    def put(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=author_id)
            # check host if they are hosted on our server
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
            # create copy of author on our server
            return Response(status=404)
        if followingAuthor in targetAuthor.followers.all():
            return Response(status=405)
        # link two authors together with relationship
        targetAuthor.followers.add(followingAuthor)
        targetAuthor.save()
        return Response(status=200)

    def delete(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=author_id)
            # check host if they are hosted on our server
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
            # create copy of author on our server
            return Response(status=404)
        if followingAuthor not in targetAuthor.followers.all():
            return Response(status=404)
        targetAuthor.followers.remove(followingAuthor)
        targetAuthor.save()
        return Response(status=200)

class APIInbox(APIView):
    def get(request, author_id):
        # get the owner first in order to get the inbox
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            inbox = Inbox.objects.filter(owner=author)
        except Inbox.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ServerSerializer(inbox).data)

# get one server
@api_view(['GET'])
def get_server(request, author_id):
    # get the owner first in order to get the server
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        server = Server.objects.filter(owner=author)
    except Server.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ServerSerializer(server).data)

# Get all of the servers that one owns:
@api_view(['GET'])
def get_servers(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    servers=Server.objects.filter(owner=author)
    serializer=ServerSerializer(servers, many=True, context={"type":"post"})
    serverListDict = {}
    serverListDict["type"]="servers"
    postListDict["items"] = serializer.data
    return Response(serverListDict)

@api_view(['GET'])
def get_inbox(request, author_id):
    # get the owner first in order to get the inbox
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        inbox = Inbox.objects.filter(owner=author).get(pk=inboxID)
    except Inbox.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ServerSerializer(inbox).data)

# similar to get_posts, but find them through the server but not the author
# @api_view(['GET'])
# def get_inbox_posts(request, server_id):
