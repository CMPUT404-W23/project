# MIT License

# Copyright (c) 2023 CMPUT404-W23

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
# https://testdriven.io/blog/drf-views-part-1/
# https://docs.djangoproject.com/en/4.1/topics/db/queries/#:~:text=Creating%20objects&text=To%20create%20an%20object%2C%20instantiate,save%20it%20to%20the%20database.&text=This%20performs%20an%20INSERT%20SQL,method%20has%20no%20return%20value.
# https://docs.djangoproject.com/en/4.1/ref/request-response/
# https://www.geeksforgeeks.org/adding-permission-in-api-django-rest-framework/
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/
# https://stackoverflow.com/questions/25943850/django-package-to-generate-random-alphanumeric-strin
# https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import QueryDict
from rest_framework import status
from django.utils.crypto import get_random_string
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
import urllib.parse

from .models import Author, Post, Comment, Like, Server, Inbox, UserFollowing
from . import api_helper 

HOST = "http://127.0.0.1:8000/"

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

# API View for list of authors API queries (endpoint /api/authors/<author_id>/posts/)
class APIListAuthors(APIView):
    # Getting list of authors
    def get(self, request):
        # TODO: adjust the query by page and size numbers
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
        # query string not provided, return full list of authors
        else:
            authors = Author.objects.filter(host=HOST)
            serializer = AuthorSerializer(authors, many=True)
            return Response(status=200, data=api_helper.construct_list_of_authors(serializer.data))

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
    def post(self, request, author_id, post_id):
        # Check if specified author exists
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if specfied post exists
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
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
    def delete(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        if not request.user.is_authenticated and request.user.id != author_id:
            return Response(status=401)
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        post.delete()
        return Response(status=200)
    
# API View for a list of post queries (endpoint /api/authors/<author_id>/posts/)
class APIListPosts(APIView):
    # Get a list of posts
    #TODO: paginated this!
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        posts = Post.objects.filter(author=author).filter(visibility="VISIBLE")
        serializer = PostSerializer(posts, many=True)
        return Response(status=200, data=api_helper.construct_list_of_posts(serializer.data, author))
    
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
            
# WIP: DO NOT USE!
class APIImage(APIView):
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        # Check if resource already exists, if it does, acts like POST!
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            if post.contentType != "image/png" and post.contentType != "image/jpeg":
                return Response(status=404)
            # print(post.content.encode('ascii'))
            return HttpResponse(status=200, 
                            content=post.content.encode('ascii'), 
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
    #TODO: paginate this!
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        comments = Comment.objects.filter(parentPost=HOST+"authors/"+author_id+"/posts/"+post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(status=200, data=api_helper.construct_list_of_comments(serializer.data, author, post))
    
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
    # Get list of likes originating from this author
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

class APIInbox(APIView):
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
            # 3. getting all of the posts in the server (learned from APIListPosts)

            # 3a filter the posts to ensure they are all followers
            # 3a.1 Get id for every follower (learned from APIFollowers)
            user_followers = author.followers.all()
            followersList = []
            for user_follower in user_followers:
                followersList.append(user_follower.user_id)

            # 3b use those id's to get their posts (learned from APIListPosts)
            postList = []
            # 3b1.For each follower (each id), get all posts
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
            # 3c. setting the items to be the postlist
            inboxDict["items"]=postList
            return Response(status=200, data=inboxDict)
        except:
            return Response(status=404)
    
    # send respective object in body
    def post(request, author_id):
        return Response(status=404)

    
"""
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
"""