from django.contrib import admin
from .models import Author, Comment, Like, Post, Server, Inbox
# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)

# test the new added models in the admin site
admin.site.register(Server)
admin.site.register(Inbox)
