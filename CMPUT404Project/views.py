from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from socialDist.models import Author, Post, Connection
from socialDist.serializers import ConnectionSerializer, AuthorSerializer
import base64
import json
import marko

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

# Markdown parser: https://marko-py.readthedocs.io/en/latest/

HOST = "https://socialdistcmput404.herokuapp.com/"

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

@login_required
def settings(request):
    # Get Author instance for the current user
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        author = None
    context = {'author': author}
    return render(request, 'settings.html', context)

@login_required
def search(request):
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    author = Author.objects.get(user=request.user)
    author_serial = AuthorSerializer(author)
    context = {'connections': json.dumps(connections_serial.data),
               'author': json.dumps(author_serial.data)}
    return render(request, 'search.html', context)

# URL to public post, even if unlisted, if image, will be actual image!
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
    context = {
        'post': post,
        'current_author': current_author_context,
    }
    return render(request, 'post_page.html', context)

# URL to author profile page, will contain inbox if owner
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
    
@login_required
def create_post(request):
    connections = Connection.objects.all()
    connections_serial = ConnectionSerializer(connections, many=True) 
    author = Author.objects.get(user=request.user)
    author_serial = AuthorSerializer(author)
    context = {'connections': json.dumps(connections_serial.data),
               'author': json.dumps(dict(author_serial.data))}
    return render(request, 'post.html', context)

@login_required
def postComment(request, author_id, post_id):
    author = Author.objects.get(user=request.user)
    author_serial = AuthorSerializer(author)
    try:
        post = Post.objects.filter(visibility="VISIBLE").get(id=HOST+"authors/"+author_id+"/posts/"+post_id)
        # author =  Author.objects.get(id=HOST+"authors/"+author_id)
        context = {'post': post, 'author':json.dumps(author_serial.data)}
        return render(request, 'post_comment.html', context)
    except Post.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")