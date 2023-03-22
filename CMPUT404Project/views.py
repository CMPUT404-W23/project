from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from socialDist.models import Author, Post
import base64

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

HOST = "https://socialdistcmput404.herokuapp.com/"

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
def home(request):
    return render(request, 'home.html')

# URL to public post, even if unlisted, if image, will be actual image!
def postPage(request, author_id, post_id):
    try:
        author =  Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")
    try:
        post = Post.objects.filter(visibility="VISIBLE").get(id=HOST+"authors/"+author_id+"/posts/"+post_id)
        if post.contentType == "image/png;base64" or post.contentType == "image/jpeg;base64" or post.contentType == "image/jpg;base64":
            content_bytes_base64 = post.content.encode('ascii')
            return HttpResponse(status=200, 
                            content=base64.b64decode(content_bytes_base64), 
                            content_type=post.contentType)
        else:
            context = {'post': post}
            return render(request, 'post_page.html', context)
    except Post.DoesNotExist:
        return HttpResponse(status=404, content="Post does not exist")

# URL to author profile page, will contain inbox if owner
def authorPage(request, author_id):
    try:
        author =  Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Author does not exist!")
    context = {'author' :author,
               'isOwner': request.user.is_authenticated and (request.user.is_staff or request.user.author == author)}
    #TODO: create a page for the author, if the requester is the author, add inbox here!
    return render(request, 'profile.html', context)

@login_required
def create_post(request):
    return render(request, 'post.html')
