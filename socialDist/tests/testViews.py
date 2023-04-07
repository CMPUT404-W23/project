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

import json, datetime
from django.utils.timezone import make_aware
from rest_framework import status
from socialDist.serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from socialDist.models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User
from rest_framework.test import APIClient, force_authenticate

# NOTE:
# BACK-END tests for API views
# TO RUN ALL the TESTS in this file: Enter Command "python manage.py test socialDist.tests.testViews"

HOST="https://socialdistcmput404.herokuapp.com/"

# Test case for the API views APIListAuthors
class APIListAuthorsTests(TestCase):
    # Setup client, a dummy broswer used for testing
    def setUp(self):
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        # create users and perform authentication
        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        User.objects.create_superuser(username='test1',email='test1@gmail.com', password='password1')
        self.user2=User.objects.get(username='test1')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})

        self.client.force_authenticate(user=self.user)

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
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

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
        self.assertEqual(response.status_code, 404)

    # for POST: add a new author
    def testPOSTAuthorSuccess(self):
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/ for an existed author
        """
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # check status code
        self.assertEqual(response.status_code, 200)
        # get the UUID
        authorUUID=response.data['items'][0]['id'].split("/")[-1]

        updateData={
            "id": "https://socialdistcmput404.herokuapp.com/authors/",
            "host": "https://socialdistcmput404.herokuapp.com/",
            "displayName": "TestAuthor",
            "github": "https://github.com/testUser/",
            "profileImage": "http://sampleUserImage.com/1.jpg",
            "type": "author",
            "url": "https://socialdistcmput404.herokuapp.com/authors/"
        }

        newUrl=reverse('socialDist:author', kwargs={"id":authorUUID})
        # test status code
        response = self.client.post(newUrl, updateData, format="json")
        self.assertEqual(response.status_code, 201)

        # test data
        self.assertEqual(response.data['type'], 'author')
        self.assertEqual(response.data['host'], HOST)
        self.assertEqual(response.data['displayName'],'TestAuthor')
        self.assertEqual(response.data['github'], "https://github.com/testUser/")
        self.assertEqual(response.data['profileImage'], "http://sampleUserImage.com/1.jpg")
        # Find the authorUUID to test id and url
        self.assertEqual(response.data['id'],HOST+"authors/"+authorUUID)
        self.assertEqual(response.data['url'],HOST+"authors/"+authorUUID)
        

    def testPOSTAuthorFailureAuthorEmpty(self):
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/ for a non-existed author
        """
        newUrl=reverse('socialDist:author', kwargs={"id":'1'})
        # test status code: expect 404
        response = self.client.post(newUrl, {})
        self.assertEqual(response.status_code, 404)

    def testPOSTAuthorFailureInvalidSerializer(self):
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/ for invalid serializer fields
        """
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # check status code
        self.assertEqual(response.status_code, 200)
        # get the UUID
        authorUUID=response.data['items'][0]['id'].split("/")[-1]

        updateData={
            "id": "https://socialdistcmput404.herokuapp.com/authors/",
            "host": "https://socialdistcmput404.herokuapp.com/",
            "github": "github.ca/testUser",
            "type": "author",
            "url": "https://socialdistcmput404.herokuapp.com/authors/"
        }
        newUrl=reverse('socialDist:author', kwargs={"id":authorUUID})
        # test status code
        response = self.client.post(newUrl, updateData)
        self.assertEqual(response.status_code, 400)

        errorData="{'github': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}"
        self.assertEqual(str(response.data), errorData)

class APIListPostsTests(TestCase):
    def setUp(self): 
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author
        url=reverse('socialDist:authors')

        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # check status code
        self.assertEqual(response.status_code, 200)
        # get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]
        
    # Test creating a post with a randomized ID
    def testPOSTPostSuccess(self):
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/posts for valid serializer data
        """
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }

        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # POST the post
        response=self.client.post(url, data, format='json')
        # Test status code
        self.assertEqual(201, response.status_code)

        postUUID=response.data['id'].split("/")[-1]
        
        # Test data
        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+postUUID, 
            'title': 'sample post title', 
            'source': 'sample source', 
            'origin': 'sample origin', 
            'description': 'sample Post descr', 
            'content': 'sample post content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID},  
            'visibility': 'VISIBLE', 
            'categories': 'testing', 
            'unlisted': True, 'type': 
            'post', 'count': 0, 
            'comments': HOST+'authors/'+self.authorUUID+'/posts/'+postUUID+'/comments/'}

        response.data.pop('published')

        # test without the date
        self.assertEqual(expectedData, response.data)

    # changing the visibility of a post: give 400
    def testPOSTPostFail(self):
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/posts for invalid serializer fields
        """
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }

        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the author
        response=self.client.post(url, data)
        self.assertEqual(400, response.status_code)
        
    # Test creating a post
    def testGETPostSuccess(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/posts for valid serializer data
        """
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, data, format='json')

        # Test status code
        self.assertEqual(201, response.status_code)
        # Get the UUID of the post
        postUUID=response.data['id'].split("/")[-1]

        # Do GET API
        response=self.client.get(url)
        self.assertEqual(response.data['type'], 'posts')

        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+postUUID, 
            'title': 'sample post title', 
            'source': 'sample source', 
            'origin': 'sample origin', 
            'description': 'sample Post descr', 
            'content': 'sample post content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID},  
            'visibility': 'VISIBLE', 
            'categories': 'testing', 
            'unlisted': True, 'type': 
            'post', 'count': 0, 
            'comments': HOST+'authors/'+self.authorUUID+'/posts/'+postUUID+'/comments/'}

        # test without the date
        response.data["items"][0].pop('published')
        self.assertEqual(expectedData, response.data["items"][0])

    # Getting a post that doesn't exist
    def testGETPostFail(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/posts for an author who doesn't exist
        """
        url=reverse('socialDist:posts', kwargs={"author_id":1})
        response=self.client.get(url)
        self.assertEqual(404, response.status_code)

class APIPostTests(TestCase):
    def setUp(self): 
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # Adding a post
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/posts for valid serializer data
        """
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, data, format='json')
        self.postUUID=response.data['id'].split("/")[-1]

    def testGETPostSuccess(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/posts, test status code and response data
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.get(url)

        # test status code
        self.assertEqual(200, response.status_code)

        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID, 
            'title': 'sample post title', 
            'source': 'sample source', 
            'origin': 'sample origin', 
            'description': 'sample Post descr', 
            'content': 'sample post content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID},  
            'visibility': 'VISIBLE', 
            'categories': 'testing', 
            'unlisted': True, 'type': 
            'post', 'count': 0, 
            'comments': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'}

        # Test data for easier testing
        response.data.pop('published')
        self.assertEqual(response.data, expectedData)

    def testGETPostFailure(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/posts, with unexisted author
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":1})
        response=self.client.get(url)

        # test status code
        self.assertEqual(404, response.status_code)

    def testPOSTPostSuccess(self):
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/posts, test status code and response data
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        postData={'source': 'sample source2'}
        response=self.client.post(url, postData, format='json')

        # test status code
        self.assertEqual(201, response.status_code)
        # test updated field
        self.assertEqual(response.data['source'],'sample source2')

    def testPOSTPostFailure(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/posts, with invalid serializer fields
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        postData={'source': 'sample source2'}
        response=self.client.post(url, postData)

        # test status code
        self.assertEqual(400, response.status_code)
        # test updated field
        errorData="{'source': [ErrorDetail(string='Not a valid string.', code='invalid')]}"
        self.assertEqual(str(response.data), errorData)

    def testPUTPostSuccess(self):
        """
        Test PUT method for API with endpoint: /api/authors/<author_id>/posts, test status code and response data
        """
        # Send request
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        putData={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        response=self.client.put(url, putData, format='json')

        # test status code
        self.assertEqual(201, response.status_code)

        # test data
        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID, 
            'title': 'sample post title', 
            'source': 'sample source', 
            'origin': 'sample origin', 
            'description': 'sample Post descr', 
            'content': 'sample post content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID},  
            'visibility': 'VISIBLE', 
            'categories': 'testing', 
            'unlisted': True, 'type': 
            'post', 'count': 0, 
            'comments': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'}

        response.data.pop('published')
        self.assertEqual(response.data, expectedData)

    def testPUTPostFailure(self):
        """
        Test GET method for API with endpoint: /api/authors/<author_id>/posts, but with invalid serializer field
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        putData={
            'categories': "",
            }
        response=self.client.put(url, putData)

        # test status code
        self.assertEqual(400, response.status_code)

    def testDELETEPostSuccess(self):
        """
        Test DELETE method for API with endpoint: /api/authors/<author_id>/posts, test status code 
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.delete(url)

        # test status code
        self.assertEqual(200, response.status_code)

        # Try to get the post: expect to return 404
        response=self.client.get(url)
        self.assertEqual(404, response.status_code)

    def testDELETEPostFailure(self):
        """
        Test DELETE method for API with endpoint: /api/authors/<author_id>/posts, with unexisted post id
        """
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":1})
        response=self.client.delete(url)

        # test status code
        self.assertEqual(404, response.status_code)

    def testGETPostsSuccess(self):
        """
        Test GET method for API with endpoint: /posts/
        """
        url=reverse('socialDist:allposts')
        response=self.client.get(url)

        # test status code
        self.assertEqual(200, response.status_code)

        # test data
        expectedData={'type': 'posts', 'items': []}
        self.assertEqual(response.data, expectedData)

    def testGETPrivatePostsSuccess(self):
        """
        Test GET method for API with endpoint: authors/<str:author_id>/private-posts/
        """ 
        url=reverse('socialDist:private-posts',kwargs={"author_id":self.authorUUID})
        response=self.client.get(url)

        # test status code
        self.assertEqual(200, response.status_code)

        # test data
        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID, 
            'title': 'sample post title', 
            'source': 'sample source', 
            'origin': 'sample origin', 
            'description': 'sample Post descr', 
            'content': 'sample post content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID},  
            'visibility': 'VISIBLE', 
            'categories': 'testing', 
            'unlisted': True, 'type': 
            'post', 'count': 0, 
            'comments': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'}

        response.data["items"][0].pop('published')

        self.assertEqual(expectedData,response.data["items"][0])

class APIImageTests(TestCase):
    def setUp(self): 
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')
        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # Adding a post
        """
        Test POST method for API with endpoint: /api/authors/<author_id>/posts for valid serializer data
        """
        data={
            "title": "sample Image post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "image string",
            "contentType": "image/jpg;base64",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, data, format='json')
        self.postUUID=response.data['id'].split("/")[-1]

    def testGETImagePostSuccess(self): 
        url=reverse('socialDist:post', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.get(url)

        # Test status code
        self.assertEqual(200, response.status_code)

        # Test data
        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID, 
            "title": "sample Image post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "image string",
            "contentType": "image/jpg;base64",
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID},  
            'visibility': 'VISIBLE', 
            'categories': 'testing', 
            'unlisted': True, 'type': 
            'post', 'count': 0, 
            'comments': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'}

        response.data.pop('published')
        self.assertEqual(response.data, expectedData)

class APIListCommentsTests(TestCase):
    def setUp(self): 
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID for author
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # Adding a post
        postData={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, postData, format='json')
        self.postUUID=response.data['id'].split("/")[-1]

    def testPOSTCommentSuccess(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/' for an existed author and valid fields for CommentSerializer to pass
        """
        # Perform POST request
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID,
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID
            },
            "type": "comment"
            }
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.post(url, commentData, format='json')

        # test status code
        self.assertEqual(201, response.status_code)

        # Get UUID of comment for testing
        commentUUID=response.data['id'].split("/")[-1]

        # test data
        expectedData={
            'id': 'https://socialdistcmput404.herokuapp.com/authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+commentUUID, 
            'comment': 'Test comment content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID,
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
                }, 
            'type': 'comment'}

        # test data without published field (hard to test)
        response.data.pop('published')
        self.assertEqual(response.data, expectedData)

    def testPOSTCommentFailure(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/' for an existed author but unexisted post
        """
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID,
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID
            },
            "type": "comment"
            }
        # Send POST request
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":1})
        response=self.client.post(url, commentData, format='json')

        # test status code
        self.assertEqual(404, response.status_code)
        # test data: expect return empty
        self.assertEqual(response.data, None)

    def testGETCommentSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/' for an existed author, post, and comments
        """
        # POST a comment
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID,
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID
            },
            "type": "comment"
            }
        # Send POST request
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.post(url, commentData, format='json')

        # test status code
        self.assertEqual(201, response.status_code)

        # Get that comment
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.get(url)

        # test status code
        self.assertEqual(response.data['type'], 'comments')
        commentUUID=response.data['items'][0]['id'].split("/")[-1]
        
        # Test data
        expectedData={
            'id': 'https://socialdistcmput404.herokuapp.com/authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+commentUUID, 
            'comment': 'Test comment content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
                }, 
            'type': 'comment'}

        # test data without published field (hard to test)
        response.data["items"][0].pop('published')
        self.assertEqual(response.data['items'][0], expectedData)
    def testGETCommentFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/' for an existed author, but unexisted post
        """
        # POST a comment
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID,
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID
            },
            "type": "comment"
            }
        # Send POST request
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.post(url, commentData, format='json')

        # Get that comment
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":2})
        response=self.client.get(url)

        # Test status code
        self.assertEqual(404, response.status_code)

class APICommentTests(TestCase):
    def setUp(self): 
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # Adding a post
        postData={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, postData, format='json')
        self.postUUID=response.data['id'].split("/")[-1]

        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID,
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID
            },
            "type": "comment"
            }
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.post(url, commentData, format='json')

        self.commentUUID=response.data['id'].split("/")[-1]

    def testGETCommentSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/' for an existed author, post, and comment
        """
        # send GET request
        url=reverse('socialDist:comment', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID, "comment_id":self.commentUUID})
        response=self.client.get(url)

        # Test status code
        self.assertEqual(200, response.status_code)

        # Test data
        expectedData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+self.commentUUID, 
            'comment': 'Test comment content', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
                }, 
            'type': 'comment'}

        response.data.pop('published')
        self.assertEqual(response.data, expectedData)
    def testGETCommentFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/' for an existed author, post, but unexisted comment
        """
        # Send invalid GET request
        url=reverse('socialDist:comment', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID, "comment_id":1})
        response=self.client.get(url)

        # Test status code
        self.assertEqual(404, response.status_code)

