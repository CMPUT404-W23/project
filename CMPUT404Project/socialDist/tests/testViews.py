import json, datetime
from django.utils.timezone import make_aware
from rest_framework import status
from socialDist.serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from socialDist.models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User

from rest_framework.test import APIClient, force_authenticate
# Reference (TBA): https://www.django-rest-framework.org/api-guide/testing/ 

# BACK-END tests for views
# TO RUN THIS TEST: Command "python manage.py test socialDist.tests.testViews"
#  python manage.py runserver

# Test case for the API views APIListAuthors
class APIListAuthorTests(TestCase):
    # Setup client, a dummy broswer used for testing
    def setUp(self):
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)
        # client = APIClient(enforce_csrf_checks=True)
        # client.login()

        # Work by creating objects, but want to create through POST
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id="http://127.0.0.1:8000/authors/2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 


        """
        # The API way
        data={
        "id": "http://127.0.0.1:8000/authors/1",
        "host": "http://127.0.0.1:8000/",
        "displayName": "jasonKNEWaaaa",
        "github": "aaaaakkkkkkkkkk",
        "profileImage": "new",
        "type": "author",
        "url": "http://127.0.0.1:8000/authors/1"
        }

        # Testing on POSTing (TBA)
        # url = reverse('socialDist:author', args="1")
        response=self.client.post('authors/1/',data, follow=True)
        # printing a 404, why?
        print(response.status_code)
        """
        # Author.objects.get(id="http://127.0.0.1:8000/authors/1")


    # Basic test 
    def testGetListAuthors(self):
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # test basic API fields
        self.assertEqual(response.status_code, 200)

        expectedData={'type': 'authors', 'items': [{'id': 'http://127.0.0.1:8000/authors/1', 'host': 'http://127.0.0.1:8000/', 'displayName': 'tester1', 'github': 'http://github.com/test1', 'profileImage': 'https://i.imgur.com/test1.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/1'}, {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'tester2', 'github': 'http://github.com/test2', 'profileImage': 'https://i.imgur.com/test2.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}]}
        self.assertContains(response, "type")
        self.assertContains(response, "items")
        self.assertEqual(response.data, expectedData)

    # test by replacing the second author with a third author: intend to give 409
    def testPutListAuthors(self):
        # self.client=Client()
        # self.client = APIClient()

        # test PUTing existing user: give 409
        self.newUser=User.objects.create_user('test2','test2@gmail.com', 'password2')
        self.client.force_authenticate(user=self.newUser)

        data={"username": 'test2', "email": "", "password1": "password2"}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.assertEqual(409, response.status_code)
        self.assertEqual(response.content.decode("utf-8"), '"An account with that username already exists."')

        """
        # Success test (TBA)
        # test new user
        # self.newUser=User.objects.create_user('newTest','', 'newPassword')
        # self.client.force_authenticate(user=self.newUser)
        # newData={'username': 'sike', 'email': "", 'password1': "newPassword"}
        # url=reverse('socialDist:authors')
        # response=self.client.put(url, data=json.dumps(newData), content_type='application/json')
        # print(response.status_code)
        # print(response.content)
        """

    # Get for 1 author
    def testget1Author(self):

        # data={
        #     "id": "http://127.0.0.1:8000/authors/1",
        #     "host": "http://127.0.0.1:8000/",
        #     "displayName": "jasonKNEWaaaa",
        #     "github": "aaaaakkkkkkkkkk",
        #     "profileImage": "new",
        #     "type": "author",
        #     "url": "http://127.0.0.1:8000/authors/1"
        # }
        # url = reverse('socialDist:author', args="1")
        # self.client.post(url, data, follow=True)  

        url = reverse('socialDist:author', args="1")
        # url = reverse('socialDist:author', kwargs={'id':1})
        response = self.client.get(url)
        expectedData={'id': 'http://127.0.0.1:8000/authors/1', 'host': 'http://127.0.0.1:8000/', 'displayName': 'tester1', 'github': 'http://github.com/test1', 'profileImage': 'https://i.imgur.com/test1.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/1'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expectedData)

# class APIAuthorTests(TestCase):


        




        
        

