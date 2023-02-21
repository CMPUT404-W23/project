from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'socialDist'
# router = DefaultRouter()
# router.register(r'authors', views.AuthorViewSet, basename='author')
urlpatterns = [path('authors/', views.get_authors, name='get_authors'),
               path('authors/<int:id>/', views.get_author, name="get_author"),
               path('authors/<int:author_id>/posts/<str:post_id>/', views.get_post, name="get_post"),
               path('authors/<int:author_id>/posts/<str:post_id>/', views.edit_post, name="edit_post"),
               path('authors/<int:author_id>/posts/',views.get_posts, name="get_posts"),
               path('authors/<int:author_id>/posts/<str:post_id>/comments/', views.get_comments, name="get_comments"),
            path('authors/<int:author_id>/posts/<str:post_id>/comments/<str:comment_id>/', views.get_comment, name="get_comment")]