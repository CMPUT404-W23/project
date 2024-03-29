from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from socialDist.models import Author, Post, Connection
from socialDist.serializers import ConnectionSerializer, AuthorSerializer
from socialDist.api_helper import is_follower
import json


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

# File contains views representing different pages of our web app

HOST = "https://socialdistcmput404.herokuapp.com/"

# Source: 
# StackOverflow 
# Author: xyres
# Author URL: https://stackoverflow.com/users/1925257/xyres
# Title: How to use the context variables passed from Django in javascript?
# Date: Apr 9, 2017  
# URL: https://stackoverflow.com/questions/43305020/how-to-use-the-context-variables-passed-from-django-in-javascript

# Home page
@login_required
def home(request):
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    try:
        current_author = Author.objects.get(user=request.user)
        current_author_serial = AuthorSerializer(current_author)
        context = {'connections': json.dumps(connections_serial.data),
               'current_author': json.dumps(dict(current_author_serial.data))}
    except:
        context = {'connections': json.dumps(connections_serial.data),
                   'current_author': json.dumps({})}
    return render(request, 'home.html', context)

# Settings page
@login_required
def settings(request):
    # Get Author instance for the current user
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        author = None
    context = {'author': author}
    return render(request, 'settings.html', context)

# Search page
@login_required
def search(request):
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    author = Author.objects.get(user=request.user)
    author_serial = AuthorSerializer(author)
    context = {'connections': json.dumps(connections_serial.data),
               'author': json.dumps(author_serial.data)}
    return render(request, 'search.html', context)

# Public post page, even if unlisted
def postPage(request, author_id, post_id):
    try:
        author =  Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")
    try:
        current_author = Author.objects.get(user=request.user)
        current_author_serial = AuthorSerializer(current_author)
        current_author_context = json.dumps(dict(current_author_serial.data))
    except:
        current_author_context = json.dumps({})
    try:
        post = Post.objects.filter(visibility="VISIBLE").get(id=HOST+"authors/"+author_id+"/posts/"+post_id)
    except Post.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    context = {
        'connections': json.dumps(connections_serial.data),
        'post': post,
        'current_author': current_author_context,
    }
    return render(request, 'post_page.html', context)

# Author profile page, will contain inbox if owner
def authorPage(request, author_id):
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    try:
        author =  Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Author does not exist!")
    try:
        current_author = Author.objects.get(user=request.user)
        current_author_serial = AuthorSerializer(current_author)
        current_author_context = json.dumps(dict(current_author_serial.data))
    except:
        current_author_context = json.dumps({})
    user_followers = author.followers.all()
    follower_list = []
    for follower in user_followers:
        follower_list.append(follower)
    user_following = author.following.all()
    following_list = []
    for following in user_following:
        following_list.append(following)
    context = {
        'author' :author,
        'isOwner': request.user.is_authenticated and (request.user.is_staff or request.user.author == author),
        'follower_list':follower_list,
        'following_list':following_list,
        'current_author': current_author_context,
        'connections': json.dumps(connections_serial.data),
    }
    return render(request, 'profile.html', context)

# Author's stream
@login_required
def privatePosts(request):
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        author = None
    context = {'author': author}
    return render(request, 'stream.html', context)

# Edit post page
@login_required
def editPost(request, author_id, post_id):
    try:
        author =  Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")
    if (not (request.user.is_staff or request.user.author == author)):
        return HttpResponse(status=401)
    try:
        post = Post.objects.filter(visibility="VISIBLE").get(id=HOST+"authors/"+author_id+"/posts/"+post_id)
        context = {'post': post,
                    'isImage': post.contentType == "image/png;base64" 
                       or post.contentType == "image/jpeg;base64" 
                       or post.contentType == "image/jpg;base64"}
        return render(request, 'edit_post.html', context)

    except Post.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")

# Create post 
@login_required
def create_post(request):
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    author = Author.objects.get(user=request.user)
    author_serial = AuthorSerializer(author)
    context = {'connections': json.dumps(connections_serial.data),
               'author': json.dumps(dict(author_serial.data))}
    return render(request, 'post.html', context)

# Local comment posting page
@login_required
def localComment(request, author_id, post_id):
    current_author = Author.objects.get(user=request.user)
    current_author_serial = AuthorSerializer(current_author)
    try:
        author = Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")
    try:
        post = Post.objects.get(id=HOST+"authors/"+author_id+"/posts/"+post_id)
        if post.visibility == "FRIENDS" and not is_follower(request.user, author):
            return HttpResponse(status=404, content="Post does not exist")
        context = {'post': post, 'author':json.dumps(current_author_serial.data)}
        return render(request, 'post_comment.html', context)
    except Post.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")

# Remote comment posting page  
@login_required
def foreignComment(request, hostName, post_id, foreignauthor_id):
    author = Author.objects.get(user=request.user)
    author_serial = AuthorSerializer(author)
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    context = {'hostName':hostName, 'post_id':post_id, 'author':json.dumps(author_serial.data), 'foreignauthor_id': foreignauthor_id, 'connections': json.dumps(connections_serial.data)}
    return render(request, 'post_comment.html',context)