class APIInboxTests(TestCase):
    def setUp(self): 
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

    def testGETInboxEmpty(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/inbox/' for an existed author
        """
        # Send GET Request
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        response = self.client.get(url)

        # Test status code
        self.assertEqual(200, response.status_code)

        # Test data: expect empty
        expectedData={
            'type': 'inbox', 
            'author': 'https://socialdistcmput404.herokuapp.com/authors/'+self.authorUUID, 
            'items': []
        }
        self.assertEqual(response.data, expectedData)

    def testGETInboxSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/inbox/' for an existed author and an post object inside inbox
        """
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        postData={"id":"http://127.0.0.1:8000/authors/"+self.authorUUID+"/posts/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': 'testContent', 
                    'contentType': "text/plain", 
                    'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                        },  
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }

        # Send POST request
        response = self.client.post(url, postData, format='json')
        self.assertEqual(200, response.status_code)

        # Get the post object
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        response = self.client.get(url)

        # test status code and some fields
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['type'], 'inbox')
        self.assertEqual(response.data['author'], HOST+'authors/'+self.authorUUID)

        # test the rest of the data
        expectedData={
            'id': 'http://127.0.0.1:8000/authors/'+self.authorUUID+'/posts/1', 
            'title': 'testTitle', 
            'source': 'testSource', 
            'origin': 'testOrigin', 
            'description': '', 
            'content': 'testContent', 
            'contentType': 'text/plain', 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
                }, 
            'visibility': 'VISIBLE', 
            'categories': 'test', 
            'unlisted': False, 
            'type': 'post', 
            'count': 0, 
            'comments': 'http://127.0.0.1:8000/authors/'+self.authorUUID+'/posts/1/comments/'
            }

        response.data["items"][0].pop('published')
        self.assertEqual(response.data["items"][0], expectedData)

    def testPOSTInboxPostSuccess(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/inbox/' for POSTing an post object to the inbox
        """
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        postData={"id":"http://127.0.0.1:8000/authors/"+self.authorUUID+"/posts/1", 
                    "title":'testTitle', 
                    'source':"testSource", 
                    'origin':"testOrigin", 
                    'descritption':"testDescription", 
                    'content': 'testContent', 
                    'contentType': "text/plain", 
                    'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                        },  
                    'published':"2023-03-03T00:41:14Z",
                    'visibility': 'VISIBLE', 
                    'categories': 'test', 
                    'unlisted': False, 
                    "type": "post",
                    "count": 1,
                    "comments": "http://127.0.0.1:8000/authors/2/posts/1/comments/"
                    }
        # Send the post object
        response = self.client.post(url, postData, format='json')

        # Test status code
        self.assertEqual(200, response.status_code)

    def testPOSTInboxCommentSuccess(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/inbox/' for POSTing an post object to the inbox
        """

        # Create a post through POST in APIListPosts first
        postData={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }

        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})

        # POST the post
        response=self.client.post(url,postData, format='json')
        # Test status code
        self.assertEqual(201, response.status_code)
        postUUID=response.data['id'].split("/")[-1]

        # use the post object to POST an comment object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        commentData={
            "id": HOST+"authors/"+self.authorUUID+"/posts/"+postUUID+"/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                        },  
            "type": "comment"
            }
        # Send POST request
        response = self.client.post(url, commentData, format='json')
        
        # Test status code
        self.assertEqual(200, response.status_code)

    def testPOSTInboxPostLikeSuccess(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/inbox/' for POSTing an like object (post like) to the inbox
        """
        # Create a post through POST in APIListPosts first
        postData={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})

        # Send POST request
        response=self.client.post(url,postData, format='json')
        # Test status code
        self.assertEqual(201, response.status_code)
        postUUID=response.data['id'].split("/")[-1]

        # use the post object to POST an comment object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        likeData={
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "TestAuthor Likes your post",
            "type": "Like",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                    },  
            "object": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID+"/posts/"+postUUID
        }
        # Send POST request
        response = self.client.post(url, likeData, format='json')

        # Test status code
        self.assertEqual(200, response.status_code)
    
    def testPOSTInboxCommentLikeSuccess(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/inbox/' for POSTing an like object (comment like) to the inbox
        """
        # Create a post through POST in APIListPosts first
        postData={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})

        # POST the post
        response=self.client.post(url,postData, format='json')
        # Test status code
        self.assertEqual(201, response.status_code)
        postUUID=response.data['id'].split("/")[-1]

        # test add a comment based on created post
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID,
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID
            },
            "type": "comment"
            }
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":postUUID})
        response=self.client.post(url, commentData, format='json')

        # test status code
        self.assertEqual(201, response.status_code)

        commentUUID=response.data['id'].split("/")[-1]


        # use the post object to POST an comment object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        likeData={
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "TestAuthor Likes your post",
            "type": "Like",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                    },  
            "object": "https://socialdistcmput404.herokuapp.com/authors/"+self.authorUUID+"/posts/"+postUUID+"/comments/"+commentUUID
        }
        # Send POST request
        response = self.client.post(url, likeData, format='json')

        # Test status code
        self.assertEqual(200, response.status_code)

    def testPOSTInboxFollowSuccess(self): 
        """
        Test POST method for API with endpoint: 'authors/<str:author_id>/inbox/' for POSTing a follow request object to the inbox
        """

        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')

        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        # send POST request to send follow request objects
        response = self.client.post(url, followRequestData, format='json')
        self.assertEqual(200, response.status_code)

    def testDeleteInboxSuccess(self): 
        """
        Test DELETE method for API with endpoint: 'authors/<str:author_id>/inbox/' for clearing an inbox from an existing author
        """
        # Send DELETE request
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        response = self.client.delete(url)

        # Test status code
        self.assertEqual(200, response.status_code)

    def testDeleteInboxFailure(self): 
        """
        Test DELETE method for API with endpoint: 'authors/<str:author_id>/inbox/' for clearing an inbox from a non-existing author
        """
        # Send DELETE request
        url=reverse('socialDist:inbox',kwargs={"author_id":1})
        response = self.client.delete(url)

        # Test status code
        self.assertEqual(404, response.status_code)

