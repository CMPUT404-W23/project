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

from django_test_curl import CurlClient
from django.test import TestCase, Client
from socialDist.models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User

# NOTE:
# BACK-END tests for API views
# TO RUN ALL the TESTS in this file: Enter Command "python manage.py test socialDist.tests.testCurl"

# Since the way we generate most of our new objects (authors, posts, comments, likes, followrequst) through PUT and using UUID
# Therefore there are only very few API views can be tested with a CURL command
# To see the detailed APIView test, please refer to testViews.py 

class CURLAPIListAuthorsTests(TestCase):
    # Setup client, a dummy broswer used for testing
    def setUp(self):
        # Create a server, save it
        new_server = Server.objects.create(serverAddress="http://127.0.0.1:8000",serverKey="516e5c3d636f46228edb8f09b9613d5b4b166816", isLocalServer=True)
        new_server.save()

        # Create an user
        User.objects.create_superuser(username='test',email='test@gmail.com', password='password')
        self.user=User.objects.get(username='test')

        # Setup CurlClient to test CURL commands
        self.client=CurlClient()

        # Login for the user
        self.client.login(username='test', password='password')

    
    def testGETListAuthorsSuccess(self):
        """
        Test GET method for API with endpoint: /api/authors/
        """
        # Since django-test-curl doesn't allow to send PUT request and we use PUT to create authors, we can only test with no authors (empty)

        # Sending the GET request
        response = self.client.curl("""
          curl -X 'get' \
            'https://socialdistcmput404.herokuapp.com/api/authors/' \
            -H 'accept: application/json' \
            -H 'X-CSRFToken: Q0JArUPzBgk4WgNhOWcjlBRFE3cqhKivGQSw9TI52L9RngsxF4pzCJKEcVlh4cd9'
        """)

        # Test status code
        self.assertEqual(response.status_code, 200)

        # Test data
        self.assertEqual(response.data['type'], 'authors')
        self.assertEqual(response.data['items'], list())

    def testGETListAuthorsFailure(self):
        """
        Test GET method for API with an invalid endpoint: /api/author/ 
        """
        # Sending the GET request
        response = self.client.curl("""
          curl -X 'get' \
            'https://socialdistcmput404.herokuapp.com/api/author/' \
            -H 'accept: application/json' \
        """)

        # Test status code
        self.assertEqual(response.status_code, 404)