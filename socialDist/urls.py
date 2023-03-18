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

from django.urls import path, re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Social Dist API",
      default_version='v1',
      description="API for Social Dist",
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

app_name = 'socialDist'
urlpatterns = [
     # Commented just for testing
     # path('docs/', schema_view),
     path('authors/', 
          views.APIListAuthors.as_view(),name='authors'),
     path('authors/<str:id>/', 
          views.APIAuthor.as_view(), name='author'),
     # TODO Fix required on APIInbox
     # path('authors/<str:author_id>/inbox/',
     #      views.APIInbox.as_view()),
     path('authors/<str:author_id>/liked/',
          views.APILiked.as_view()),
     path('authors/<str:author_id>/followers/',
          views.APIFollowers.as_view()),
     path('authors/<str:author_id>/followers/<path:foreign_author_id>/',
          views.APIFollower.as_view()),
     path('authors/<str:author_id>/posts/<str:post_id>/', 
          views.APIPost.as_view(), name='post'),
     path('authors/<str:author_id>/posts/<str:post_id>/image/', 
          views.APIImage.as_view(), name='image'),
     path('authors/<str:author_id>/posts/',
          views.APIListPosts.as_view(), name='posts'),
     path('authors/<str:author_id>/posts/<str:post_id>/comments/', 
          views.APIListComments.as_view()),
     path('authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/', 
          views.APIComment.as_view(), name='comment'),
     path('authors/<str:author_id>/posts/<str:post_id>/likes/', 
          views.APIListLikesPost.as_view()),
     path('authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes', 
          views.APIListLikesComments.as_view()),
     path('posts/',
          views.APIPosts.as_view()),
     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
     re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