class APIFollowerTests(TestCase):
    def setUp(self):
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

    def testPUTFollowerSuccess(self): 
        """
        Test PUT method for API with endpoint: 'authors/<str:author_id>/followers/<path:foreign_author_id>/' for an existed author and a foreign author
        """
        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # Send follow request from 2 to 1's inbox
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        # Send POST request
        response = self.client.post(url, followRequestData, format='json')

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        
        # Send the PUT request
        response = self.client.put(url)

        # Test status code
        self.assertEqual(201, response.status_code)
        
    def testPUTFollowerFailure(self): 
        """
        Test PUT method for API with endpoint: 'authors/<str:author_id>/followers/<path:foreign_author_id>/' for an non-existed author and a foreign author
        """
        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":1, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.put(url)

        # Test status code
        self.assertEqual(404, response.status_code)
    
    def testGETFollowerSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/followers/<path:foreign_author_id>/' for an existed author and a foreign author
        """
        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # Send follow request from 2 to 1's inbox
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        response = self.client.post(url, followRequestData, format='json')

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.put(url)

        # Actual testing the GET api method
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.get(url)

        # Test status code
        self.assertEqual(200, response.status_code)
        
        # Test data
        expectedData={
            'id': 'https://socialdistcmput404.herokuapp.com/authors/'+author2UUID, 
            'host': 'https://socialdistcmput404.herokuapp.com/', 
            'displayName': 'testUsername2', 
            'github': '', 
            'profileImage': '', 
            'type': 'author', 
            'url': 'https://socialdistcmput404.herokuapp.com/authors/'+author2UUID
            }
        self.assertEqual(expectedData, response.data)

    def testGETFollowerFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/followers/<path:foreign_author_id>/' for a non-existed author and a foreign author
        """
         # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # Send follow request from 2 to 1's inbox
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        response = self.client.post(url, followRequestData, format='json')

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.put(url)

        # Actual testing the GET api method
        url=reverse('socialDist:follower',kwargs={"author_id":1, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.get(url)
        # test status code
        self.assertEqual(404, response.status_code)

    def testDELETEFollowerSuccess(self): 
        """
        Test DELETE method for API with endpoint: 'authors/<str:author_id>/followers/<path:foreign_author_id>/' for an existed author and a foreign author
        """
        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # Send follow request from 2 to 1's inbox
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        response = self.client.post(url, followRequestData, format='json')

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.put(url)

        # Actual testing the GET api method
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.delete(url)

        # test status code
        self.assertEqual(200, response.status_code)

    def testDELETEFollowerFailure(self): 
        """
        Test DELETE method for API with endpoint: 'authors/<str:author_id>/followers/<path:foreign_author_id>/' for a non-existed author and a foreign author
        """
        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # get the UUID
        author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # Send follow request from 2 to 1's inbox
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})

        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        response = self.client.post(url, followRequestData, format='json')

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.put(url)

        # Actual testing the GET api method
        url=reverse('socialDist:follower',kwargs={"author_id":1, "foreign_author_id":HOST+"authors/"+author2UUID})
        response = self.client.delete(url)

        # test status code
        self.assertEqual(404, response.status_code)

