from django.contrib import admin
from .models import Author, Comment, Like, Post, Server, Inbox, FollowRequest, UserFollowing
# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)

# test the new added models in the admin site
admin.site.register(Server)
admin.site.register(Inbox)

admin.site.register(FollowRequest)
admin.site.register(UserFollowing)
