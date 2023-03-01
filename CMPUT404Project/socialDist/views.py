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
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/
# https://stackoverflow.com/questions/25943850/django-package-to-generate-random-alphanumeric-string

HOST = "http://127.0.0.1:8000/"
# maybe store URL field in database as id?

# when creating author, set id to HOST + authors/ + <some id> and host to HOST
# authors who are local to the server and any author who interacts with the server
# (likes, comments, follow requests) should be hosted on the server
class APIAuthor(APIView):
    def get(self, request, id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+id)
            serialzer = AuthorSerializer(author)
            returnDict = dict(serialzer.data)
            returnDict["type"] = "author"
            returnDict["url"] = returnDict["id"]
            return Response(status=200, data=returnDict)
        except Author.DoesNotExist:
            return Response(status=404)
        
    # when posting, don't send authorID or host
    def post(self, request, id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+id)
        except Author.DoesNotExist:
            return Response(status=404)
        authorDict = dict(request.data)
        authorDict["id"] = HOST+"authors/"+id
        authorDict["host"] = HOST
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            authorDict = dict(serializer.data)
            authorDict["url"] = authorDict["id"]
            authorDict["type"] = "author"
            return Response(status=201, data=authorDict)
        return Response(status=400, data=serializer.errors)
    
class APIListAuthors(APIView):
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
        # query string not provided
        else:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            returnList = []
            for author_serial in serializer.data:
                returnDict = dict(author_serial)
                returnDict["type"] = "author"
                returnDict["url"] = author_serial["id"]
                returnList.append(returnDict)
            authorListDict = {}
            authorListDict["type"] = "authors"
            authorListDict["items"] = returnList
            return Response(status=200, data=authorListDict)