class APIFollowersTests(TestCase):
    def setUp(self):
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)

        # Get the UUID for the first author
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # PUT another author
        User.objects.create_superuser(username='test2',email='test2@gmail.com', password='password2')
        user=User.objects.get(username='test2')
        self.client.force_authenticate(user=user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author2Data={'username': 'testUsername2', "email": 'test2@gmail.com', "password1": 'testPassword2'}
        response=self.client.put(url, author2Data)
        
        # Use a GET for APIListAuthors to get the author's UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)

        # Get the UUID for the second author
        self.author2UUID=response.data['items'][1]['id'].split("/")[-1]

        # Send follow request from 2 to 1's inbox
        # POST an post object to the author's inbox
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        followRequestData={
            "type": "Follow",      
            "summary":"testUsername2 wants to follow testUsername1",
            "actor":{
                'id': HOST+'authors/'+self.author2UUID, 
                'host': HOST, 
                'displayName': 'testUsername2', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.author2UUID
            },
            "object":
            {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID
            }
        }
        # Send the POST request
        response = self.client.post(url, followRequestData, format='json')

        # let the second author follow the first author (created in setup)
        url=reverse('socialDist:follower',kwargs={"author_id":self.authorUUID, "foreign_author_id":HOST+"authors/"+self.author2UUID})
        response = self.client.put(url)

        # Test status code
        self.assertEqual(201, response.status_code)

    def testGETFollowersSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/followers/' for an existed author and a foreign author
        """
        # Send the GET request
        url=reverse('socialDist:followers',kwargs={"author_id":self.authorUUID})
        response = self.client.get(url)

        # Test status code
        self.assertEqual(200, response.status_code)

        # Test Data
        expectedData={
            'id': 'https://socialdistcmput404.herokuapp.com/authors/'+self.author2UUID, 
            'host': 'https://socialdistcmput404.herokuapp.com/', 
            'displayName': 'testUsername2', 
            'github': '', 
            'profileImage': '', 
            'type': 'author', 
            'url': 'https://socialdistcmput404.herokuapp.com/authors/'+self.author2UUID
        }
        self.assertEqual(response.data['type'], 'followers')
        self.assertEqual(response.data['items'][0], expectedData)

    def testGETFollowersFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/followers/' for a non-existed author and a foreign author
        """
        # Send the GET request
        url=reverse('socialDist:followers',kwargs={"author_id":1})
        response = self.client.get(url)

        # Test status code
        self.assertEqual(404, response.status_code)
        
class APILikedTests(TestCase):
    def setUp(self):
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # Get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # PUT a post
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, data, format='json')
        self.postUUID=response.data['id'].split("/")[-1]
        
        # PUT a comment from that post
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": HOST+"authors/"+self.authorUUID,
                "host": HOST,
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": HOST+"authors/"+self.authorUUID
            },
            "type": "comment"
        }
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.post(url, commentData, format='json')

        self.commentUUID=response.data['id'].split("/")[-1]

        # Add the like objects 
        # 1. Add like for post
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        likeData={
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "TestAuthor Likes your post",
            "type": "Like",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                    },  
            "object": HOST+"authors/"+self.authorUUID+"/posts/"+self.postUUID
        }
        response = self.client.post(url, likeData, format='json')

        # 2. Add like for comment
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        likeData={
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "TestAuthor Likes your post",
            "type": "Like",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                    },  
            "object": HOST+"authors/"+self.authorUUID+"/posts/"+self.postUUID+"/comments/"+self.commentUUID
        }
        response = self.client.post(url, likeData, format='json')

    def testGETLikedSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/liked/' for an existed author, post like and comment like
        """
        # Send the GET request
        url=reverse('socialDist:liked',kwargs={"author_id":self.authorUUID})
        response = self.client.get(url)

        # check status code
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['type'], "liked")

        # Testing data
        # 1. Testing postLike data

        # get the like ID here
        postLikeUUID=response.data["items"][0]['id'].split("/")[-1]
        
        # Test data
        expectedPostLikeData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/likes/'+postLikeUUID, 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID, 
            }, 
            'object': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID, 
            'summary': 'testUsername1 liked your post', 
            'type': 'Like'}

        # popped published time for easier testing
        response.data["items"][0].pop('published')
        self.assertEqual(response.data["items"][0], expectedPostLikeData)


        # 2. testing commentLike data
        commentLikeUUID=response.data["items"][1]['id'].split("/")[-1]

        # Test data
        expectedCommentLikeData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+self.commentUUID+'/likes/'+commentLikeUUID, 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID, 
            }, 
            'object': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+self.commentUUID,
            'summary': 'testUsername1 liked your comment', 
            'type': 'Like'}

        # popped published time for easier testing
        response.data["items"][1].pop('published')
        self.assertEqual(response.data["items"][1], expectedCommentLikeData)
        
    def testGETLikedFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/liked/' for an non-existed author
        """
        # Send GET request
        url=reverse('socialDist:liked',kwargs={"author_id":1})
        response = self.client.get(url)

        # check status code
        self.assertEqual(404, response.status_code)
 
