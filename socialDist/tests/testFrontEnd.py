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
from ..serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User

# Front-end tests for pages
# Create your tests here.
class AccountsUITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='django404')
        self.author = Author.objects.create(id="https://socialdistcmput404.herokuapp.com/authors/139f2c94-d428-11ed-afa1-0242ac120002", host="http://127.0.0.1:8000/", displayName="testuser", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg", user_id=self.user.id)
        self.client.force_login(user=self.user)

    def test_login_page(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Log In')

    def test_signup_page(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertContains(response, 'Sign Up')
    
    def test_settings_page(self):
        url = reverse('settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        self.assertContains(response, 'Settings')
        self.assertContains(response, 'Your Account Information')
        self.assertContains(response, 'Edit Account Settings')
        self.assertContains(response, 'Save Changes')

    def test_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Home')

    def test_create_post_page(self):
        url = reverse('post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post.html')
        self.assertContains(response, 'Create a Post & Share it With Others!')
        self.assertContains(response, 'Post Type')
        self.assertContains(response, 'Post Type')
        self.assertContains(response, 'Content Type')
        self.assertContains(response, 'Content')
        self.assertContains(response, 'Description')
        self.assertContains(response, 'Content')
        self.assertContains(response, 'Categories')
        self.assertContains(response, 'Visibility')
        self.assertContains(response, 'Unlisted')
        self.assertContains(response, 'Post!')
    
    def test_own_profile_page(self):
        url = reverse('page_author', args=[self.author.id.split('/').pop()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "'s Profile")
        self.assertContains(response, "Connections")
        self.assertContains(response, "Inbox")
        self.assertContains(response, "Posts")
        self.assertContains(response, "Likes")
        self.assertContains(response, "Comments")
        self.assertContains(response, "Follow Requests")
    
    def test_others_profile_page(self):
        # Create a new author
        otherUser = User.objects.create_user(username='otherUser', password='django404')
        otherAuthor = Author.objects.create(id="https://socialdistcmput404.herokuapp.com/authors/139f2c94-d428-11ed-afa1-0242ac120003", host="http://127.0.0.1:8000/", displayName="otherUser", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg", user_id=otherUser.id)
        url = reverse('page_author', args=[otherAuthor.id.split('/').pop()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "'s Profile")
        self.assertContains(response, "Connections")
        # Should not be able to see the following on another author's profile
        self.assertNotContains(response, "Inbox")
        self.assertNotContains(response, "Posts")
        self.assertNotContains(response, "Likes")
        self.assertNotContains(response, "Comments")
        self.assertNotContains(response, "Follow Requests")
    
    def test_search_page(self):
        url = reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, "Search Any Accounts Here:")
            
    def test_profile_page(self):
        url = reverse('stream')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stream.html')
        self.assertContains(response, "My Posts")
        self.assertContains(response, "GitHub Activity Stream:")
