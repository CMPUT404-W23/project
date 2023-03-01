from django.urls import path
from . import views

app_name = 'socialDist'
# router = DefaultRouter()
# router.register(r'authors', views.AuthorViewSet, basename='author')
urlpatterns = [path('authors/', 
                    views.APIListAuthors.as_view()),
               path('authors/<str:id>/', 
                    views.APIAuthor.as_view()),
               path('authors/<str:author_id>/inbox/',
                 views.APIInbox.as_view()),
               path('authors/<str:author_id>/liked/',
                    views.APILiked.as_view()),
               path('authors/<str:author_id>/followers/',
                    views.APIFollowers.as_view()),
               path('authors/<str:author_id>/followers/<path:foreign_author_id>/',
                    views.APIFollower.as_view()),
               path('authors/<str:author_id>/posts/<str:post_id>/', 
                    views.APIPost.as_view()),
               path('authors/<str:author_id>/posts/',
                    views.APIListPosts.as_view()),
               path('authors/<str:author_id>/posts/<str:post_id>/comments/', 
                    views.APIListComments.as_view()),
            path('authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/', 
                 views.APIComment.as_view()),
            path('authors/<str:author_id>/posts/<str:post_id>/likes/', 
                 views.APIListLikesPost.as_view()),
            path('authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes', 
                views.APIListLikesComments.as_view()),]
