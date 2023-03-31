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

# This file contains the views for our API

# Sources:
# https://docs.djangoproject.com/en/4.1/topics/db/queries/#:~:text=Creating%20objects&text=To%20create%20an%20object%2C%20instantiate,save%20it%20to%20the%20database.&text=This%20performs%20an%20INSERT%20SQL,method%20has%20no%20return%20value.
# https://docs.djangoproject.com/en/4.1/ref/request-response/
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/
# https://testdriven.io/blog/drf-views-part-1/
# https://www.geeksforgeeks.org/adding-permission-in-api-django-rest-framework/
# https://stackoverflow.com/questions/25943850/django-package-to-generate-random-alphanumeric-strin
# https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/

import datetime
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from . import auth
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from django.http import QueryDict
from rest_framework import status
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer, FollowRequestSerializer
import urllib.parse
# from itertools import chain
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid

# TODO: we need to support the following operations to connect with other nodes!
# What is said below appiles to local node elements too!
# We also need the UI for the corresponding pages
#   - Home stream or "global stream"
#   - User profile page with user inbox
#   - Create post page
#   - Edit post page
# - When making a post, we need to send a POST request containing the Post body
#   to foreign inboxes which are targeted 
#   - Public posts and private posts with no target, inbox of all followers of poster
#   - Private posts, inbox of specfic target follower
#   - Note this should also be forwarded to the inbox of the author!
# - When we edit a public post, we should re-send the post to the inbox of the foreign node
# - When making a follow request, we need to send a POST request containing the follow request
#   body to the foreign author inbox in question
#   - The follow request interface could be a field allowing us to select users in foriegn server
#   which we want to follow (suggestion)
# - On home or global stream, we need to get all of public Post of to all our
# connected nodes using GET requests 
#   - For fetching posts with embedded images, we need to fetch the corresponding image post using GET
# - When making a comment on a foreign post or liking a foreign post (public or private), we need to send
# a POST request to the foriegn node (to the /comments endpoint and the /inbox for comments and /inbox for likes)
# - When fetching comments or likes of a foreign post/likes, we need to send a GET request to that node
#   - How to display fetched likes or comments?
# - When the inbox recieves a follow request, it should:
#       - Check if the target author is hosted on the server or not
#       - Check if the sending author is stored on the server's DB, create an author object if it isn't
#       - Create a follow request object in the database
# - When the inbox recieves a like object, it should:
#       - Check if liking author exists (can be hosted on our server or foreign)
#           - Create an author object if it isn't (foreign only)
#       - Create a like object and associated with the parent object
# - When the inbox recieves a comment object, it should: 
#       - Check if comment author exists (can be hosted on our server or foreign)
#           - Create an author object if it isn't (foreign only)
# - When the post recieves a post object, it should:
#        - Check if post author exists (can be hosted on our server or foreign)
#           - Create an author object if it isn't (foreign only)
# - In order to support cross-origin AJAX requests, we need to allow Cross-Origin on any returned webpages!
#   - Note: need to see if we use AJAX or node to node commuication

from .models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from . import api_helper, sample_dicts
import base64 

HOST = "https://socialdistcmput404.herokuapp.com/"

# Swagger: DONE!!!

