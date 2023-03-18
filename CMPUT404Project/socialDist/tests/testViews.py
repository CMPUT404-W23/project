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
        # self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.user=User.objects.create_user(username='test',email='test@gmail.com', password='password')
        self.client.force_authenticate(user=self.user)
        # client = APIClient(enforce_csrf_checks=True)
        # client.login()


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


    # Basic test: DONE 
    def testGetListAuthors(self):

        # Work by creating objects, but want to create through POST
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id="http://127.0.0.1:8000/authors/2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 

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
        # Successful case, should return 201
        data={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}

        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.assertEqual(201, response.status_code)

        # Failure case: test with existing user (same data) --> give 409
        newdata={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}
        response=self.client.put(url, newdata)

        self.assertEqual(409, response.status_code)
        self.assertEqual(response.content.decode("utf-8"), '"An account with that username already exists."')

class APIAuthorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)
        # client = APIClient(enforce_csrf_checks=True)
        # client.login()

        """
        # Work by creating objects, but want to create through POST
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id="http://127.0.0.1:8000/authors/2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 
        """

    # Get for 1 author
    def testgetAuthor(self):

        # Work by creating objects, but want to create through POST
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id="http://127.0.0.1:8000/authors/2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 


        url = reverse('socialDist:author', args="1")
        # url = reverse('socialDist:author', kwargs={'id':1})
        response = self.client.get(url)
        expectedData={'id': 'http://127.0.0.1:8000/authors/1', 'host': 'http://127.0.0.1:8000/', 'displayName': 'tester1', 'github': 'http://github.com/test1', 'profileImage': 'https://i.imgur.com/test1.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/1'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expectedData)

    # for POST: add a new author
    # Problem: dict exist, serializer is not valid
    def testPostAuthor(self):

        # using PUT author list to create both author and user; WORKED
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)

        # PASSED the author get
        # 2 users
        # print(User.objects.all())
        # 1 author: [<Author: Author object (http://127.0.0.1:8000/authors/2)>], it binds with the user I created earlier in this fucntion
        # print(Author.objects.get(id="http://127.0.0.1:8000/authors/2").user)
        
        # Success case
        url = reverse('socialDist:author', args="2")
        # new data is from the testing user with some udpated fields
        newData={'user_id': None, 'id': 'http://127.0.0.1:8000/authors/3', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg'}
        response=self.client.post(url, newData, id=2, follow=True, format='json')

        expected_data={'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected_data)
        

        # Fail case: author doesn't exist
        url = reverse('socialDist:author', args="5")
        failData={}
        response=self.client.post(url, failData, id="4", follow=True, format='json')
        expected_data={'id': 'http://127.0.0.1:8000/authors/3', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.status_code, 404)

