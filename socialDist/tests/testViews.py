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



# TODO: handle permission_classes
# TODO: APIListComments, APIListLikesPost, APIListLikesComments(APIView), APILiked, APIFollowers, APIFollower, 


import json, datetime
from django.utils.timezone import make_aware
from rest_framework import status
from socialDist.serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from socialDist.models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework.test import APIClient, force_authenticate
# Reference (TBA): https://www.django-rest-framework.org/api-guide/testing/
import base64
import io
from rest_framework.authtoken.models import Token

# pycurl (not working)
# import pycurl
# from io import BytesIO 

# django-test-curl
from django_test_curl import CurlClient

# BACK-END tests for views
# TO RUN THIS TEST: Command "python manage.py test socialDist.tests.testViews"
#  python manage.py runserver

# HOST="http://127.0.0.1:8000/"
HOST="https://socialdistcmput404.herokuapp.com/"
# https://socialdistcmput404.herokuapp.com/api/authors/

# Test case for the API views APIListAuthors
class APIListAuthorTests(TestCase):
    # Setup client, a dummy broswer used for testing
    def setUp(self):
        

        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        # self.HEADERS={"Authorization": "Token 516e5c3d636f46228edb8f09b9613d5b4b166816"}
        # self.user=User.objects.create_user('test','test@gmail.com', 'password')
        # self.user=User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        # self.user=User.objects.create_user(username='test',email='test@gmail.com', password='password')

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        User.objects.create_superuser(username='test1',email='test1@gmail.com', password='password1')
        self.user2=User.objects.get(username='test1')

        # self.client.force_login(self.user)

        # token=Token.objects.get_or_create(user__username='test')
        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})

        self.client.force_authenticate(user=self.user)

        # self.client.credentials(HTTP_AUTHORIZATION="Token "+token.key)
        # self.client.credentials(HTTP_AUTHORIZATION= "Token 516e5c3d636f46228edb8f09b9613d5b4b166816")

        # self.testAuthor=Author.objects.create(user=self.user, id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")

        # self.data={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}
        # url=reverse('socialDist:authors')
        # self.response=self.client.put(url, self.data)
    
    def testPUTListAuthorsSuccess(self):
        """
        Test PUT method for API with endpoint: /api/authors/
        PUT an author that hasn't been created
        """

        data={'username': 'newTestUsername', "email": 'newTest1@gmail.com', "password1": 'newTestPassword1'}
        url=reverse('socialDist:authors')
        # PUT the author
        response=self.client.put(url, data)
        # test status code
        self.assertEqual(201, response.status_code)

    def testPUTListAuthorsFail(self):
        """
        Test PUT method for API with endpoint: /api/authors/
        PUT an author that has created before in setUp
        """
        # Send the PUT request
        data={'username': 'test1', "email": 'test1@gmail.com', "password1": 'password1'}
        url=reverse('socialDist:authors')
        # PUT the author
        response=self.client.put(url, data)
        self.assertEqual(409, response.status_code)
        self.assertEqual(response.content.decode("utf-8"), '"An account with that username already exists."')

    # Basic test: DONE? 
    def testGETListAuthorsSuccess(self):
        """
        Test GET method for API with endpoint: /api/authors/
        Added 2 authors, expect to return 2 authors
        """

        # Add 2 authors using PUT
        url=reverse('socialDist:authors')

        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)

        # send GET request
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # check status code
        self.assertEqual(response.status_code, 200)

        # test data fields
        self.assertEqual(response.data['type'], 'authors')
        self.assertEqual(response.data['items'][0]['host'], HOST)
        self.assertEqual(response.data['items'][0]['displayName'],'testUsername1')
        self.assertEqual(response.data['items'][0]['type'],'author')
        # Find the authorUUID to test id and url
        authorUUID=response.data['items'][0]['id'].split("/")[-1]
        # index=response.data['items'][0]['id'].rfind("/")
        self.assertEqual(response.data['items'][0]['id'],HOST+"authors/"+authorUUID)
        self.assertEqual(response.data['items'][0]['url'],HOST+"authors/"+authorUUID)


        self.assertEqual(response.data['items'][1]['host'], HOST)
        self.assertEqual(response.data['items'][1]['displayName'],'testUsername2')
        self.assertEqual(response.data['items'][1]['type'],'author')
        # Find the index of the last slash to test id and url
        authorUUID=response.data['items'][1]['id'].split("/")[-1]
        # index=response.data['items'][1]['id'].rfind("/")
        self.assertEqual(response.data['items'][1]['id'],HOST+"authors/"+authorUUID)
        self.assertEqual(response.data['items'][1]['url'],HOST+"authors/"+authorUUID)


    def testGETListAuthorsEmpty(self):
        """
        Test GET method for API with endpoint: /api/authors/, but with no authors added
        """
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # check status code
        self.assertEqual(response.status_code, 200)

        # test data fields
        self.assertEqual(response.data['type'], 'authors')
        # check is items in an empty list
        self.assertEqual(response.data['items'], list())


