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
    def testGETListAuthors(self):

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
    def testPUTListAuthorsSuccess(self):
        # Successful case, should return 201
        data={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}

        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.assertEqual(201, response.status_code)

    def testPUTListAuthorsFailure(self):
        # Failure case: test with existing user (same data) --> give 409

        # same beginning as the success case
        data={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}
        url=reverse('socialDist:authors')
        response=self.client.put(url, data)
        self.assertEqual(201, response.status_code)

        # put a again with new data, but same user
        newdata={'username': 'sigh', "email": 'sighmail', "password1": 'sighpwd'}
        url=reverse('socialDist:authors')
        
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
    def testGETAuthorSuccess(self):

        # Work by creating objects, but want to create through POST
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id="http://127.0.0.1:8000/authors/2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg") 


        url = reverse('socialDist:author', args="1")
        # url = reverse('socialDist:author', kwargs={'id':1})
        response = self.client.get(url)
        expectedData={'id': 'http://127.0.0.1:8000/authors/1', 'host': 'http://127.0.0.1:8000/', 'displayName': 'tester1', 'github': 'http://github.com/test1', 'profileImage': 'https://i.imgur.com/test1.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/1'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expectedData)

    # Find an author doesn't exist
    def testGETAuthorFailure(self):
        # Work by creating objects, but want to create through POST
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")

        url = reverse('socialDist:author', args="2")
        response = self.client.get(url)
        expectedData={'id': 'http://127.0.0.1:8000/authors/1', 'host': 'http://127.0.0.1:8000/', 'displayName': 'tester1', 'github': 'http://github.com/test1', 'profileImage': 'https://i.imgur.com/test1.jpeg', 'type': 'author', 'url': 'http://127.0.0.1:8000/authors/1'}

        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.data, expectedData)

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
        self.assertEqual(response.data['published'], '2023-03-03T00:41:14Z')
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
                    'published':"2023-03-03T00:41:14Z",
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
        self.assertEqual(response.data['items'][0]['published'], '2023-03-03T00:41:14Z')
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
        self.assertEqual(response.data['items'][1]['published'], '2023-03-03T00:41:14Z')
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

    
        # TODO: Issue found: Only returns the latest author for api_helper.construct_list_of_posts







# TODO: APIPosts?