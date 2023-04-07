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

# This file contains the views for the different endpoints of our API

# Sources:
# https://docs.djangoproject.com/en/4.1/topics/db/queries/#:~:text=Creating%20objects&text=To%20create%20an%20object%2C%20instantiate,save%20it%20to%20the%20database.&text=This%20performs%20an%20INSERT%20SQL,method%20has%20no%20return%20value.
# https://docs.djangoproject.com/en/4.1/ref/request-response/
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/
# https://testdriven.io/blog/drf-views-part-1/
# https://www.geeksforgeeks.org/adding-permission-in-api-django-rest-framework/
# https://stackoverflow.com/questions/25943850/django-package-to-generate-random-alphanumeric-strin
# https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/

from django.db import IntegrityError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from django.http import QueryDict
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import auth
from . import api_helper, sample_dicts
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, InboxSerializer, FollowRequestSerializer
from .models import Author, Post, Comment, Like, Inbox, UserFollowing, FollowRequest
import uuid
import base64 
import urllib.parse
import datetime

# Host name
HOST = "https://socialdistcmput404.herokuapp.com/"

# API View for single author API queries (endpoint /api/authors/<author_id>/)
class APIAuthor(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve an author's profile", operation_description="Retrieve an author's profile based on:\n\n* The author's id", tags=["Author's Profile"], responses=sample_dicts.sampleGETAuthorDict)
    # Getting the information of a single author with that id
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

    # Setting Up swagger schema
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
            "github": openapi.Schema(type=openapi.TYPE_STRING, example="https://github.com/testUser"), 
            "profileImage": openapi.Schema(type=openapi.TYPE_STRING, example="http://sampleUserImage.com/1.jpg"), 
            "type": openapi.Schema(type=openapi.TYPE_STRING, example="author"), 
            "url": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"), 
        },
        description="Sample User object",
    ),)
    # Edit the author object with the specified ID  
    # When posting, send an author object in body in JSON with modified fields
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
            # Try to Update the author with Author Serializer
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
            # Request data does not have vaild fields, return 400 with errors
            return Response(status=400, data=serializer.errors)
        # Request data is not in right JSON format, return 400 with errors
        except:
            return Response(status=400, data=serializer.errors)

