"""CMPUT404Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# MIT License

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

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView, RedirectView
from .views import settings, home, postPage, authorPage, privatePosts, create_post, editPost, search, localComment, foreignComment

urlpatterns = [
    
    ######################################################### 
    # Do not add any path above this
    # else redirection functionality won't work as intended
    path("search/", search,  name="search"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("post/", create_post, name="post"),
    path("api/", include("socialDist.urls")),
    #########################################################  
    path("", home, name="home"),  
    path("admin/", admin.site.urls),
    path("accounts/settings", settings, name="settings"),
    path("accounts/signup", TemplateView.as_view(template_name="registration/signup.html"), name="signup"),
    path("accounts/stream", privatePosts, name="stream"),
    path("authors/<str:author_id>/", view=authorPage, name="page_author"),
    path("authors/<str:author_id>/posts/<str:post_id>/", view=postPage, name="page_post"),
    path("authors/<str:author_id>/posts/<str:post_id>/edit/", view=editPost, name="edit_post"),
    path("authors/<str:author_id>/posts/<str:post_id>/comments/",view=localComment, name="local_comment" ),
    path("posts/foreign/<str:hostName>/authors/<str:foreignauthor_id>/posts/<str:post_id>/comments/",view=foreignComment, name="foreign_comment" )
]
# Automatically add redirections
# set number of items to add to itself from the beginning
final_index = 4
urlpatterns += [path(each[:-1], RedirectView.as_view(url=each)) 
    for each in [each_path.pattern._route
        for each_path in urlpatterns[:final_index]
    ]
]