class APIListLikesPostTests(TestCase):
    def setUp(self):
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Get the author and his/her UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # Get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # PUT a post
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, data, format='json')
        self.postUUID=response.data['id'].split("/")[-1]

        # Add like for post
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        likeData={
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "TestAuthor Likes your post",
            "type": "Like",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                    },  
            "object": HOST+"authors/"+self.authorUUID+"/posts/"+self.postUUID
        }
        response = self.client.post(url, likeData, format='json')

    def testGETListLikesPostSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/likes/' for an existed author, post, and post like
        """
        # Send GET request
        url=reverse('socialDist:post-likes',kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response = self.client.get(url)

        # check status code
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['type'], "likes")

        # test data
        postLikeUUID=response.data["items"][0]['id'].split("/")[-1]
        expectedPostLikeData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/likes/'+postLikeUUID, 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID, 
            }, 
            'object': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID, 
            'summary': 'testUsername1 liked your post', 
            'type': 'Like'}

        # popped published time for easier testing
        response.data["items"][0].pop('published')
        self.assertEqual(response.data["items"][0], expectedPostLikeData)

    def testGETListLikesPostFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/likes/' for an existed author, but non-existed post
        """
        # Send GET request
        url=reverse('socialDist:post-likes',kwargs={"author_id":self.authorUUID, "post_id":1})
        response = self.client.get(url)

        # check status code
        self.assertEqual(404, response.status_code)