# API View for list of authors API queries (endpoint /api/authors/)
class APIListAuthors(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve every author's profile within the server", operation_description="Retrieve every author's profile within the server", tags=["Authors List"], responses=sample_dicts.sampleListAuthorDict)
    # Getting list of authors, with optional pagination
    def get(self, request):
        # Check if user provided query paramters, paginate if they do
        if (request.META["QUERY_STRING"] != ""):
            queryDict = QueryDict(request.META["QUERY_STRING"])
            pageNum = 1 # default page
            sizeNum = 5 # default page size
            # Check if value provided with "page" query value is vaild
            if "page" in queryDict:
                try:
                    pageNum = int(queryDict["page"])
                except ValueError:
                    return Response(status=404)
            # Check if value provided with "size" query value is vaild
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
    
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Create a new author's profile", 
    operation_description="Create an author's profile without any fields", 
    tags=["Author's Profile"], 
    responses=sample_dicts.samplePUTAuthorDict,
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
    # Create an author's profile, provide the user creditenals
    def put(self, request):
        # Extract user creditenals
        username = request.data["username"]
        email = request.data.get("email", "") # if email is not provided, set it to empty string
        password = request.data["password1"]
        try:
            user = User.objects.create_user(username, email, password)
            # Generate a UUID for the author object
            UUID=uuid.uuid4()
            # Create author object for user
            author = Author.objects.create(
                user=user,
                id=HOST+"authors/"+str(UUID),
                host=HOST,
                displayName=username,
                github="",
                profileImage="",
            )
            # Create inbox for user
            inbox = Inbox.objects.create(
                inboxID=HOST+"authors/"+str(UUID)+"/inbox",
                author=author
            )
            return Response(status=201)
        # Error Handling
        except (IntegrityError, ValueError) as e:
            if IntegrityError:
                return Response(status=409, data="An account with that username already exists.")
            else:
                return Response(status=400, data="Account creation failed.")

# API View for single post queries (endpoint /api/authors/<author_id>/posts/<post_id>)
class APIPost(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a public post", operation_description="Retrieve a public post's information based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"], responses=sample_dicts.sampleGETPostDict)
    # Get a single post with the specified ID belonging to the specifed author
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

    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Edit a public post", operation_description="Edit a public post's information based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"],responses=sample_dicts.samplePOSTPostDict, request_body=PostSerializer)
    # Edit a single post
    # When POSTing, send a post object in JSON with the modified fields
    # Cannot edit a private post!
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
        # Try to POST the post with PostSerializer
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

    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Create a public post", operation_description="Create a public post based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"],responses=sample_dicts.samplePOSTPostDict, request_body=PostSerializer)   
    def put(self, request, author_id, post_id):
        # Check if author exists
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
            if post.visibility == "FRIENDS":
                return Response(status=404)
            # Construct post with PostSerializer
            postDict = dict(request.data)
            postDict["author"] = HOST+"authors/"+author_id
            serializer = PostSerializer(post, data=postDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_post_object(serializer.data, author))
            return Response(status=400, data=serializer.errors)
        # If resource does not exists, creates a post with the specified ID
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
                return Response(status=201, data=api_helper.construct_post_object(serializer.data, author))
            return Response(status=400, data=serializer.errors)
        
    # Delete the single post
    # Cannot delete private posts!
    
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Delete a public post", operation_description="Delete a public post's information based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Posts"], responses=sample_dicts.sampleDELETEPostDict)
    def delete(self, request, author_id, post_id):
        # Checks if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Checks if request comes from authorized source
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        # Checks if post exists and is public
        try:
            post = Post.objects.filter(visibility="VISIBLE").get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # If passed everything, DELETE the post
        post.delete()
        return Response(status=200)
    
# API View for a list of post queries (endpoint /api/authors/<author_id>/posts/)
class APIListPosts(APIView):
    permission_classes = [auth.RemotePermission]

    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve a list of posts (public posts only) for a specific author", operation_description="Retrieve a list of posts (public posts only) for a specific author based on:\n\n* The author's own id", tags=["Post List"], responses=sample_dicts.sampleListPostsDict)
    # Returns a list of the public posts of the specified author, with optional pagination
    def get(self, request, author_id):
        # Check if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        posts = Post.objects.filter(author=author).filter(visibility="VISIBLE").order_by('-published')
        serializer = PostSerializer(posts, many=True)
        # Check if query string provided, paginate if is
        if (request.META["QUERY_STRING"] == ""):
            return Response(status=200, data=api_helper.construct_list_of_posts(serializer.data, author))
        queryDict = QueryDict(request.META["QUERY_STRING"])
        pageNum = 1 # default page
        sizeNum = 5 # default page size
        # Check if value provided with "page" field is vaild
        if "page" in queryDict:
            try:
                pageNum = int(queryDict["page"])
            except ValueError:
                return Response(status=404)
         # Check if value provided with "size" field is vaild
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

    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Create a post with a randomized post id", operation_description="Create a post with a randomized post id based on:\n\n* The author's own id", tags=["Post List"], request_body=PostSerializer, responses=sample_dicts.samplePOSTPostDict)
    def post(self, request, author_id):
        # Checks if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Checks if request comes from authorized source
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        while True:
            # generate new UUID
            UUID=uuid.uuid4()
            post_id=str(UUID)
            # Check if post has that ID already, regenerate if case
            try:
                post = Post.objects.get(postID=HOST+"authors/"+author_id+"/posts/"+post_id)
                continue
            # Generate new post when new, unique ID found, with PostSerializer
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

# API View used to fetch image posts as images (endpoint /api/authors/<author_id>/posts/<post_id>/image)
class APIImage(APIView):
    permission_classes = [auth.RemotePermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve an image post", operation_description="Retrieve an image post based on:\n\n* The id of the post's author\n* The id of the post itself", tags=["Images"], responses=sample_dicts.sampleImagePostGETDict)
    # Gets the image binary of an image post with the specified ID from the specified author
    def get(self, request, author_id, post_id):
        # Checks if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if resource already exists, if it does, acts like a GET request
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            # Checks if request comes from authorized source
            if post.visibility == "FRIENDS" and not api_helper.is_follower(request.user, author):
                return Response(status=401)
            # Checks if requested post is an image
            if post.contentType != "image/png;base64" and post.contentType != "image/jpeg;base64" and post.contentType != "image/jpg;base64":
                return Response(status=404)
            # Decodes base64 string of image into image binary
            content_bytes_base64 = post.content.encode('ascii')
            return HttpResponse(status=200, 
                            content=base64.b64decode(content_bytes_base64), 
                            content_type=post.contentType)
        except Post.DoesNotExist:
            return Response(status=404)
    
#API View for single comment queries (endpoint /api/authors/<author_id>/posts/<post_id>/comments/<comment_id>)
class APIComment(APIView):
    permission_classes = [auth.RemotePermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve a comment within a post", operation_description="Retrieve a comment within a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post\n* The id of the comment itself", tags=["Comments"], responses=sample_dicts.sampleGETCommentDict)
    # Get a single comment with the specified ID on the specified post from the specified author
    def get(self, request, author_id, post_id, comment_id):
        # Check if post author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if post exists
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # Check if request comes from authorized source, for a private post, only author can access!
        if post.visibility == "FRIENDS" and (not request.user.is_authenticated or request.user.author != author):
            return Response(status=401)
        # Check if comment exists
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
            return Response(status=200, data=api_helper.construct_comment_object(serialzer.data, author))
        except Comment.DoesNotExist:
            return Response(status=404)
    
#API View for list of comments queries (endpoint /api/authors/<author_id>/posts/<post_id>/comments/)
class APIListComments(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve all of the comments within a post", operation_description="Retrieve all of the comments within a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post", tags=["Comments"], responses=sample_dicts.sampleListCommentsDict)
    # Get list of comments on the specified post by the specified author, with optional pagination
    def get(self, request, author_id, post_id):
        # Checks if the post author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Checks if post exists
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # For a private post, only the author can access the comments!
        if post.visibility == "FRIENDS" and (not request.user.is_authenticated or request.user.author != author):
            return Response(status=401)
        comments = Comment.objects.filter(parentPost=HOST+"authors/"+author_id+"/posts/"+post_id)
        serializer = CommentSerializer(comments, many=True)
        # Check if query string provided, paginate if it is
        if (request.META["QUERY_STRING"] == ""):
            return Response(status=200, data=api_helper.construct_list_of_comments(serializer.data,
                                                                               post))
        queryDict = QueryDict(request.META["QUERY_STRING"])
        pageNum = 1 # default page
        sizeNum = 5 # default page size
        # Check if value provided with "page" field is valid
        if "page" in queryDict:
            try:
                pageNum = int(queryDict["page"])
            except ValueError:
                return Response(status=404)
        # Check if value provided with "size" field is valid
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

    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Create a comment in a post", 
    operation_description="Create a comment in a post based on:\n\n* The id of the comment's author\n* The id of the comment's commented post", 
    tags=["Comments"],
    responses=sample_dicts.samplePOSTCommentDict, 
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            "id": openapi.Schema(type=openapi.TYPE_STRING, example="https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3"),
            "comment": openapi.Schema(type=openapi.TYPE_STRING, example="Test comment content"),         
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
        # Check if post author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if post exists
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        while True:
            # Generate a UUID
            UUID=uuid.uuid4()
            comment_id=str(UUID)
            
            # Check if comment with that ID already exists
            try:
                comment = Comment.objects.get(id=HOST+
                                              "authors/"+
                                              author_id+
                                              "/posts/"+
                                              post_id+
                                              "/comments/"+
                                              comment_id)
                continue
            # If generated comment ID doesn't exist, produce comment!
            except Comment.DoesNotExist:
                newCommentDict = dict(request.data)
                newCommentDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id+"/comments/"+comment_id
                newCommentDict["parentPost"] = HOST+"authors/"+author_id+"/posts/"+post_id

                # Check if author is saved in our DB (remote or local)
                try:
                    commentAuthor = Author.objects.get(pk=newCommentDict["author"]["id"])
                except Author.DoesNotExist:
                    # Check if author is a remote author not yet saved
                    if newCommentDict["author"]["host"] == HOST:
                        # Author is not remote, but doesn't exist in our DB, return 404
                        return Response(status=404)
                    # Save new remote author into our DB
                    commentAuthorSerializer = AuthorSerializer(data=newCommentDict["author"])
                    # Check for errors in provided author object
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
    # Get the list of likes on a specified post by the specified author
    def get(self, request, author_id, post_id):
        # Check if post author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if post exists
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        #  Showing likes with LikeSerializer
        likes = Like.objects.filter(parentPost=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(status=200, data=api_helper.construct_list_of_likes(serializer.data, post.id, "post"))
    
# API view for likes on a comment (endpoint /api/authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes)
class APIListLikesComments(APIView):
    permission_classes = [auth.RemotePermission]
    
    @swagger_auto_schema(operation_summary="Retrieve all of likes for a comment", operation_description="Retrieve all of the likes for a comment based on:\n\n* The id of the comment's author\n* The id of the comment's commented post\n* The id of the comment itself", tags=["Likes"], responses=sample_dicts.sampleListLikesCommentDict)
      # Get list of likes originating on this comment
    def get(self, request, author_id, post_id, comment_id):
        # Check if post author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if post exists
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        # Check if comment exists
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
    permission_classes = [auth.RemotePermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve a list of likes from public posts and their comments", operation_description="Retrieve a list of likes from public posts and their comments based on:\n\n* The author's own id", tags=["Likes"], responses=sample_dicts.sampleListLikedDict)
    # Get list of likes on public objects (comments on public posts, public posts)
    # originating from this author
    def get(self, request, author_id):
        # Check if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Author does not exist")
        likes = Like.objects.filter(author=HOST+"authors/"+author_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(status=200, data=api_helper.construct_list_of_liked(serializer.data, author))
        
# API View for followers (endpoint /api/authors/<author_id>/followers)
class APIFollowers(APIView):
    permission_classes = [auth.RemotePermission]
    @swagger_auto_schema(operation_summary="Retrieve a list of followers for an author", operation_description="Retrieve a list of followers for an author based on:\n\n* The author's own id", tags=["Followers"], responses=sample_dicts.sampleFollowersDict)
    # Get list of followers for this local author
    def get(self, request, author_id):
        # Check if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Author does not exist")
        user_followers = author.followers.all()
        followersList = []
        for user_follower in user_followers:
            followersList.append(user_follower.user_id)
        serializer = AuthorSerializer(followersList, many=True)
        return Response(status=200, data=api_helper.construct_list_of_followers(serializer.data))

# API View for a follower (endpoint /api/authors/<author_id>/followers/<foreign_author_id>)
# foreign_author_id should be an abs URL, encoded as a parameter or path element
class APIFollower(APIView):
    permission_classes = [auth.RemotePermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Check whether an author is a follower for another author", operation_description="Check whether an author is a followr for another author based on:\n\n* The author's own id\n* The FULL id of the foreign author (i.e. https://socialdistcmput404.herokuapp.com/authors/{AUTHOR_ID})", tags=["Followers"], responses=sample_dicts.sampleGETAuthorDict, parameters=[{"allowReserved": True}])
    # Check if the specified foreign or local author is a follower of the author
    # Returns the author object if it exists
    def get(self, request, author_id, foreign_author_id):
        # Check if author exists
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Target author does not exist")
        # Check if following author exists
        try: 
            # Decode foreign author URL
            decoded_foreign_author_id = urllib.parse.unquote(foreign_author_id, 'utf-8')
            followingAuthor = Author.objects.get(pk=decoded_foreign_author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Following author does not exist")
        # Check if following author follows target author
        try:
            follower = targetAuthor.followers.all().get(user_id=followingAuthor)
            serialzer = AuthorSerializer(followingAuthor)
            return Response(status=200, data=api_helper.construct_author_object(serialzer.data))
        except UserFollowing.DoesNotExist:
            return Response(status=404, data="Following author does not follow target author")
        
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Allow one author to follow another author", operation_description="Allow one author to follow another author based on:\n\n* The author's own id\n* The FULL id of the foreign author (i.e. https://socialdistcmput404.herokuapp.com/authors/{AUTHOR_ID})", tags=["Followers"], parameters=[{"allowReserved": True}])
    # Make the author (foreign or local) follow the author
    # foreign_author_id should be an abs URL, encoded as a parameter or path element
    # PUT body should contain author object, which is author object of requested follower
    def put(self, request, author_id, foreign_author_id):
        # Check if target author exists
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Author does not exist")
        # Check if from authorized source
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id)):
            return Response(status=401)
        # Check if author exists in our DB
        try: 
            decoded_foreign_author_id = urllib.parse.unquote(foreign_author_id, 'utf-8')
            # return Response(status=201, data=request.data)
            followingAuthor = Author.objects.get(pk=foreign_author_id)
            # return Response(status=201, data=followingAuthor.values())
        except:
            # Create copy of author on our server
            serializer = AuthorSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(status=400, data=serializer.errors)
            serializer.save()
            followingAuthor = Author.objects.get(pk=decoded_foreign_author_id)
        # Check if author is already following target
        try:
            targetAuthor.followers.all().get(user_id=followingAuthor)
            return Response(status=404, data="Already following!")
        except:
            # Link two authors together with relationship
            userfollowing = UserFollowing(user_id=followingAuthor, 
                                          following_user_id=targetAuthor)
            userfollowing.save()
            followRequest = FollowRequest.objects.get(target=targetAuthor, sender=followingAuthor)
            followRequest.delete()
            return Response(status=201)
    
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Allow one author to not follow another author", operation_description="Allow one author to not follow another author based on:\n\n* The author's own id\n* The FULL id of the foreign author (i.e. https://socialdistcmput404.herokuapp.com/authors/{AUTHOR_ID})", tags=["Followers"], responses=sample_dicts.sampleDELETEFollowersDict)
    # Make the foreign author not follow the author
    # foreign_author_id should be an abs URL, encoded as a parameter or path element
    def delete(self, request, author_id, foreign_author_id):
        # Check if target author exists
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Target author does not exist")
        # Check if request comes from authorized source
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id )):
            return Response(status=401)
        # Check if following author exists in our DB
        try: 
            decoded_foreign_author_id = urllib.parse.unquote(foreign_author_id, 'utf-8')
            followingAuthor = Author.objects.get(pk=decoded_foreign_author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Following author does not exist")
        # Check if following author follows target, delete relationship if they do
        try:
            userFollowing = targetAuthor.followers.all().get(user_id=followingAuthor)
            userFollowing.delete()
            return Response(status=200)
        except UserFollowing.DoesNotExist:
            return Response(status=404, data="Following author not following target")
        
# API endpoint for the inbox of <author_id> (endpoint /api/authors/<author_id>/inbox/)
class APIInbox(APIView):
    permission_classes = [auth.InboxPermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve a list of objects(posts, follow requests, post likes, comment likes, comments) within an author's inbox", operation_description="Retrieve an inbox object based on:\n\n* The author's own id", tags=["Inbox"], responses=sample_dicts.sampleInboxDict)
    # Return the list of items within an author's inbox
    def get(self, request, author_id):
        # Check if request from authorized source
        if not request.user.is_authenticated or (not request.user.is_staff and author_id != api_helper.extract_UUID(request.user.author.id)):
            return Response(status=401)
        # Check if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Author does not exist")
        try:
            inbox=Inbox.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/inbox")
            serializer=InboxSerializer(inbox)
            itemList = []
            # Extract posts in inbox
            for post in inbox.posts.order_by("-published"):
                post_serial = PostSerializer(post, partial=True)
                post_author = Author.objects.get(pk=post_serial.data["author"])
                itemList.append(api_helper.construct_post_object(post_serial.data, post_author))
            # Extract follow requests in inbox
            for follow_request in inbox.requests.order_by("-date"):
                request_serial = FollowRequestSerializer(follow_request, partial=True)
                target = Author.objects.get(pk=request_serial.data["target"])
                sender = Author.objects.get(pk=request_serial.data["sender"])
                itemList.append(api_helper.construct_follow_request_object(request_serial.data,
                                                                           target,
                                                                           sender))
            # Extract likes in inbox
            for like in inbox.likes.order_by("-published"):
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
            # Extract comments in inbox
            for comment in inbox.comments.order_by("-published"):
                comment_serial = CommentSerializer(comment, partial=True)
                comment_author = Author.objects.get(pk=comment_serial.data["author"])
                itemList.append(api_helper.construct_comment_object(comment_serial.data, comment_author))
            inboxDict = {}
            inboxDict["type"] = "inbox"
            inboxDict["author"] = author.id
            inboxDict["items"] = itemList
            return Response(status=200, data=inboxDict)
        except Inbox.DoesNotExist:
            return Response(status=404, data="Author doesn't have an inbox")
    
    # Setting Up swagger schema for POST in APIInbox
    @swagger_auto_schema(operation_summary="Send an object(posts, follow requests, post likes, comment likes, comments) to an author's inbox", 
    operation_description="Send an object(posts, follow requests, post likes, comment likes, comments) to an author's inbox based on:\n\n* The author's own id\n\nThe sampe object below is a like object, if you prefer to POST other objects (post, comments, follow requsts) to the inbox, please copy the objects from our other APIs", 
    tags=["Inbox"],
    responses=sample_dicts.sampleDELETEDict,
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
    # Add an object to the author's inbox (Like, Comment, Post, Follow Request)
    def post(self, request, author_id):
        # Check if author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404, data="Author does not exist")
        # Check if inbox exists
        try:
            inbox = Inbox.objects.get(author=author)
        except:
            return Response(status=404, data="Inbox does not exist")
        # If type is post, add that post (referred from post from APIPost)
        if request.data["type"]=="post":
            # Check if post is a local post and exists
            try:
                post = Post.objects.get(pk=request.data["id"])
            except Post.DoesNotExist:
                # Extract post host and check if local
                post_host_name = urllib.parse.urlparse(request.data["id"]).hostname
                post_scheme = urllib.parse.urlparse(request.data["id"]).scheme
                # If local, post does not exist and do not allow POSTing
                if post_scheme + "://" + post_host_name + "/" == HOST:
                    return Response(status=404, data="Post does not exist")
                # Check if post author is local and exists
                try:
                    post_author = Author.objects.get(pk=request.data["author"]["id"])
                except Author.DoesNotExist:
                    # If local, author does not exist and do not allow POSTing
                    if request.data["author"]["host"] == HOST:
                        return Response(status=404, data="Author does not exist")
                    new_author_serial = AuthorSerializer(data=request.data["author"], partial=True)
                    if not new_author_serial.is_valid():
                        return Response(status=400, data=new_author_serial.errors)
                    new_author_serial.save()
                postDict = dict(request.data)
                # Source: https://www.programiz.com/python-programming/methods/string/join
                # Programiz
                # Title: Python String join()
                try:
                    if type(postDict["categories"]) is list:
                            postDict["categories"] = ' '.join(postDict["categories"])
                except KeyError:
                    postDict["categories"] = "Uncategorized"
                postDict["author"] = request.data["author"]["id"]
                new_post_serial = PostSerializer(data=postDict, partial=True)
                if not new_post_serial.is_valid():
                    return Response(status=400, data=new_post_serial.errors)
                new_post_serial.save()
                post = Post.objects.get(pk=request.data["id"])
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
                # Generate a UUID
                UUID=uuid.uuid4()
                like_id=str(UUID)
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
                comment_dict = dict(request.data)
                comment_dict["parentPost"] = request.data["id"].split("/comments")[0]
                comment_dict["published"] =  datetime.datetime.now().isoformat()
                comment_dict["author"] = request.data["author"]["id"]
                comment_serial = CommentSerializer(data=comment_dict, partial=True)
                if not comment_serial.is_valid():
                    return Response(status=400, data=comment_serial.errors)
                comment_serial.save()
                comment = Comment.objects.get(pk=request.data["id"])
            inbox.comments.add(comment)
            return Response(status=200)
            
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Clear an author's inbox",operation_description="Clear an author's inbox based on:\n\n* The author's own id", tags=["Inbox"], responses=sample_dicts.sampleDELETEInboxDict)
    # Clearing an inbox
    def delete (self, request, author_id):
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
        new_inbox = Inbox(inboxID=HOST+"authors/"+author_id+"/inbox", 
                          author=author)
        new_inbox.save()
        return Response(status=200)

"""
Below endpoints are not specified in the specification of the project.
These endpoints are intended for local server use only for efficient use of AJAX requests.
"""
class APIPosts(APIView): 
    # Serves to retrieve all of the public posts in our server
    permission_classes = [auth.RemotePermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve all of the posts from every author",operation_description="Retrieve all of the posts from every author", tags=["Posts"], responses=sample_dicts.sampleListEveryPostDict)
    def get(self, request):
        author_posts_pair = []
        for each_author in Author.objects.filter(host=HOST):
            if not Post.objects.filter(author=each_author).count():
                continue
            posts = PostSerializer(Post.objects.filter(author=each_author).filter(visibility="VISIBLE").filter(unlisted=False).order_by("-published"), many=True)
            author_posts_pair.append([each_author, posts.data])
            
        return Response(status=200, data=api_helper.construct_list_of_all_posts(author_posts_pair))

class APIAuthorPrivatePosts(APIView):
    # Serves to return all private and unlisted posts from our server
    permission_classes = [auth.RemotePermission]
    # Setting Up swagger schema
    @swagger_auto_schema(operation_summary="Retrieve all of the private and unlisted posts from an author",operation_description="Retrieve all of the private and unlisted posts from an author using the author's id", tags=["Posts"], responses=sample_dicts.sampleListEveryPostDict)
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # ONLY CHANGE: from visible to private
        posts = Post.objects.filter(author=author).filter(visibility="FRIENDS").order_by('-published') | Post.objects.filter(author=author).filter(unlisted=True).order_by('-published') 
        
        # Return all post from author
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