# API View for single author API queries (endpoint /api/authors/<author_id>/)
class APIAuthor(APIView):
    # Getting the information of a single author with that id
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve an author's profile", operation_description="Retrieve an author's profile based on:\n\n* The author's id", tags=["Author's Profile"], responses=sample_dicts.sampleGETAuthorDict)
    def get(self, request, id):
        try:
            # find author object
            author = Author.objects.get(pk=HOST+"authors/"+id)
            # serialize author object
            serialzer = AuthorSerializer(author)
            return Response(status=200, 
                            data=api_helper.construct_author_object(serialzer.data))
        except Author.DoesNotExist:
            # 404 if author object does not exist
            return Response(status=404)

    # Edit the author object  
    # When posting, send an author object in body in JSON with modified fields
    @swagger_auto_schema(operation_summary="Edit an author's profile", 
    operation_description="Edit an author's profile based on:\n\n* The author's id", 
    tags=["Author's Profile"], 
    responses=sample_dicts.samplePOSTAuthorDict,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            "id": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
            "host": openapi.Schema(type=openapi.TYPE_STRING, example=HOST),
            "displayName": openapi.Schema(type=openapi.TYPE_STRING, example="TestAuthor"), 
            "github": openapi.Schema(type=openapi.TYPE_STRING, example="www.githubtest.com"), 
            "profileImage": openapi.Schema(type=openapi.TYPE_STRING, example="testImage1.jpg"), 
            "type": openapi.Schema(type=openapi.TYPE_STRING, example="author"), 
            "url": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
        },
        description="Sample User object",
    ),)
    def post(self, request, id):
        # Check if author exists, 404 if not
        try:
            author = Author.objects.get(pk=HOST+"authors/"+id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if request is from an authorized source (only user and admin can call this!), 401 if not
        if not request.user.is_authenticated or (not request.user.is_staff and id != api_helper.extract_UUID(request.user.author.id)):
            return Response(status=401)
        try:
            authorDict = dict(request.data)
            authorDict["id"] = HOST+"authors/"+id
            authorDict["host"] = HOST
            serializer = AuthorSerializer(author, data=authorDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                author.user.username = serializer.data["displayName"]
                author.user.save()
                return Response(status=201, 
                                data=api_helper.construct_author_object(serializer.data))
            # Request data does not have vaild fields
            return Response(status=400, data=serializer.errors)
        # Request data is not in right JSON format
        except:
            return Response(status=400, data=serializer.errors)

# API View for list of authors API queries (endpoint /api/authors/)
class APIListAuthors(APIView):
    # Getting list of authors
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve every author's profile within the server", operation_description="Retrieve every author's profile within the server", tags=["Authors List"], responses=sample_dicts.sampleListAuthorDict)
    def get(self, request):
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
            authors = Author.objects.filter(host=HOST)
            serializer = AuthorSerializer(authors, many=True)
            return Response(status=200, data=api_helper.construct_paginated_list_of_authors(serializer.data,
                                                                                            pageNum,
                                                                                            sizeNum))
        # query string not provided, return full list of authors
        else:
            authors = Author.objects.filter(host=HOST)
            serializer = AuthorSerializer(authors, many=True)
            return Response(status=200, data=api_helper.construct_list_of_authors(serializer.data))
    
    # Update an author's profile

    @swagger_auto_schema(operation_summary="Create a new author's profile", 
    operation_description="Create an author's profile without any fields", 
    tags=["Author's Profile"], 
    responses=sample_dicts.sampleGETAuthorDict,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            "username": openapi.Schema(type=openapi.TYPE_STRING, example="sampleUsername"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, example="sampleUser@gmail.com"),         
            "password1": openapi.Schema(type=openapi.TYPE_STRING, example="samplePassword"),
        },
        description="Sample User object",
    ),)
    def put(self, request):
        username = request.data["username"]
        email = request.data.get("email", "") # if email is not provided, set it to empty string
        password = request.data["password1"]
        try:
            user = User.objects.create_user(username, email, password)
            # Generate a UUID
            UUID=uuid.uuid4()
            author = Author.objects.create(
                user=user,
                # id=HOST+"authors/" + str(user.pk),
                id=HOST+"authors/"+str(UUID),
                host=HOST,
                displayName=username,
                github="",
                profileImage="",
            )
            # OLD start
            # inbox = Inbox.objects.create(
            #     inboxID=HOST+"authors/"+str(user.pk)+"/inbox",
            #     author=author
            # )
            # OLD end

            # NEW start
            inbox = Inbox.objects.create(
                inboxID=HOST+"authors/"+str(UUID)+"/inbox",
                author=author
            )
            # NEW end
            return Response(status=201)
        except (IntegrityError, ValueError) as e:
            if IntegrityError:
                return Response(status=409, data="An account with that username already exists.")
            else:
                return Response(status=400, data="Account creation failed.")

