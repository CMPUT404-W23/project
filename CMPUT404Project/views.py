from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from socialDist.models import Author

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

@login_required
def create_post(request):
    return render(request, 'post.html')
