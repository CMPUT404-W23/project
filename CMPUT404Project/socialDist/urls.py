from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'posts', views.PostViewSet)

app_name = 'socialDist'
urlpatterns = router.urls