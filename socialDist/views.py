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

# Sources:
# https://docs.djangoproject.com/en/4.1/topics/db/queries/#:~:text=Creating%20objects&text=To%20create%20an%20object%2C%20instantiate,save%20it%20to%20the%20database.&text=This%20performs%20an%20INSERT%20SQL,method%20has%20no%20return%20value.
# https://docs.djangoproject.com/en/4.1/ref/request-response/
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/
# https://testdriven.io/blog/drf-views-part-1/
# https://www.geeksforgeeks.org/adding-permission-in-api-django-rest-framework/
# https://stackoverflow.com/questions/25943850/django-package-to-generate-random-alphanumeric-strin
# https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/

from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import QueryDict
from rest_framework import status
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
import urllib.parse

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

from .models import Author, Post, Comment, Like, Server, Inbox, UserFollowing
from . import api_helper
import base64 

HOST = "https://socialdistcmput404.herokuapp.com/"

# API View for single author API queries (endpoint /api/authors/<author_id>/)
class APIAuthor(APIView):
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

    # Edit the author object  
    # When posting, send an author object in body in JSON with modified fields
    def post(self, request, id):
        # Check if author exists, 404 if not
        try:
            author = Author.objects.get(pk=HOST+"authors/"+id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if request is from an authorized source (only user and admin can call this!), 401 if not
        if not request.user.is_authenticated and request.user.id != id:
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
    
    def put(self, request):
        username = request.data["username"]
        email = request.data.get("email", "") # if email is not provided, set it to empty string
        password = request.data["password1"]
        try:
            user = User.objects.create_user(username, email, password)
            author = Author.objects.create(
                user=user,
                id=HOST+"authors/" + str(user.pk),
                host=HOST,
                displayName=username,
                github="",
                profileImage="",
            )
            return Response(status=201)
        except (IntegrityError, ValueError) as e:
            if IntegrityError:
                return Response(status=409, data="An account with that username already exists.")
            else:
                return Response(status=400, data="Account creation failed.")

# API View for single post queries (endpoint /api/authors/<author_id>/posts/<post_id>)
class APIPost(APIView):
    # Get a single post
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
        if not request.user.is_authenticated and request.user.id != author_id:
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
    def put(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if resource already exists, if it does, acts like POST!
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            # Check if request is from an authorized source (only user and admin can call this!), 401 if not
            if not request.user.is_authenticated and request.user.id != author_id:
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
            if not request.user.is_authenticated and request.user.id != author_id:
                return Response(status=401)
            postDict = dict(request.data)
            postDict["author"] = HOST+"authors/"+author_id
            postDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id
            serializer = PostSerializer(data=postDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_post_object(serializer.data))
            return Response(status=400, data=serializer.errors)
        
    # Delete the single post
    # Cannot delete private posts!
    def delete(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated and request.user.id != author_id:
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
    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated and request.user.id != author_id:
            return Response(status=401)
        while True:
            post_id = get_random_string(10)
            try:
                post = Post.objects.get(postID=HOST+"authors/"+author_id+"/posts/"+post_id)
                continue
            except:
                newPostDict = dict(request.data)
                newPostDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id
                newPostDict["author"]=HOST+"authors/"+author_id
                serializer = PostSerializer(data=newPostDict, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, 
                                        data=api_helper.construct_post_object(serializer.data, author))
                return Response(status=400, data=serializer.errors)

# Endpoint used to fetch image posts as images (endpoint /api/authors/<author_id>/posts/<post_id>/image)
class APIImage(APIView):
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if resource already exists, if it does, acts like a GET request
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            # TODO: create a function to check if requesting user is allowed
            if post.visibility == "PRIVATE":
                return Response(status=401)
            if post.contentType != "image/png;base64" and post.contentType != "image/jpeg;base64":
                return Response(status=404)
            content_bytes_base64 = post.content.encode('ascii')
            return HttpResponse(status=200, 
                            content=base64.b64decode(content_bytes_base64), 
                            content_type=post.contentType)
        except Post.DoesNotExist:
            return Response(status=404)
    
#API View for single comment queries (endpoint /api/authors/<author_id>/posts/<post_id>/comments/<comment_id>)
class APIComment(APIView):
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
    
#API View for list of comments queries (endpoint /api/authors/<author_id>/posts/<post_id>/comments/)
class APIListComments(APIView):
    # Get list of comments
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
                                                                               author, 
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
            comment_id = get_random_string(20)
            try:
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
                    if not commentAuthorSerializer.is_vaild():
                        return Response(status=400, data=commentAuthorSerializer.errors)
                    commentAuthorSerializer.save()
                newCommentDict["author"] = newCommentDict["author"]["id"]
                serializer = CommentSerializer(data=newCommentDict, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, 
                                        data=api_helper.construct_comment_object(serializer.data,
                                                                                 Author.objects.get(id=newCommentDict["author"])))
                return Response(status=400, data=serializer.errors)

# API view for likes on a post (endpoint /api/authors/<author_id>/posts/<post_id>/likes/)
class APIListLikesPost(APIView):
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
        return Response(status=200, data=api_helper.construct_list_of_likes(serializer.data, post.id))
    
# API view for likes on a comment (endpoint /api/authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes)
class APIListLikesComments(APIView):
    # Get list of likes originating on this comment
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
        return Response(status=200, data=api_helper.construct_list_of_likes(serializer.data, comment.id))
    
# API view for liked objects by the author (endpoint /api/authors/<author_id>/liked)
class APILiked(APIView):
    # Get list of likes on public objects (comments on public posts, public posts)
    # originating from this author
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
    def put(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated and request.user.id != author_id:
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
            return Response(status=201)
    
    # Make the foreign author not follow the author
    # foreign_author_id should be an abs URL, encoded as a parameter or path element
    # same notes as before!
    def delete(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated and request.user.id != author_id:
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
"""class APIInbox(APIView):
    def get(self, request, author_id):
        # get the owner first in order to get the inbox
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            inbox=Inbox.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/inbox")
            serializer=InboxSerializer(inbox)
            # 1. getting the type
            inboxDict=dict(serializer.data)
            inboxDict["type"]="inbox"
            # 2. getting the author (which is the getter him/herself)
            serializer= AuthorSerializer(author)
            inboxDict["author"]=serializer["id"]

            # 3. getting all of the items (post, comment, likes, followrequsts)
            itemList=[]
            # 3a. getting post objects
            # 3a filter the posts to ensure they are all followers
            # 3a.1 Get id for every follower (learned from APIFollowers)
            user_followers = author.followers.all()
            followersList = []
            for user_follower in user_followers:
                followersList.append(user_follower.user_id)
            # 3a.2 use those id's to get their posts (learned from APIListPosts)
            postList = []
            # 3a.3 For each follower (each id), get all posts
            for each in followersList:
                posts = Post.objects.filter(author=each)
                serializer = PostSerializer(posts, many=True)
                # Post list to gather info from all posts
                for post_serial in serializer.data:
                    postDict = dict(post_serial)
                    postDict["type"] = "post"
                    postDict["url"] = postDict["id"]
                    serialzer = AuthorSerializer(author)
                    authorDict = dict(serialzer.data)
                    authorDict["type"] = "author"
                    authorDict["url"] = authorDict["id"]
                    postDict["author"] = authorDict
                    postDict["count"] = len(Comment.objects.filter(parentPost=post_serial["id"]))
                    postDict["comments"] = postDict["id"] + "/comments/"
                    postList.append(postDict)

            # 3b. get comment object
            commentList=[]
            # get the actual comments (learned from APIListComments)
            comments = Comment.objects.filter(parentPost=postDict["id"])
            serializer = CommentSerializer(comments, many=True)
            commentList = []
            for comment_serial in serializer.data:
                commentDict = dict(comment_serial)
                commentAuthor = Author.objects.get(pk=comment_serial["author"])
                author_serialzer = AuthorSerializer(commentAuthor)
                authorDict = dict(author_serialzer.data)
                authorDict["type"] = "author"
                authorDict["url"] = authorDict["id"]
                commentDict["author"] = authorDict
                commentDict["type"] = "comment"
                commentList.append(commentDict)


            # 3c. get like object
            # get the likes for the post
            likes = Like.objects.filter(parentPost=postDict["id"])
            likeList = []
            serializer = LikeSerializer(likes, many=True)
            for like_serial in serializer.data:
                likeDict = dict(like_serial)
                likeAuthor = Author.objects.get(pk=like_serial["author"])
                author_serialzer = AuthorSerializer(likeAuthor)
                authorDict = dict(author_serialzer.data)
                authorDict["type"] = "author"
                authorDict["url"] = authorDict["id"]
                likeDict["author"] = authorDict
                likeDict["object"] = HOST + "authors/" + author_id + "/posts/" + post_id
                likeList.append(likeDict)

            # 3d. adding the follower request object
            # get the id for every follower
            user_followers = author.followers.all()
            followersList = []
            for user_follower in user_followers:
                followersList.append(user_follower.user_id)

            followRequestList=[]
            # For each follower (each id), get the follower request
            for each in followersList:
                localAuthor=Author.objects.get(pk=each)
                author_serialzer = AuthorSerializer(localAuthor)
                localAuthorDict=dict(author_serialzer.data)

                # getting all the fields and append them into a list using request
                followRequestDict=dict(request.data)
                followRequestDict["type"]="Follow"
                followRequestDict["sunmmary"]=request.data["summary"]
                followRequestDict["actor"]=request.data["actor"]
                # first get the authors, then get the actors
                followRequestDict["author"]=localAuthorDict
                followRequestList.append(followRequestDict)

            # 3e. setting the items to be the postlist
            itemList=postList+commentList+likeList+followRequestList

            # Finalizing up
            inboxDict["items"]=itemList
            return Response(status=200, data=inboxDict)
        except:
            return Response(status=404)
    
    # send respective object in body
    def post(request, author_id):
        # get the author object first
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # if type is post, add that post (referred from post from APIPost)
        # getting the post_id through the 
        if request.data["type"]=="post":
            # get the post_id
            post_id=request.data["id"].split("/")[-1]
            # gettting the post object
            try:
                post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            except Post.DoesNotExist:
                return Response(status=404)
            # Check if request is from an authorized source (only user and admin can call this!), 401 if not
            if not request.user.is_authenticated and request.user.id != author_id:
                return Response(status=401)
            postDict = dict(request.data)
            postDict["author"] = HOST+"authors/"+author_id
            serializer = InboxSerializer(data=postDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_post_object(serializer.data, author))
            return Response(status=400, data=serializer.errors)
            
            
        # if the type is “follow” then add that follow is added to AUTHOR_ID’s inbox to approve later
        elif request.data["type"]=="follow":
            followDict=dict(request.data)
            followDict["author"]=HOST+"authors/"+author_id
            # get the summary and actor
            # summary=followDict["summary"]
            # actor=followDict["actor"]["id"]
            actor=followDict["actor"]
            serializer=InboxSerializer(data=followDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_follow_request_object(serializer.data, author, actor))
            return Response(status=400, data=serializer.error)

        # if the type is “like” then add that like to AUTHOR_ID’s inbox
        elif request.data["type"]=="like":
            # (refer from post from APIListLikesPost)
            # use the request.object to get the post_id
            post_id=request.data["object"].split("/")[-1]
            # Try to get the Post object
            try:
                post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            except Post.DoesNotExist:
                return Response(status=404)
            # Try to get the like
            try:
                likes = Like.objects.filter(parentPost=post)
            except Like.DoesNotExist:
                return Response(status=404)

            likeDict=dict(serializer.data)
            likeDict["author"] = HOST+"authors/"+author_id
            serializer = InboxSerializer(data=likeDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_like_object(serializer.data, post, author))
            return Response(status=400, data=serializer.errors)

        # if the type is “comment” then add that comment to AUTHOR_ID’s inbox    
        elif request.data["type"]=="comment":
            # get the required info from the comment object with endpoint( ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments)
            post_id=request.data["id"].split("/")[-3]
            comment_id=request.data["id"].split("/")[-1]
            # check whether the post exist
            try:
                post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            except Post.DoesNotExist:
                return Response(status=404)
            # getting the comment object itself, then send commentDict later on
            try:
                comment=Comment.objects.get(id=HOST+"authors/"+author_id+"/posts/"+post_id+"/comments/"+comment_id)
            except Comment.DoesNotExist:
                return Response(status=404)

            # referred from post from APIListComments
            CommentDict=dict(request.data)
            CommentDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id+"/comments/"+comment_id
            CommentDict["parentPost"] = HOST+"authors/"+author_id+"/posts/"+post_id
            # check if author is saved in our DB (remote or local)
            try:
                commentAuthor = Author.objects.get(pk=newCommentDict["author"]["id"])
            except Author.DoesNotExist:
                # check if author is a remote author not yet saved
                if newCommentDict["author"]["host"] == HOST:
                    return Response(status=404)
                # save new remote author into DB
                commentAuthorSerializer = AuthorSerializer(data=newCommentDict["author"])
                if not commentAuthorSerializer.is_vaild():
                    return Response(status=400, data=commentAuthorSerializer.errors)
                commentAuthorSerializer.save()
            CommentDict["author"] = newCommentDict["author"]["id"]
            serializer=InboxSerializer(data=commentDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201, data=api_helper.construct_comment_object(serializer.data, Author.objects.get(id=newCommentDict["author"])))
            return Response(status=400, data=serializer.errors)
            

        # TBA
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
        inbox["items"]={}
        return Response(status=200)"""

        

# TODO Please generate appropriate documentation of the following API to root_project/openapi.json
class APIPosts(APIView):
    def get(self, request):
        author_posts_pair = []
        for each_author in Author.objects.all():
            if not Post.objects.filter(author=each_author).count():
                continue
            posts = PostSerializer(Post.objects.filter(author=each_author).filter(visibility="VISIBLE").filter(unlisted=False), many=True)
            author_posts_pair.append([each_author, posts.data])
            print("num_post for "+dict(AuthorSerializer(each_author).data)["id"]+": "+str(len(posts.data)))
            
        return Response(status=200, data=api_helper.construct_list_of_all_posts(author_posts_pair))