class APIAuthorTests(TestCase):
    def setUp(self):
        """
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)
        # client = APIClient(enforce_csrf_checks=True)
        # client.login()

        # Work by creating objects, but want to create through POST
        # author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        # author2=Author.objects.create(id="http://127.0.0.1:8000/authors/2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 
        """

        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()


        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        # User.objects.create_superuser(username='test1',email='test1@gmail.com', password='password1')
        # self.user2=User.objects.get(username='test1')

    
        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})

        self.client.force_authenticate(user=self.user)

        # PUTing an author
        url=reverse('socialDist:authors')

        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)


    # Get for 1 author
    def testGETAuthorSuccess(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/
        """
        # GET the PUTted author in setUp

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # check status code
        self.assertEqual(response.status_code, 200)
        # get the UUID
        authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # Use the GET from APIAuthors
        newUrl=reverse('socialDist:author', kwargs={"id":authorUUID})
        # test status code
        response = self.client.get(newUrl)
        self.assertEqual(response.status_code, 200)

        # test data
        self.assertEqual(response.data['type'], 'author')
        self.assertEqual(response.data['host'], HOST)
        self.assertEqual(response.data['displayName'],'testUsername1')
        self.assertEqual(response.data['github'], '')
        self.assertEqual(response.data['profileImage'], '')
        # Find the authorUUID to test id and url
        self.assertEqual(response.data['id'],HOST+"authors/"+authorUUID)
        self.assertEqual(response.data['url'],HOST+"authors/"+authorUUID)

    # Find an author doesn't exist
    def testGETAuthorFailure(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/ but with non-existed author
        """
        authorUUID="samepleFailString"
        newUrl=reverse('socialDist:author', kwargs={"id":authorUUID})
        # test status code
        response = self.client.get(newUrl)
        print(response.status_code)
        self.assertEqual(response.status_code, 404)


"""
    # for POST: add a new author
    # Problem: dict exist, serializer is not valid
    def testPOSTAuthorSuccess(self):

        # using PUT author list to create both author and user; WORKED
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        
        # Success case
        url = reverse('socialDist:author', args="2")
        # new data is from the testing user with some udpated fields
        newData={'user_id': None, 'id': 'http://127.0.0.1:8000/authors/3', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg'}
        response=self.client.post(url, newData, id=2, follow=True, format='json')

        expected_data={'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected_data)

    def testPOSTAuthorFailure(self):
        # using PUT author list to create both author and user; WORKED
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)

        # Fail case: author doesn't exist
        # send url with author's id not exist
        url = reverse('socialDist:author', args="3")
        failData={'user_id': None, 'id': 'http://127.0.0.1:8000/authors/3', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg'}
        response=self.client.post(url, failData, id="3", follow=True, format='json')
        expected_data={'id': 'http://127.0.0.1:8000/authors/3', 'host': 'http://127.0.0.1:8000/', 'displayName': 'New test', 'github': 'http://github.com/testnew', 'profileImage': 'https://i.imgur.com/newtest2.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.status_code, 404)
        

class APIPostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)

        # add an User and Author first
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.testAuthor=Author.objects.filter(id="http://127.0.0.1:8000/authors/2").values()

        self.postData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': 'testContent', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }


    # Test creating a post
    def testPUTPostSuccess(self):
        # Create a post first with id=1 using PUT
        # post=Post.objects.create(id="http://127.0.0.1:8000/authors/1", title="testTitle", source="testSource", origin="testOrigin", descritption="testDescription")

        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})

        response=self.client.put(url, self.postData, format='json')

        expectedData={'id': 'http://127.0.0.1:8000/authors/2/posts/1', 'title': 'testTitle', 'source': 'testSource', 'origin': 'testOrigin', 'description': '', 'content': 'testContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/2/posts/1/comments/'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expectedData)


        # Test 2.0: test existed post (also give 201)
        newPostData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'newTestTitle', 
                    'source':"newTestSource", 
                    'origin':"newTestOrigin", 
                    'descritption':"newTestDescription", 
                    'content': 'newTestContent', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        response=self.client.put(url, newPostData, format='json')

        newExpectedData={'id': 'http://127.0.0.1:8000/authors/1', 'title': 'newTestTitle', 'source': 'newTestSource', 'origin': 'newTestOrigin', 'description': '', 'content': 'newTestContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/1/comments/'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, newExpectedData)

    
    # changing the visibility of a post: give 400
    def testPUTPostFail(self):
        # Create a post first with id=1 using PUT
        # post=Post.objects.create(id="http://127.0.0.1:8000/authors/1", title="testTitle", source="testSource", origin="testOrigin", descritption="testDescription")

        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})

        response=self.client.put(url, self.postData, format='json')

        expectedData={'id': 'http://127.0.0.1:8000/authors/2/posts/1', 'title': 'testTitle', 'source': 'testSource', 'origin': 'testOrigin', 'description': '', 'content': 'testContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/2/posts/1/comments/'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expectedData)

        
        # make it to private by putting it again
        newPostData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': 'testContent', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': "Public", 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        response=self.client.put(url, newPostData, format='json')
        self.assertEqual(response.status_code, 400)
    
    # Test creating a post
    def testGETPostSuccess(self):
        # creating a post, then getting it
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})

        response=self.client.put(url, self.postData, format='json')

        expectedData={'id': 'http://127.0.0.1:8000/authors/2/posts/1', 'title': 'testTitle', 'source': 'testSource', 'origin': 'testOrigin', 'description': '', 'content': 'testContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/2/posts/1/comments/'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expectedData)

        # Getting the created post

        testData={}
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.get(url, testData, format='json')
        newExpectedData={'id': 'http://127.0.0.1:8000/authors/2/posts/1', 'title': 'testTitle', 'source': 'testSource', 'origin': 'testOrigin', 'description': '', 'content': 'testContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/2/posts/1/comments/'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, newExpectedData)

    # Getting a post that doesn't exist
    def testGETPostFail(self):
        # data can be empty
        testData={}
        # change post_id to 2 (which post doesn't exist)
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':2})
        response=self.client.get(url, testData, format='json')
        self.assertEqual(response.status_code, 404)

    # POSTing (editing) an existing Post
    def testPOSTPostSuccess(self):
        # Created a post
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, self.postData, format='json')

        # Update the created post
        updatedPostData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'newTestTitle', 
                    'source':"newTestSource", 
                    'origin':"newTestOrigin", 
                    'descritption':"newTestDescription", 
                    'content': 'newTestContent', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        updatedResponse=self.client.post(url, updatedPostData, format='json')
        updatedData={'id': 'http://127.0.0.1:8000/authors/1', 'title': 'newTestTitle', 'source': 'newTestSource', 'origin': 'newTestOrigin', 'description': '', 'content': 'newTestContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/1/comments/'}

        self.assertEqual(updatedResponse.status_code, 201)
        self.assertEqual(updatedResponse.data, updatedData)
        
    # Updating a post without valid fields
    def testPOSTPostFail(self):
        # Created a post
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, self.postData, format='json')

        # Update the created post (with eding fields with invalid values)
        updatedPostData={"id":"http://127.0.0.1:8000/authors/1",'visibility': 'PRIVATE'}

        updatedResponse=self.client.post(url, updatedPostData, format='json')
        updatedData={'id': 'http://127.0.0.1:8000/authors/1', 'title': 'newTestTitle', 'source': 'newTestSource', 'origin': 'newTestOrigin', 'description': '', 'content': 'newTestContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/1/comments/'}

        self.assertEqual(updatedResponse.status_code, 400)


    # Delete a created post
    def testDELETEPostSuccess(self):
        # Created a post
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, self.postData, format='json')

        # Delete the created post using DELETE
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        newPostData={}
        newResponse=self.client.delete(url, newPostData)
        self.assertEqual(newResponse.status_code, 200)
 
        # Try GETing the deleted post: expect 404
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        getResponse=self.client.get(url, newPostData)
        self.assertEqual(getResponse.status_code, 404)

    # Delete an not existed post
    def testDELETEPostFail(self):
        # Created a post
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, self.postData, format='json')

        # Delete an unexisted post (id=2) using DELETE
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':2})
        newPostData={}
        newResponse=self.client.delete(url, newPostData)
        self.assertEqual(newResponse.status_code, 404)
 
        # Try GETing the creaed post: expect 200
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        getResponse=self.client.get(url, newPostData)
        self.assertEqual(getResponse.status_code, 200)
        expectedData={'id': 'http://127.0.0.1:8000/authors/2/posts/1', 'title': 'testTitle', 'source': 'testSource', 'origin': 'testOrigin', 'description': '', 'content': 'testContent', 'contentType': 'text/plain', 'author': {'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}, 'published': '2023-03-03T00:41:14Z', 'visibility': 'VISIBLE', 'categories': 'test', 'unlisted': False, 'type': 'post', 'count': 0, 'comments': 'http://127.0.0.1:8000/authors/2/posts/1/comments/'}
        self.assertEqual(getResponse.data, expectedData)

# Tests for APIListPosts
class APIListPostsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)

        # add an User and Author first
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.testAuthor=Author.objects.filter(id="http://127.0.0.1:8000/authors/2").values()

        
        self.post1Data={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle1', 
                    'source':"testSource1", 
                    'origin':"testOrigin1", 
                    'descritption':"testDescription1", 
                    'content': 'testContent1', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }
        
        self.post2Data={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle2', 
                    'source':"testSource2", 
                    'origin':"testOrigin2", 
                    'descritption':"testDescription2", 
                    'content': 'testContent2', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        

    def testPOSTListPostsSuccess(self):
        # Create a post
        url=reverse('socialDist:posts', kwargs={'author_id':2})
        response=self.client.post(url, self.post1Data, format='json')
        self.assertEqual(response.status_code, 201)

        # Check the values from response's fields:
        # Can only check upto id's last 10 char due to randomness of string producing
        self.assertEqual(response.data['id'][:-10], 'http://127.0.0.1:8000/authors/2/posts/')
        self.assertEqual(response.data['title'], 'testTitle1')
        self.assertEqual(response.data['source'], 'testSource1')
        self.assertEqual(response.data['origin'], 'testOrigin1')
        self.assertEqual(response.data['description'], '')
        expectedData={'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.data['author'], expectedData)
        self.assertEqual(response.data['content'], 'testContent1')
        self.assertEqual(response.data['contentType'], 'text/plain')
        self.assertEqual(response.data['published'][:4], '2023')
        self.assertEqual(response.data['visibility'], 'VISIBLE')
        self.assertEqual(response.data['categories'], 'test')
        self.assertEqual(response.data['unlisted'], False)
        self.assertEqual(response.data['type'], 'post')
        self.assertEqual(response.data['count'], 0)
        
    # POST with invalid model field
    def testPOSTListPostsFail(self):
        self.post2Data={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle2', 
                    'source':"testSource2", 
                    'origin':"testOrigin2", 
                    'descritption':"testDescription2", 
                    'content': 'testContent2', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    # 'published':"2023-03-20T20:15:29.761059Z",
                    'visibility': 'private', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        url=reverse('socialDist:posts', kwargs={'author_id':2})
        response=self.client.post(url, self.post2Data, format='json')
        self.assertEqual(response.status_code, 400)

    # add posts, then get it
    def testGETListPostsSuccess(self):

        # adding both posts, then getting it
        url=reverse('socialDist:posts', kwargs={'author_id':2})
        response=self.client.post(url, self.post1Data, format='json')

        url=reverse('socialDist:posts', kwargs={'author_id':2})
        response=self.client.post(url, self.post2Data, format='json')

        # GETing it
        response=self.client.get(url, {})
        
        # Check the values from response's fields:
        # Can only check upto id's last 10 char due to randomness of string producing

        # Test first post
        self.assertEqual(response.data['items'][0]['id'][:-10], 'http://127.0.0.1:8000/authors/2/posts/')
        self.assertEqual(response.data['items'][0]['title'], 'testTitle1')
        self.assertEqual(response.data['items'][0]['source'], 'testSource1')
        self.assertEqual(response.data['items'][0]['origin'], 'testOrigin1')
        self.assertEqual(response.data['items'][0]['description'], '')
        expectedData={'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.data['items'][0]['author'], expectedData)
        self.assertEqual(response.data['items'][0]['content'], 'testContent1')
        self.assertEqual(response.data['items'][0]['contentType'], 'text/plain')
        self.assertEqual(response.data['items'][0]['published'][:4], '2023')
        self.assertEqual(response.data['items'][0]['visibility'], 'VISIBLE')
        self.assertEqual(response.data['items'][0]['categories'], 'test')
        self.assertEqual(response.data['items'][0]['unlisted'], False)
        self.assertEqual(response.data['items'][0]['type'], 'post')
        self.assertEqual(response.data['items'][0]['count'], 0)
        self.assertEqual(response.data['items'][0]['comments'][-10:],"/comments/")

        # Test second post content
        self.assertEqual(response.data['items'][1]['id'][:-10], 'http://127.0.0.1:8000/authors/2/posts/')
        self.assertEqual(response.data['items'][1]['title'], 'testTitle2')
        self.assertEqual(response.data['items'][1]['source'], 'testSource2')
        self.assertEqual(response.data['items'][1]['origin'], 'testOrigin2')
        self.assertEqual(response.data['items'][1]['description'], '')
        expectedData={'id': 'http://127.0.0.1:8000/authors/2', 'host': 'http://127.0.0.1:8000/', 'displayName': 'alex', 'github': '', 'profileImage': '', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/2'}
        self.assertEqual(response.data['items'][1]['author'], expectedData)
        self.assertEqual(response.data['items'][1]['content'], 'testContent2')
        self.assertEqual(response.data['items'][1]['contentType'], 'text/plain')
        self.assertEqual(response.data['items'][1]['published'][:4], '2023')
        self.assertEqual(response.data['items'][1]['visibility'], 'VISIBLE')
        self.assertEqual(response.data['items'][1]['categories'], 'test')
        self.assertEqual(response.data['items'][1]['unlisted'], False)
        self.assertEqual(response.data['items'][1]['type'], 'post')
        self.assertEqual(response.data['items'][1]['count'], 0)
        self.assertEqual(response.data['items'][1]['comments'][-10:],"/comments/")

    # GET when there are no posts
    def testGETListPostsEmpty(self):
        # GET without adding and post
        url=reverse('socialDist:posts', kwargs={'author_id':2})
        # adding first post
        testData={}
        response=self.client.get(url, testData, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['type'], 'posts')
        self.assertEqual(response.data['items'], [])

    def testGETListPostsFail(self):
        # GET with an invalid author
        url=reverse('socialDist:posts', kwargs={'author_id':3})
        # adding first post
        testData={}
        response=self.client.get(url, testData, format='json')
        self.assertEqual(response.status_code, 404)

# Test for APIImage
class APIImageTests(TestCase):
    # Setup the image from user --> post --> image
    def setUp(self):
        # Creeate User
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)

        # use user to create author
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.testAuthor=Author.objects.filter(id="http://127.0.0.1:8000/authors/2").values()

        # reading an image for good post
        with open("socialDist/tests/testImage1.jpg", "rb") as image:
            imageString=base64.b64encode(image.read())

        # Add a post that has the image type
        self.goodPostData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': imageString, 
                    'contentType': "image/png;base64", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

         # Create good post using author
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, self.goodPostData, format='json')

        # Add a post that does NOT have the image type
        self.badPostData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': 'testContent', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        # Create bad post using author
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':2})
        response=self.client.get(url, self.badPostData, format='json')

    # TODO: finish success once image post is done
    def testGETImageSuccess(self):
        url=reverse('socialDist:image', kwargs={'author_id':2, 'post_id': 1})
        response=self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, 200)

    # Getting the image when the post's type is not "image/png;base64": expect 404
    def testGETImageFail(self):
        url=reverse('socialDist:image', kwargs={'author_id':2, 'post_id': 2})
        response=self.client.get(url, {}, format='json')
        
        self.assertEqual(response.status_code, 404)


# Test for APIComment
class APIListCommentTests(TestCase):
    # Setup the image from user --> post --> comment
    def setUp(self):       
        # Creeate User
        self.client = APIClient()
        self.user=User.objects.create_user('test','test@gmail.com', 'password')
        self.client.force_authenticate(user=self.user)

        # use user to create author
        data={'username': 'alex', "email": 'alexmail', "password1": 'a'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.testAuthor=Author.objects.filter(id="http://127.0.0.1:8000/authors/2").values()

        # Create that post
        self.postData={"id":"http://127.0.0.1:8000/authors/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': 'testContent', 
                    'contentType': "text/plain", 
                    'author': self.testAuthor[0], 
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        # Create a post using author
        url=reverse('socialDist:post', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, self.postData, format='json')

    def testPOSTListCommentSuccess(self):
        # adding the comments from the post
        commentData={}
        url=reverse('socialDist:comments', kwargs={'author_id':2, 'post_id':1})
        response=self.client.put(url, {}, format='json')

# TODO: APIPosts?
"""

"""
class APIListAuthorTests(TestCase):
    def setUp(self):
        # Setup server
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_user(username='test',email='test@gmail.com', password='password')
        # get the User back and assign it
        self.user=User.objects.get(username='test')

        self.client = APIClient()
        # peform force authentication
        self.client.force_authenticate(user=self.user)
        

    # Basic test: DONE? 
    def testGETListAuthors(self):
        # Create an author based on an user 
        testAuthor=Author.objects.create(user=self.user, id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")

        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # test basic API fields

        # Still gives 403...
        self.assertEqual(response.status_code, 200)
"""


# # CURL testing
# class APIListAuthorTestsCURL(TestCase):
#     # Setup client, a dummy broswer used for testing
#     def setUp(self):
#         new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
#         new_server.save()

#         User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
#         self.user=User.objects.get(username='test')

#         # self.client.force_login(self.user)

#         # token=Token.objects.get_or_create(user__username='test')
#         self.client = CurlClient()

#         self.client.force_authenticate(user=self.user)

#     def testBasic(self):

#         data={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}

#         url=reverse('socialDist:authors')
#         # PUT the author
#         response=self.client.put(url, data)
#         self.assertEqual(201, response.status_code)

#         response=self.client.curl(
#             """
#             curl http://127.0.0.1:8000/authors/
#             """
#         )



#         print(response.status_code)