# API View for single post queries (endpoint /api/authors/<author_id>/posts/<post_id>)
class APIPost(APIView):
    # Get a single post
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a public post", operation_description="Retrieve a public post's information based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"], responses=sample_dicts.sampleGETPostDict)
    def get(self, request, author_id, post_id):
        # Check if specified author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if specfied post exists
        try:
            post = Post.objects.filter(author=author).filter(visibility="VISIBLE").get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            serialzer = PostSerializer(post)
            return Response(status=200, data=api_helper.construct_post_object(serialzer.data, author))
        except Post.DoesNotExist:
            return Response(status=404)
        
    # Edit a single post
    # When POSTing, send a post object in JSON with the modified fields
    # Cannot edit a private post!
    @swagger_auto_schema(operation_summary="Edit a public post", operation_description="Edit a public post's information based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"],responses=sample_dicts.samplePOSTPostDict, request_body=PostSerializer)
    def post(self, request, author_id, post_id):
        # Check if specified author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if specfied post exists
        try:
            post = Post.objects.filter(visibility="VISIBLE").get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # Check if request is from an authorized source (only user and admin can call this!), 401 if not
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        postDict = dict(request.data)
        postDict["author"] = HOST+"authors/"+author_id
        serializer = PostSerializer(post, data=postDict, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=api_helper.construct_post_object(serializer.data, author))
        return Response(status=400, data=serializer.errors)
    
    # Create a single post
    # When PUTTing, send a post object in JSON with the field
    # Note that host and id will be set to HOST and HOST/authors/author_id/posts/post_id
    # When PUTTing to a public post that already exists, replace post with JSON post object in body
    # Cannot PUT to an already existing private post!
    @swagger_auto_schema(operation_summary="Create a public post", operation_description="Create a public post based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"],responses=sample_dicts.samplePOSTPostDict, request_body=PostSerializer)
    def put(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if resource already exists, if it does, acts like POST!
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            # Check if request is from an authorized source (only user and admin can call this!), 401 if not
            if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
                return Response(status=401)
            if post.visibility == "PRIVATE":
                return Response(status=404)
            postDict = dict(request.data)
            postDict["author"] = HOST+"authors/"+author_id
            serializer = PostSerializer(post, data=postDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_post_object(serializer.data, author))
            return Response(status=400, data=serializer.errors)
        except Post.DoesNotExist:
            # Check if request is from an authorized source (only user and admin can call this!), 401 if not
            if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
                return Response(status=401)
            postDict = dict(request.data)
            postDict["author"] = HOST+"authors/"+author_id
            postDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id
            serializer = PostSerializer(data=postDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                #
                # return Response(status=201, data=api_helper.construct_post_object(serializer.data))
                #  add argument for author since that's what needed from api_helper
                return Response(status=201, data=api_helper.construct_post_object(serializer.data, author))
                # return Response(status=201, data=api_helper.construct_post_object(serializer.data))
            return Response(status=400, data=serializer.errors)
        
    # Delete the single post
    # Cannot delete private posts!
    @swagger_auto_schema(operation_summary="Delete a public post", operation_description="Delete a public post's information based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"], responses=sample_dicts.sampleDELETEDict)
    def delete(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        try:
            post = Post.objects.filter(visibility="VISIBLE").get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        post.delete()
        return Response(status=200)
    
# API View for a list of post queries (endpoint /api/authors/<author_id>/posts/)
class APIListPosts(APIView):
    # Get a list of posts, with paginating support
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a list of posts (public posts only) for a specific author", operation_description="Retrieve a list of posts (public posts only) for a specific author based on:\n\n* The author's own id", tags=["Post List"], responses=sample_dicts.sampleListPostsDict)
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        posts = Post.objects.filter(author=author).filter(visibility="VISIBLE").order_by('published')
        serializer = PostSerializer(posts, many=True)
        if (request.META["QUERY_STRING"] == ""):
            return Response(status=200, data=api_helper.construct_list_of_posts(serializer.data, author))
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
        return Response(status=200, data=api_helper.construct_list_of_paginated_posts(serializer.data,
                                                                                    pageNum,
                                                                                    sizeNum,
                                                                                    author))
    # Add a post with a randomized post id
    # Include a post object in JSON with modified fields
    # Note that host and id field will be ignored!

    # Template
    # {
    #     "id": "",
    #     "title": "UUID testing",
    #     "source": "UUID",
    #     "origin": "string",
    #     "description": "string",
    #     "content": "string",
    #     "contentType": "text/plain",
    #     "author": "https://socialdistcmput404.herokuapp.com/authors/2",
    #     "published": "2023-03-30T20:31:50.362Z",
    #     "visibility": "VISIBLE",
    #     "categories": "string",
    #     "unlisted": true
    # }
    @swagger_auto_schema(operation_summary="Create a post with a randomized post id", operation_description="Create a post with a randomized post id based on:\n\n* The author's own id", tags=["Post List"], request_body=PostSerializer, responses=sample_dicts.samplePOSTPostDict)
    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            print("Author does not exist")
            return Response(status=404)
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        while True:
            # OLD start
            # post_id = get_random_string(10)
            # old end

            # NEW start
            # generate new UUID
            UUID=uuid.uuid4()
            post_id=str(UUID)
            # NEW end

            try:
                post = Post.objects.get(postID=HOST+"authors/"+author_id+"/posts/"+post_id)
                continue
            except:
                newPostDict = dict(request.data)
                newPostDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id
                newPostDict["author"]=HOST+"authors/"+author_id
                newPostDict["published"] = datetime.datetime.now().isoformat()
                serializer = PostSerializer(data=newPostDict, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, 
                                        data=api_helper.construct_post_object(serializer.data, author))
                return Response(status=400, data=serializer.errors)

# Endpoint used to fetch image posts as images (endpoint /api/authors/<author_id>/posts/<post_id>/image)
class APIImage(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve an image post", operation_description="Retrieve an image post based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Images"], responses=sample_dicts.sampleImagePostGETDict)
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if resource already exists, if it does, acts like a GET request
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            if post.visibility == "PRIVATE" and not api_helper.is_follower(request.user, author):
                return Response(status=401)
            if post.contentType != "image/png;base64" and post.contentType != "image/jpeg;base64" and post.contentType != "image/jpg;base64":
                return Response(status=404)
            content_bytes_base64 = post.content.encode('ascii')
            return HttpResponse(status=200, 
                            content=base64.b64decode(content_bytes_base64), 
                            content_type=post.contentType)
        except Post.DoesNotExist:
            return Response(status=404)
    
#API View for single comment queries (endpoint /api/authors/<author_id>/posts/<post_id>/comments/<comment_id>)
class APIComment(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a comment within a post", operation_description="Retrieve a comment within a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post\n* The id of the comment itself", tags=["Comments"], responses=sample_dicts.sampleGETCommentDict)
    def get(self, request, author_id, post_id, comment_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # for a private post, only the author can access the comments!
        if post.visibility == "PRIVATE" and (not request.user.is_authenticated or request.user.author != author):
            return Response(status=401)
        try:
            comment = Comment.objects.filter(parentPost=HOST+
                                                        "authors/"+
                                                        author_id+
                                                        "/posts/"+
                                                        post_id).get(pk=HOST+
                                                        "authors/"+
                                                        author_id+
                                                        "/posts/"+
                                                        post_id+
                                                        "/comments/"+
                                                        comment_id)
            serialzer = CommentSerializer(comment)
            return Response(api_helper.construct_comment_object(serialzer.data, author))
        except Comment.DoesNotExist:
            return Response(status=404)
    
#API View for list of comments queries (endpoint /api/authors/<author_id>/posts/<post_id>/comments/)
class APIListComments(APIView):
    # Get list of comments
    permission_classes = [auth.CommentsPermissions]
    @swagger_auto_schema(operation_summary="Retrieve all of the comments within a post", operation_description="Retrieve all of the comments within a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post", tags=["Comments"], responses=sample_dicts.sampleListCommentsDict)
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # for a private post, only the author can access the comments!
        if post.visibility == "PRIVATE" and (not request.user.is_authenticated or request.user.author != author):
            return Response(status=401)
        comments = Comment.objects.filter(parentPost=HOST+"authors/"+author_id+"/posts/"+post_id)
        serializer = CommentSerializer(comments, many=True)
        if (request.META["QUERY_STRING"] == ""):
            return Response(status=200, data=api_helper.construct_list_of_comments(serializer.data,
                                                                               post))
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
        return Response(status=200, data=api_helper.construct_paginated_list_of_comments(serializer.data,
                                                                                         pageNum,
                                                                                         sizeNum,
                                                                                         author,
                                                                                         post))
    
    # Post a comment under that post
    # Include comment object in body in JSON form
    # id and parentPost field will be ignored!
    @swagger_auto_schema(operation_summary="Create a comment in a post", 
    operation_description="Create a comment in a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post", 
    tags=["Comments"],
    responses=sample_dicts.samplePOSTCommentDict, 
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            "id": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3"),
            "content": openapi.Schema(type=openapi.TYPE_STRING, example="Test comment content"),         
            "contentType": openapi.Schema(type=openapi.TYPE_STRING, example="text/plain"),
            "published": openapi.Schema(type=openapi.TYPE_STRING, example="2023-03-22T21:37:36Z"),
            "author": openapi.Schema(type=openapi.TYPE_OBJECT, 
            properties=
            {
                "id": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
                "host": openapi.Schema(type=openapi.TYPE_STRING, example=HOST),
                "displayName": openapi.Schema(type=openapi.TYPE_STRING, example="TestAuthor"), 
                "github": openapi.Schema(type=openapi.TYPE_STRING, example="www.githubtest.com"), 
                "profileImage": openapi.Schema(type=openapi.TYPE_STRING, example="testImage1.jpg"), 
                "type": openapi.Schema(type=openapi.TYPE_STRING, example="author"), 
                "url": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
            }
            ),
            "type":openapi.Schema(type=openapi.TYPE_STRING, example="comment"),     
            },
        description="Sample Comment object",
    ))
    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        while True:
            # OLD start
            # comment_id = get_random_string(20)
            # OLD end

            # NEW start
            # Generate a UUID
            UUID=uuid.uuid4()
            comment_id=str(UUID)
            # NEW end
            
            # try searching that comment
            try:
                # return Response(status=200)
                comment = Comment.objects.get(id=HOST+
                                              "authors/"+
                                              author_id+
                                              "/posts/"+
                                              post_id+
                                              "/comments/"+
                                              comment_id)
                continue
            except Comment.DoesNotExist:
                newCommentDict = dict(request.data)
                newCommentDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id+"/comments/"+comment_id
                newCommentDict["parentPost"] = HOST+"authors/"+author_id+"/posts/"+post_id

                # check if author is saved in our DB (remote or local)
                try:
                    commentAuthor = Author.objects.get(pk=newCommentDict["author"]["id"])
                except Author.DoesNotExist:
                    # check if author is a remote author not yet saved
                    if newCommentDict["author"]["host"] == HOST:
                        return Response(status=404)
                    # save new remote author into DB
                    commentAuthorSerializer = AuthorSerializer(data=newCommentDict["author"])
                    if not commentAuthorSerializer.is_valid():
                        return Response(status=400, data=commentAuthorSerializer.errors)
                    commentAuthorSerializer.save()
                newCommentDict["author"] = newCommentDict["author"]["id"]
                newCommentDict["published"] = datetime.datetime.now().isoformat()
                serializer = CommentSerializer(data=newCommentDict, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, 
                                        data=api_helper.construct_comment_object(serializer.data,
                                                                                 Author.objects.get(id=newCommentDict["author"])))
                return Response(status=400, data=serializer.errors)

# API view for likes on a post (endpoint /api/authors/<author_id>/posts/<post_id>/likes/)
class APIListLikesPost(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve all of the likes for a post", operation_description="Retrieve all of the likes for a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post", tags=["Likes"], responses=sample_dicts.sampleListLikesPostDict)
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        likes = Like.objects.filter(parentPost=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(status=200, data=api_helper.construct_list_of_likes(serializer.data, post.id, "post"))
    
# API view for likes on a comment (endpoint /api/authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes)
class APIListLikesComments(APIView):
    # Get list of likes originating on this comment
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve all of likes for a comment", operation_description="Retrieve all of the likes for a comment based on:\n\n* The id of the comment's author\n* The id of the comment's commented post\n* The id of the comment itself", tags=["Likes"], responses=sample_dicts.sampleListLikesCommentDict)
    def get(self, request, author_id, post_id, comment_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        try: 
            comment = Comment.objects.filter(parentPost=post).get(pk=HOST+"authors/"+
                                                                       author_id+"/posts/"+
                                                                       post_id+"/comments/"+
                                                                       comment_id)
        except Comment.DoesNotExist:
            return Response(status=404)
        likes = Like.objects.filter(parentComment=comment)
        serializer = LikeSerializer(likes, many=True)
        return Response(status=200, data=api_helper.construct_list_of_likes(serializer.data, comment.id, "comment"))
    
# API view for liked objects by the author (endpoint /api/authors/<author_id>/liked)
class APILiked(APIView):
    # Get list of likes on public objects (comments on public posts, public posts)
    # originating from this author
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a list of likes from public posts and their comments", operation_description="Retrieve a list of likes from public posts and their comments based on:\n\n* The author's own id", tags=["Likes"], responses=sample_dicts.sampleListLikedDict)
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        likes = Like.objects.filter(author=HOST+"authors/"+author_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(status=200, data=api_helper.construct_list_of_liked(serializer.data, author))
        
# API View for followers (endpoint /api/authors/<author_id>/followers)
class APIFollowers(APIView):
    # Get list of followers
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a list of followers for an author", operation_description="Retrieve a list of followers for an author based on:\n\n* The author's own id", tags=["Followers"], responses=sample_dicts.sampleFollowersDict)
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        user_followers = author.followers.all()
        followersList = []
        for user_follower in user_followers:
            followersList.append(user_follower.user_id)
        serializer = AuthorSerializer(followersList, many=True)
        return Response(status=200, data=api_helper.construct_list_of_followers(serializer.data))

# API View for a follower (endpoint /api/authors/<author_id>/followers/<foreign_author_id>)
# foreign_author_id should be an abs URL, encoded as a parameter or path element
class APIFollower(APIView):
    # Check if the specified foreign author is a follower of the author
    # Returns the author object if it exists
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Check whether an author is a followr for another author", operation_description="Check whether an author is a followr for another author based on:\n\n* The author's own id\n* The FULL id of the foreign author (i.e. https://socialdistcmput404.herokuapp.com/authors/{AUTHOR_ID})", tags=["Followers"], responses=sample_dicts.sampleGETAuthorDict, parameters=[{"allowReserved": True}])
    def get(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            decoded_foreign_author_id = urllib.parse.unquote(foreign_author_id, 'utf-8')
            followingAuthor = Author.objects.get(pk=decoded_foreign_author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            follower = targetAuthor.followers.all().get(user_id=followingAuthor)
            serialzer = AuthorSerializer(followingAuthor)
            return Response(status=200, data=api_helper.construct_author_object(serialzer.data))
        except UserFollowing.DoesNotExist:
            return Response(status=404)
        
    # Make the foreign author follow the author
    # foreign_author_id should be an abs URL, encoded as a parameter or path element
    # PUT body should contain author object, which is author object of requested follower
    @swagger_auto_schema(operation_summary="Allow one author to follow another author", operation_description="Allow one author to follow another author based on:\n\n* The author's own id\n* The FULL id of the foreign author (i.e. https://socialdistcmput404.herokuapp.com/authors/2/)", tags=["Followers"], parameters=[{"allowReserved": True}])
    def put(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id)):
            return Response(status=401)
        try: 
            decoded_foreign_author_id = urllib.parse.unquote(foreign_author_id, 'utf-8')
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
            # create copy of author on our server
            serializer = AuthorSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(status=400)
            serializer.save()
            followingAuthor = Author.objects.get(pk=decoded_foreign_author_id)
        try:
            targetAuthor.followers.all().get(user_id=followingAuthor)
            return Response(status=404)
        except:
            # link two authors together with relationship
            userfollowing = UserFollowing(user_id=followingAuthor, 
                                          following_user_id=targetAuthor)
            userfollowing.save()
            followRequest = FollowRequest.objects.get(target=targetAuthor, sender=followingAuthor)
            followRequest.delete()
            return Response(status=201)
    
    # Make the foreign author not follow the author
    # foreign_author_id should be an abs URL, encoded as a parameter or path element
    # same notes as before!
    @swagger_auto_schema(operation_summary="Allow one author to not follow another author", operation_description="Allow one author to not follow another author based on:\n\n* The author's own id\n* The FULL id of the foreign author (i.e. https://socialdistcmput404.herokuapp.com/authors/2/)", tags=["Followers"], responses=sample_dicts.sampleDELETEDict)
    def delete(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        try: 
            decoded_foreign_author_id = urllib.parse.unquote(foreign_author_id, 'utf-8')
            followingAuthor = Author.objects.get(pk=decoded_foreign_author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            userFollowing = targetAuthor.followers.all().get(user_id=followingAuthor)
            userFollowing.delete()
            return Response(status=200)
        except UserFollowing.DoesNotExist:
            return Response(status=404)

# TODO Fix required
class APIInbox(APIView):
    permission_classes = [auth.InboxPermission]
    @swagger_auto_schema(operation_summary="Retrieve a list of objects(posts, follow requests, post likes, comment likes, comments) within an author's inbox", operation_description="Retrieve an inbox object based on:\n\n* The author's own id", tags=["Inbox"], responses=sample_dicts.sampleInboxDict)
    def get(self, request, author_id):
        # get the owner first in order to get the inbox
        print()
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id)):
            return Response(status=401)
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            inbox=Inbox.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/inbox")
            serializer=InboxSerializer(inbox)
            itemList = []
            for post in inbox.posts.all():
                post_serial = PostSerializer(post, partial=True)
                post_author = Author.objects.get(pk=post_serial.data["author"])
                itemList.append(api_helper.construct_post_object(post_serial.data, post_author))
            for follow_request in inbox.requests.all():
                request_serial = FollowRequestSerializer(follow_request, partial=True)
                target = Author.objects.get(pk=request_serial.data["target"])
                sender = Author.objects.get(pk=request_serial.data["sender"])
                itemList.append(api_helper.construct_follow_request_object(request_serial.data,
                                                                           target,
                                                                           sender))
            for like in inbox.likes.all():
                like_serial = LikeSerializer(like, partial=True)
                like_author = Author.objects.get(pk=like_serial.data["author"])
                if like.likeType == "Post":
                    itemList.append(api_helper.construct_like_object(like_serial.data,
                                                                     like.parentPost.id, 
                                                                     "post",
                                                                     like_author))
                else:
                    itemList.append(api_helper.construct_like_object(like_serial.data,
                                                                     like.parentComment.id, 
                                                                     "comment",
                                                                     like_author))
            for comment in inbox.comments.all():
                comment_serial = CommentSerializer(comment, partial=True)
                comment_author = Author.objects.get(pk=comment_serial.data["author"])
                itemList.append(api_helper.construct_comment_object(comment_serial.data, comment_author))
            inboxDict = {}
            inboxDict["type"] = "inbox"
            inboxDict["author"] = author.id
            inboxDict["items"] = itemList
            # print(itemList)
            # for post in inbox.posts:
            #     print('here')
            # print(serializer.data)
            return Response(status=200, data=inboxDict)
        except Inbox.DoesNotExist:
            return Response(status=404)
    
    # send respective object in body
    @swagger_auto_schema(operation_summary="Send an object(posts, follow requests, post likes, comment likes, comments) to an author's inbox", 
    operation_description="Send an object(posts, follow requests, post likes, comment likes, comments) to an author's inbox based on:\n\n* The author's own id\n\nThe sampe object below is a like object, if you prefer to POST other objects (post, comments, follow requsts) to the inbox, please copy the objects from our other APIs", 
    tags=["Inbox"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            "@context": openapi.Schema(type=openapi.TYPE_STRING, example="https://www.w3.org/ns/activitystreams"),
            "summary": openapi.Schema(type=openapi.TYPE_STRING, example="TestAuthor Likes your post"),         
            "type": openapi.Schema(type=openapi.TYPE_STRING, example="Like"),
            "author": openapi.Schema(type=openapi.TYPE_OBJECT, 
            properties=
            {
                "id": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
                "host": openapi.Schema(type=openapi.TYPE_STRING, example=HOST),
                "displayName": openapi.Schema(type=openapi.TYPE_STRING, example="TestAuthor"), 
                "github": openapi.Schema(type=openapi.TYPE_STRING, example="www.githubtest.com"), 
                "profileImage": openapi.Schema(type=openapi.TYPE_STRING, example="testImage1.jpg"), 
                "type": openapi.Schema(type=openapi.TYPE_STRING, example="author"), 
                "url": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
            }
            ),
            "object":openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8/posts/53024f59-6a7f-4a0e-99c2-079e4a6ff0c1"),     
            },
        description="Sample Like object",
    ),)

    def post(self, request, author_id):
        # get the author object first
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            inbox = Inbox.objects.get(author=author)
        except:
            return Response(status=404)
        # if type is post, add that post (referred from post from APIPost)
        if request.data["type"]=="post":
            try:
                post = Post.objects.get(pk=request.data["id"])
            except Post.DoesNotExist:
                post_host_name = urllib.parse.urlparse(request.data["id"]).hostname
                post_scheme = urllib.parse.urlparse(request.data["id"]).scheme
                if post_scheme + "://" + post_host_name + "/" == HOST:
                    return Response(status=404)
                try:
                    post_author = Author.objects.get(pk=request.data["author"]["id"])
                except Author.DoesNotExist:
                    if request.data["author"]["host"] == HOST:
                        return Response(status=404)
                    new_author_serial = AuthorSerializer(data=request.data["author"], partial=True)
                    if not new_author_serial.is_valid():
                        return Response(status=400, data=new_author_serial.errors)
                    new_author_serial.save()
                postDict = dict(request.data)
                postDict["author"] = request.data["author"]["id"]
                new_post_serial = PostSerializer(data=postDict, partial=True)
                if not new_post_serial.is_valid():
                    return Response(status=400, data=new_post_serial.errors)
                new_post_serial.save()
                post = Post.objects.get(pk=request.data["post"]["id"])
            inbox.posts.add(post)
            return Response(status=200)
        
        # if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
        elif request.data["type"]=="Follow":
            try:
                targetAuthor = Author.objects.get(pk=request.data["object"]["id"])
            except Author.DoesNotExist:
                return Response(status=404)
            try:
                sendingAuthor = Author.objects.get(pk=request.data["actor"]["id"])
            except Author.DoesNotExist:
                if request.data["actor"]["host"] == HOST:  
                    return Response(status=404)
                new_author_serial = AuthorSerializer(data=request.data["actor"], partial=True)
                if not new_author_serial.is_valid():
                    return Response(status=400, data=new_author_serial.errors)
                new_author_serial.save()
                sendingAuthor = Author.objects.get(pk=request.data["actor"]["id"])
            try:
                followRequest = FollowRequest.objects.get(target=targetAuthor, sender=sendingAuthor)
            except FollowRequest.DoesNotExist:
                followRequest = FollowRequest.objects.create(sender=sendingAuthor, 
                                                             target=targetAuthor,
                                                             date=datetime.datetime.now().isoformat())
            inbox.requests.add(followRequest)
            return Response(status=200)
            
        # if the type is “like” then add that like to AUTHOR_ID’s inbox
        elif request.data["type"]=="Like":
            isPost = False
            try:
                post = Post.objects.get(pk=request.data["object"])
                isPost = True
            except Post.DoesNotExist:
                try: 
                    comment = Comment.objects.get(pk=request.data["object"])
                except Comment.DoesNotExist:
                    return Response(status=404)
            try:
                like_author = Author.objects.get(pk=request.data["author"]["id"])
            except Author.DoesNotExist:
                if request.data["author"]["host"] == HOST:
                    return Response(status=404, data="same host")
                new_author_serial = AuthorSerializer(data=request.data["author"], partial=True)
                if not new_author_serial.is_valid():
                    return Response(status=400, data=new_author_serial.errors)
                new_author_serial.save()
            while True:
                # OLD start
                # like_id = get_random_string(20)
                # OLD end

                # New start
                # Generate a UUID
                UUID=uuid.uuid4()
                like_id=str(UUID)
                # New end

                try:
                    like = Like.objects.get(pk=request.data["object"]+"/likes/"+like_id)
                    continue
                except Like.DoesNotExist:
                    break
            like_dict = dict(request.data)
            like_dict["id"] = request.data["object"]+"/likes/"+like_id
            like_dict["author"] = request.data["author"]["id"]
            like_dict["published"] = datetime.datetime.now().isoformat()
      
            like_serial = LikeSerializer(data=like_dict, partial=True)
            if not like_serial.is_valid():
                return Response(status=400, data=like_serial.errors)
            like_serial.save()
            like = Like.objects.get(pk=request.data["object"]+"/likes/"+like_id)
            if (isPost):
                like.parentPost = post
                like.likeType = "Post"
            else:
                like.parentComment = comment
                like.likeType = "Comment"
            like.save()
            inbox.likes.add(like)
            return Response(status=200)
        
        # if the type is “comment” then add that comment to AUTHOR_ID’s inbox    
        elif request.data["type"]=="comment":
            try:
                post = Post.objects.get(pk=request.data["id"].split("/comments")[0])
            except Post.DoesNotExist:
                return Response(status=404)
            try:
                post_author = Author.objects.get(pk=request.data["author"]["id"])
            except Author.DoesNotExist:
                if request.data["author"]["host"] == HOST:
                    return Response(status=404)
                new_author_serial = AuthorSerializer(data=request.data["author"], partial=True)
                if not new_author_serial.is_valid():
                    return Response(status=400, data=new_author_serial.errors)
                new_author_serial.save()
            try:
                comment = Comment.objects.get(pk=request.data["id"])
            except Comment.DoesNotExist:
                return Response(status=404)
            inbox.comments.add(comment)
            return Response(status=200)
            
    # TBA
    @swagger_auto_schema(operation_summary="Clear an author's inbox",operation_description="Clear an author's inbox based on:\n\n* The author's own id", tags=["Inbox"], responses=sample_dicts.sampleDELETEDict)
    def delete (request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            inbox=Inbox.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/inbox")
        except Inbox.DoesNotExist:
            return Response(status=404)
        # making inbox empty by setting all the fields as blank except author, every other field the same
        # Delete inbox and recreating it
        inbox.delete()
        inbox.create(inbox_id=HOST+"authors/"+author_id+"/inbox", author=HOST+"authors/"+author_id, post=[])

        return Response(status=200)

# TODO Please generate appropriate documentation of the following API to root_project/openapi.json

class APIPosts(APIView): 
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve all of the posts from every author",operation_description="Retrieve all of the posts from every author", tags=["Posts"], responses=sample_dicts.sampleListEveryPostDict)
    def get(self, request):
        author_posts_pair = []
        for each_author in Author.objects.filter(host=HOST):
            if not Post.objects.filter(author=each_author).count():
                continue
            posts = PostSerializer(Post.objects.filter(author=each_author).filter(visibility="VISIBLE").filter(unlisted=False), many=True)
            author_posts_pair.append([each_author, posts.data])
            # prints num_post for each author
            # print("num_post for "+dict(AuthorSerializer(each_author).data)["id"]+": "+str(len(posts.data)))
            
        return Response(status=200, data=api_helper.construct_list_of_all_posts(author_posts_pair))