# when creating posts, follow same URL scheme!
class APIPost(APIView):
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            print(HOST+"authors/"+author_id+"posts/"+post_id)
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
            serialzer = PostSerializer(post)
            postDict = dict(serialzer.data)
            postDict["type"] = "post"
            serialzer = AuthorSerializer(author)
            authorDict = dict(serialzer.data)
            authorDict["type"] = "author"
            authorDict["url"] = authorDict["id"]
            postDict["author"] = authorDict
            postDict["count"] = len(Comment.objects.filter(parentPost=HOST+"authors/"+author_id+"/posts/"+post_id))
            postDict["comments"] = postDict["id"] + "/comments/"
            return Response(status=200, data=postDict)
        except Post.DoesNotExist:
            return Response(status=404)
        
    #when POST, don't include author or post id
    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        postDict = dict(request.data)
        postDict["author"] = HOST+"authors/"+author_id
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            postDict = dict(serializer.data)
            postDict["type"] = "post"
            return Response(status=201, data=postDict)
        return Response(status=400, data=serializer.errors)
    
    # when PUT, don't include author or id
    def put(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        
            return Response(status=404)
        except Post.DoesNotExist:
            postDict = dict(request.data)
            postDict["author"] = HOST+"authors/"+author_id
            postDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id
            serializer = PostSerializer(data=postDict, partial=True)
            if serializer.is_valid():
                serializer.save()
                postDict = dict(serializer.data)
                postDict["type"] = "post"
                return Response(status=201, data=serializer.data)
            return Response(status=400, data=serializer.errors)

    def delete(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try:
            post = Post.objects.get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=404)
        post.delete()
        return Response(status=200)

class APIListPosts(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        posts = Post.objects.filter(author=author)
        serializer = PostSerializer(posts, many=True)
        postList = []
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
        postListDict = {}
        postListDict["type"] = "posts"
        postListDict["items"] = postList
        return Response(postListDict)
    
    # when POST, include in body
    #   title - string
    #   source - string
    #   origin - string
    #   description - string
    #   contentType - string
    #   catergories - string
    #   published - datetime
    #   visibitly 
    #   unlisted
    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
                        return Response(status=201, data=serializer.data)
                return Response(status=400, data=serializer.errors)
    
# comment id should be the same URL scheme as posts and authors
class APIComment(APIView):
    def get(self, request, author_id, post_id, comment_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
        commentDict = dict(serialzer.data)
        author_serialzer = AuthorSerializer(author)
        authorDict = dict(author_serialzer.data)
        authorDict["type"] = "author"
        authorDict["url"] = authorDict["id"]
        commentDict["type"] = "comment"
        commentDict["author"] = authorDict
        return Response(commentDict)

class APIListComments(APIView):
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(parentPost=HOST+"authors/"+author_id+"/posts/"+post_id)
        serializer = CommentSerializer(comments, many=True)
        commentList = []
        for comment_serial in serializer.data:
            commentDict = dict(comment_serial)
            author_serialzer = AuthorSerializer(author)
            authorDict = dict(author_serialzer.data)
            authorDict["type"] = "author"
            authorDict["url"] = authorDict["id"]
            commentDict["author"] = authorDict
            commentDict["type"] = "comment"
            commentList.append(commentDict)
        commentListDict = {}
        commentListDict["type"] = "comments"
        commentListDict["items"] = commentList
        commentListDict["post"] = HOST + "authors/" + author_id + "/posts/" + post_id 
        commentListDict["id"] = HOST + "authors/" + author_id + "/posts/" + post_id + "/comments/"
        return Response(commentListDict)
    
    # when POST, include in body
    #   author - URL form
    #   content - string
    #   contentType - string
    #   published - datetime
    def post(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
            except:
                newPostDict = dict(request.data)
                newPostDict["id"] = HOST+"authors/"+author_id+"/posts/"+post_id+"/comments/"+comment_id
                newPostDict["parentPost"] = HOST+"authors/"+author_id+"/posts/"+post_id
                serializer = CommentSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(status=201, data=serializer.data)
                return Response(status=400, data=serializer.errors)

# likes, store with same URL schemea
class APIListLikesPost(APIView):
    def get(self, request, author_id, post_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.filter(author=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(parentPost=post_id)
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
        likeListDict = {}
        likeListDict["type"] = "likes"
        likeListDict["items"] = likeList
        return Response(likeListDict)

class APIListLikesComments(APIView):
    def get(self, request, author_id, post_id, comment_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.filter(posterID=author).get(pk=HOST+"authors/"+author_id+"/posts/"+post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try: 
            comment = Comment.objects.filter(parentPost=post_id).get(pk=HOST+"authors/"+
                                                                       author_id+"/posts/"+
                                                                       post_id+"/comments/"+
                                                                       comment_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(parentComment=comment)
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
            likeDict["object"] = HOST + "authors/" + author_id + "/posts/" + post_id + "/comments/" + comment_id
            likeList.append(likeDict)
        likeListDict = {}
        likeListDict["type"] = "likes"
        likeListDict["items"] = likeList
        return Response(likeListDict)
    
class APILiked(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(author=HOST+"authors/"+author_id)
        likeList = []
        serializer = LikeSerializer(likes, many=True)
        for like_serial in serializer.data:
            likeDict = dict(like_serial)
            like = Like.objects.get(pk=like_serial["likeID"])        
            author_serialzer = AuthorSerializer(author)
            authorDict = dict(author_serialzer.data)
            authorDict["type"] = "author" 
            authorDict["url"] = authorDict["id"]
            likeDict["author"] = authorDict
            if like.likeType == "Post":
                likeDict["object"] = like.parentPost.id
            else: 
                likeDict["object"] = like.parentComment.id
            likeList.append(likeDict)
        likeListDict = {}
        likeListDict["type"] = "liked"
        likeListDict["items"] = likeList
        return Response(likeListDict)
        
class APIFollowers(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_followers = author.followers.all()
        followersList = []
        for user_follower in user_followers:
            followersList.append(user_follower.user_id)
        serializer = AuthorSerializer(followersList, many=True)
        authorList = []
        for author_serial in serializer.data:
            authorDict = dict(author_serial)
            authorDict["type"] = "author" 
            authorDict["url"] = authorDict["id"]
            authorList.append(authorDict)
        followerListDict = {}
        followerListDict["type"] = "followers"
        followerListDict["items"] = authorList
        return Response(followerListDict)

# foreign_author_id should be an abs URL, encoded as a parameter or path element
class APIFollower(APIView):
    def get(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            #TODO: convert foreign_author_id from parameter form to URL
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
            return Response(status=404)
        #TODO: need to fix
        try:
            follower = targetAuthor.followers.all().get(user_id=followingAuthor.authorId)
            return Response(status=200)
        except:
            return Response(status=404)
        
    # foreign_author_id should be an abs URL, encoded as a parameter or path element
    # same notes as before!
    def put(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=HOST+"authors/"+author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
            # create copy of author on our server
            new_author = Author(id=foreign_author_id)
        if followingAuthor in targetAuthor.followers.all():
            return Response(status=405)
        # link two authors together with relationship
        targetAuthor.followers.add(followingAuthor)
        targetAuthor.save()
        return Response(status=200)

    def delete(self, request, author_id, foreign_author_id):
        try:
            targetAuthor = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=404)
        try: 
            followingAuthor = Author.objects.get(pk=foreign_author_id)
        except:
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
