import json, datetime
from django.utils.timezone import make_aware
from rest_framework import status
from socialDist.serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from socialDist.models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User

# BACK-END tests for views

class APIAuthorTests(TestCase):
    # Setup client, a dummy broswer used for testing
    def setUp(self):
        self.client=Client()
        # Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        # Author.objects.create(id="http://127.0.0.1:8000/authors/test2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 
  
    # Basic test (TBA)
    def testGetListAuthors(self):
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # test basic API fields
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "type")
        self.assertContains(response, "items")

    def testget1Author(self):
        data={
            "id": "http://127.0.0.1:8000/authors/1",
            "host": "http://127.0.0.1:8000/",
            "displayName": "jasonKNEWaaaa",
            "github": "aaaaakkkkkkkkkk",
            "profileImage": "new",
            "type": "author",
            "url": "http://127.0.0.1:8000/authors/1"
        }
        url = reverse('socialDist:author', args="1")
        self.client.post(url, data, follow=True)  

        url = reverse('socialDist:author', args="1")
        response = self.client.get(url)

        # test basic API fields (TBA)
        self.assertEqual(response.status_code, 404)
        

