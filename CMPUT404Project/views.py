from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from socialDist.models import Author, Post
import base64

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
        return HttpResponse(status=404, content="Author does not exist!")
    try:
        post = Post.objects.filter(visibility="VISIBLE").get(id=HOST+"authors/"+author_id+"/posts/"+post_id)
        if post.contentType == "image/png;base64" or post.contentType == "image/jpeg;base64":
            content_bytes_base64 = post.content.encode('ascii')
            return HttpResponse(status=200, 
                            content=base64.b64decode(content_bytes_base64), 
                            content_type=post.contentType)
        else:
            context = {'post': post}
            #TODO: modify post_page.html to support image embedding
            return render(request, 'post_page.html', context)
    except Post.DoesNotExist:
        return HttpResponse(status=404, content="Public post does not exist!")

# URL to author profile page, will contain inbox if owner
def authorPage(request, author_id):
    try:
        author =  Author.objects.get(id=HOST+"authors/"+author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404, content="Author does not exist!")
    context = {'author' :author,
               'isOwner': request.user.is_authenticated and request.user}
    # return render()
    #TODO: create a page for the author, if the requester is the author, add inbox here!
    return HttpResponse("Temp Author page for " + author.displayName)