class APIListLikesCommentTests(TestCase):
    def setUp(self):
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        self.client = APIClient(headers={"user-agent": "curl/7.79.1"})
        self.client.force_authenticate(user=self.user)

        # PUTing an author, also PUT in APIListAuthors will create inbox for the author 
        url=reverse('socialDist:authors')
        author1Data={'username': 'testUsername1', "email": 'test1@gmail.com', "password1": 'testPassword1'}
        response=self.client.put(url, author1Data)

        # Send GET request to get the author and his/her UUID
        url=reverse('socialDist:authors')
        response = self.client.get(url)
        # Get the UUID
        self.authorUUID=response.data['items'][0]['id'].split("/")[-1]

        # PUT a post
        data={
            "title": "sample post title",
            "source": "sample source",
            "origin": "sample origin",
            "description": "sample Post descr",
            "content": "sample post content",
            "contentType": "text/plain",
            'published': '2023-04-06T04:43:41.746Z',
            'visibility': 'VISIBLE',
            'categories': 'testing',
            'unlisted': True
            }
        url=reverse('socialDist:posts', kwargs={"author_id":self.authorUUID})
        
        # PUT the post
        response=self.client.post(url, data, format='json')
        self.postUUID=response.data['id'].split("/")[-1]
        
        # PUT a comment from that post
        commentData={
            "id": 'https://socialdistcmput404.herokuapp.com/authors/b2f461f6-cd88-40d5-903d-313d300bd356/posts/9ddcb1ac-4701-4795-aaa7-38b0e095a1ca/comments/e3e2417d-8c7c-4b40-ba21-fb07225dee15',
            "comment": "Test comment content",
            "contentType": "text/plain",
            "published": "2023-03-22T21:37:36Z",
            "author": {
                "id": HOST+"authors/"+self.authorUUID,
                "host": HOST,
                "displayName": "TestAuthor",
                "github": "www.githubtest.com",
                "profileImage": "testImage1.jpg",
                "type": "author",
                "url": HOST+"authors/"+self.authorUUID
            },
            "type": "comment"
        }
        # Send GET request to get the comment and its UUID
        url=reverse('socialDist:comments', kwargs={"author_id":self.authorUUID, "post_id":self.postUUID})
        response=self.client.post(url, commentData, format='json')
        # Get the comment UUID
        self.commentUUID=response.data['id'].split("/")[-1]

        # Add like for comment
        url=reverse('socialDist:inbox',kwargs={"author_id":self.authorUUID})
        likeData={
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "TestAuthor Likes your post",
            "type": "Like",
            'author': {
                        'id': HOST+'authors/'+self.authorUUID, 
                        'host': HOST, 
                        'displayName': 'testUsername1', 
                        'github': '', 
                        'profileImage': '', 
                        'type': 'author', 
                        'url': HOST+'authors/'+self.authorUUID
                    },  
            "object": HOST+"authors/"+self.authorUUID+"/posts/"+self.postUUID+"/comments/"+self.commentUUID
        }
        # POST that comment object
        response = self.client.post(url, likeData, format='json')

    def testGETListLikesCommentSuccess(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/' for an existed author, post, comment, and comment like
        """
        # Send GET request
        url=reverse('socialDist:comment-likes',kwargs={"author_id":self.authorUUID, "post_id":self.postUUID, "comment_id":self.commentUUID})
        response = self.client.get(url)

        # check status code
        self.assertEqual(200, response.status_code)
        
        
        # test data
        self.assertEqual(response.data['type'], "likes") 
        commentLikeUUID=response.data["items"][0]['id'].split("/")[-1]
        expectedCommentLikeData={
            'id': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+self.commentUUID+'/likes/'+commentLikeUUID, 
            'author': {
                'id': HOST+'authors/'+self.authorUUID, 
                'host': HOST, 
                'displayName': 'testUsername1', 
                'github': '', 
                'profileImage': '', 
                'type': 'author', 
                'url': HOST+'authors/'+self.authorUUID, 
            }, 
            'object': HOST+'authors/'+self.authorUUID+'/posts/'+self.postUUID+'/comments/'+self.commentUUID,
            'summary': 'testUsername1 liked your comment', 
            'type': 'Like'}

        # popped published time for easier testing
        response.data["items"][0].pop('published')
        self.assertEqual(response.data["items"][0], expectedCommentLikeData)

    def testGETListLikesCommentFailure(self): 
        """
        Test GET method for API with endpoint: 'authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/' for an existed author, post, comment like, but non-existed comment
        """
        # Send GET request
        url=reverse('socialDist:comment-likes',kwargs={"author_id":self.authorUUID, "post_id":self.postUUID, "comment_id":1})
        response = self.client.get(url)

        # check status code
        self.assertEqual(404, response.status_code)