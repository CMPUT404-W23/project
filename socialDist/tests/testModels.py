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
from rest_framework import status
from ..serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import make_aware
import datetime
import pytz

# for serializer
import uuid

# Local BACK-END tests for models, Test CRUD (Create, Retrieve, Update, Delete) for each model
# TO RUN THIS FILE TYPE COMMAND: python manage.py test socialDist.tests.testModels

# using global localhost variable
HOST="http://127.0.0.1:8000/"

utc=pytz.UTC

# AUTHOR MODEL: Fully Test
class AuthorModelTests(TestCase):
    # Setup 2 author profiles
    def setUp(self):
        Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        Author.objects.create(id=HOST+"authors/test2", host=HOST, displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg")

    # Test author model to ensure its fields exist
    def testOneAuthor(self):
        """
        Get one author object and test whether the fields are valid or not
        """
        # retrieve setted up author
        author=Author.objects.filter(id=HOST+"authors/test1")
        authorDict=author.values()
        
        self.assertEqual(authorDict[0]["host"],HOST)
        self.assertEqual(authorDict[0]["displayName"],"tester1")
        self.assertEqual(authorDict[0]["github"],"http://github.com/test1")
        self.assertEqual(authorDict[0]["profileImage"],"https://i.imgur.com/test1.jpeg")

    # test list of author models (more than 1 author), and check their fields
    def testMutlipleAuthors(self):
        """
        Get multple author objects and test whether their fields are valid or not
        """
        # Get the authors and check their values
        author=Author.objects.all().filter(host=HOST)
        authorDict=author.values()

        self.assertEqual(authorDict.count(),2)

        self.assertEqual(authorDict[0]["id"],HOST+"authors/test1")
        self.assertEqual(authorDict[0]["displayName"],"tester1")
        self.assertEqual(authorDict[0]["github"],"http://github.com/test1")
        self.assertEqual(authorDict[0]["profileImage"],"https://i.imgur.com/test1.jpeg")

        self.assertEqual(authorDict[1]["id"],HOST+"authors/test2")
        self.assertEqual(authorDict[1]["displayName"],"tester2")
        self.assertEqual(authorDict[1]["github"],"http://github.com/test2")
        self.assertEqual(authorDict[1]["profileImage"],"https://i.imgur.com/test2.jpeg")

    # test object model fields can be updated
    def testUpdateAuthorFields(self):
        """
        Get one author object and update its fields, test whether the fields are valid or not
        """
        author=Author.objects.filter(id=HOST+"authors/test1")
        authorDict=author.values()

        # check field value before
        self.assertEqual(authorDict[0]["github"],"http://github.com/test1")
        
        # check field value after update
        author.update(github="http://github.com/test3")
        self.assertEqual(authorDict[0]["github"],"http://github.com/test3")

    def testDeleteAuthor(self):
        """
        Get two author objects and delete one of them, test whether there are only 1 author object left
        """
        # get 2 authors
        author=Author.objects.all().filter(host=HOST)

        authorDict=author.values()
        # check there are 2 authors
        self.assertEqual(authorDict.count(),2)
        # delete the second one
        Author.objects.get(id=HOST+"authors/test2").delete()
        authorDict=author.values()
        # Only 1 author left
        self.assertEqual(authorDict.count(),1)

# Testing Server model
class ServerModelTests(TestCase):
    # Setup an author model for future testing
    def setUp(self):
        author=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        Server.objects.create(serverAddress=HOST+"authors/", serverKey="1", isLocalServer=True)

    # Get the server object, check its values

    def testGetServerFields(self):
        """
        Get the server object and test whether the fields are valid or not
        """
        server=Server.objects.filter(serverKey="1")
        serverDict=server.values()
        
        self.assertEqual(serverDict[0]["serverAddress"],HOST+"authors/")
        self.assertEqual(serverDict[0]["serverKey"],"1")
        self.assertEqual(serverDict[0]["isLocalServer"],True)


    # Get a server object, update its fields (server address), then check the updated fields
    def testUpdateServerField(self):
        """
        Get the server object and update the author's fields, test whether the fields are valid or not
        """
        server=Server.objects.filter(serverKey="1")
        serverDict=server.values()

        # check field value before
        self.assertEqual(serverDict[0]["serverAddress"],HOST+"authors/")
        server.update(serverAddress="https://socialdistcmput404.herokuapp.com/")
        
        # check field value after update
        self.assertEqual(serverDict[0]["serverAddress"],"https://socialdistcmput404.herokuapp.com/")

    # Get the server object, check count, delete the object
    def testDeleteServer(self):
        """
        Get server object and delete it, test whether there are any servers objects left
        """
        server=Server.objects.filter(serverKey="1")

        serverDict=server.values()
        # Count of server = 1
        self.assertEqual(serverDict.count(),1)

        Server.objects.get(serverKey="1").delete()
        # Count of server after delete = 0
        self.assertEqual(serverDict.count(),0)


# Testing UserFollowing model: DONE
class UserFollowingModelTests(TestCase):
    # Create/ POST UserFollowing model
    def setUp(self):
        author1=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id=HOST+"authors/test2", host=HOST, displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg")
        UserFollowing.objects.create(user_id=author1, following_user_id=author2)

    # Get the UserFollowing object, check its values
    def testGetUserFollowingFields(self):
        """
        Get one UserFollowing object and test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        userFollowing=UserFollowing.objects.filter(user_id=author1)
        userFollowingDict=userFollowing.values()

        self.assertEqual(userFollowingDict[0]["user_id_id"],HOST+"authors/test1")
        self.assertEqual(userFollowingDict[0]["following_user_id_id"],HOST+"authors/test2")

    # Get the UserFollowing object, update its fields, then check the updated fields
    def testUpdateUserFollowingFields(self):
        """
        Get one UserFollowing object and update its fields, test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        author3=Author.objects.create(id=HOST+"authors/test3", host=HOST, displayName="tester3", github="http://github.com/test3", profileImage="https://i.imgur.com/test3.jpeg")
        userFollowing=UserFollowing.objects.filter(user_id=author1)
        userFollowingDict=userFollowing.values()
        # check field value before
        self.assertEqual(userFollowingDict[0]["following_user_id_id"],HOST+"authors/test2")

        # check field value after update
        userFollowing.update(following_user_id=author3)
        self.assertEqual(userFollowingDict[0]["following_user_id_id"],HOST+"authors/test3")

    # Get UserFollowing object, delete and check count
    def testDeleteUserFollowing(self):
        """
        Get UserFollowing object and delete it, test whether there are any user following objects left
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        userFollowing=UserFollowing.objects.filter()

        # Check count = 1
        userFollowingDict=userFollowing.values()
        self.assertEqual(userFollowingDict.count(),1)

        # Check count after delete = 0
        UserFollowing.objects.get(user_id=author1).delete()
        self.assertEqual(userFollowingDict.count(),0)

# Testing FollowRequest model
class FollowRequestModelTests(TestCase):
    # Create/ POST FollowRequest model
    def setUp(self):
        # Create subsquent authors
        author1=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id=HOST+"authors/test2", host=HOST, displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg")

        setUpDate=datetime.datetime.now(tz=timezone.utc)
        FollowRequest.objects.create(sender=author1,target=author2, date=setUpDate)
    
    # Get the FollowRequest object, check its values
    def testGetFollowRequestFields(self):
        """
        Get one FollowRequest object and test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        followRequest=FollowRequest.objects.filter(sender=author1)
        followRequestDict=followRequest.values()

        self.assertEqual(followRequestDict[0]["sender_id"],HOST+"authors/test1")  
        self.assertEqual(followRequestDict[0]["target_id"],HOST+"authors/test2") 
        # check is date within today
        self.assertLess(followRequestDict[0]["date"],utc.localize(datetime.datetime.today()))

    # Get the FollowRequest object, update its fields, then check the updated fields
    def testUpdateFollowRequestFields(self):
        """
        Get one FollowRequest object and update its fields, test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        followRequest=FollowRequest.objects.filter(sender=author1)
        
        # check field value before, check is date within today
        followRequestDict=followRequest.values()
        self.assertLess(followRequestDict[0]["date"],utc.localize(datetime.datetime.today()))
        # update with a new now time
        newSetUpDate=datetime.datetime.now(tz=timezone.utc)

        # check field value after update
        followRequest.update(date=newSetUpDate)
        self.assertLess(followRequestDict[0]["date"],utc.localize(datetime.datetime.today()))

    # Get UserFollowing object, delete and check count
    def testDeleteFollowRequest(self):
        """
        Get UserFollowing object and delete it, test whether there are any following request objects left
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        followRequest=FollowRequest.objects.filter(sender=author1)

        # Check count = 1
        followRequestDict=followRequest.values()
        self.assertEqual(followRequestDict.count(),1)

        # Check count after delete = 0
        FollowRequest.objects.get(sender=author1).delete()
        self.assertEqual(followRequestDict.count(),0)


# Testing Post model
class PostModelTests(TestCase):
    # Create/ POST Post model
    def setUp(self):
        testAuthor=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        Post.objects.create(id=HOST+"authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=testAuthor, categories=["web","tutorial"], published=datetime.datetime.now(tz=timezone.utc), visibility="VISIBLE", unlisted=False)

    # Get the Post object, check its values
    def testGetPostFields(self):
        """
        Get one post object and test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        post=Post.objects.filter(author=author1)
        postDict=post.values()

        testDict=postDict[0]
        # test data and published time (indepdent)
        testPostDate=testDict.pop('published')

        # Test Date: see is post built within today
        self.assertLess(testPostDate,utc.localize(datetime.datetime.today()))

        # Test rest of the data
        expectedDict={'id': 'http://127.0.0.1:8000/authors/test1/posts/1', 'title': 'test title', 'source': 'http://test.com', 'origin': 'http://whereitcamefrom.com/posts/zzzzz', 'description': 'test description', 'contentType': 'text/plain', 'content': 'test content', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'categories': "['web', 'tutorial']", 'visibility': 'VISIBLE', 'unlisted': False}
        self.assertEqual(testDict, expectedDict)

    # Get the Post object, update its fields, then check the updated fields
    def testUpdatePostFields(self):
        """
        Get one post object and update its fields, test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        post=Post.objects.filter(author=author1)
        postDict=post.values()

        # check field value before
        self.assertEqual(postDict[0]["description"], "test description")
        self.assertEqual(postDict[0]["content"], "test content")
        post.update(description="new test description", content="new test content")

        # check field value after update
        self.assertEqual(postDict[0]["description"], "new test description")
        self.assertEqual(postDict[0]["content"], "new test content")

    # Get UserFollowing object, delete and check count
    def testDeletePostFields(self):
        """
        Get post object and delete it, test whether there are any post objects left
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        post=Post.objects.filter(author=author1)

        # Check count = 1
        postDict=post.values()
        self.assertEqual(postDict.count(),1)

        # Check count after delete = 0
        Post.objects.get(author=author1).delete()
        self.assertEqual(postDict.count(),0)

# Testing Comment model
class CommentModelTests(TestCase):
    # Create/ POST Comment model
    def setUp(self):
        author1=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        post1=Post.objects.create(id=HOST+"authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=author1, categories=["web","tutorial"], published=datetime.datetime.now(tz=timezone.utc), visibility="VISIBLE", unlisted=False)
        
        # Create author and post before creating comment 
        # Create 2 commment objects (1 for regular comment, 1 for post comment)
        comment=Comment.objects.create(id=HOST+"authors/test1/posts/1/comments/1", author=author1, comment="test comment 1", contentType="text/plain", published=datetime.datetime.now(tz=timezone.utc), parentPost=post1)
        commentFromPost=Comment.objects.create(id=HOST+"authors/test1/posts/1/comments/", author=author1, comment="test comment 2", contentType="text/plain", published=datetime.datetime.now(tz=timezone.utc), parentPost=post1)

    # Get both Comment objects, check their values
    def testGetCommentFields(self):
        """
        Get two comment objects (1 post comment, 1 regular comment) and test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        post1=Post.objects.get(id=HOST+"authors/test1/posts/1")

        # check regular comment
        comment=Comment.objects.filter(id=HOST+"authors/test1/posts/1/comments/1")
        commentDict=comment.values()

        testDict=commentDict[0]
        # test data and published time (indepdent)
        testCommentDate=testDict.pop('published')

        # Test Date: see is post built within today
        self.assertLess(testCommentDate,utc.localize(datetime.datetime.today()))
        
        # Test rest of data
        expectedData={'id': 'http://127.0.0.1:8000/authors/test1/posts/1/comments/1', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'comment': 'test comment 1', 'contentType': 'text/plain', 'parentPost_id': 'http://127.0.0.1:8000/authors/test1/posts/1'}
        self.assertEqual(testDict,expectedData)

        # Part 2
        # check post comment
        commentFromPost=Comment.objects.filter(id=HOST+"authors/test1/posts/1/comments/")
        commentFromPostDict=commentFromPost.values()

        test2Dict=commentDict[0]
        # test data and published time (indepdent)
        testCommentDate=test2Dict.pop('published')

        # Test Date: see is post built within today
        self.assertLess(testCommentDate,utc.localize(datetime.datetime.today()))
        
        # Test rest of data
        expectedData={'id': 'http://127.0.0.1:8000/authors/test1/posts/1/comments/1', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'comment': 'test comment 1', 'contentType': 'text/plain', 'parentPost_id': 'http://127.0.0.1:8000/authors/test1/posts/1'}
        self.assertEqual(test2Dict,expectedData)
  
    # Get the Comment object, update its fields, then check the updated fields
    def testUpdateCommentFields(self):
        """
        Get two comment objects and test whether their fields are valid or not
        """
        comment=Comment.objects.filter(id=HOST+"authors/test1/posts/1/comments/1")
        commentDict=comment.values()

        # For regular comment
        # check field value before
        self.assertEqual(commentDict[0]["comment"], "test comment 1")

        # check field value after update
        comment.update(comment="new test comment 1")
        self.assertEqual(commentDict[0]["comment"], "new test comment 1")

        # For post comment
        # check field value before
        commentFromPost=Comment.objects.filter(id=HOST+"authors/test1/posts/1/comments/")
        commentFromPostDict=commentFromPost.values()
        self.assertEqual(commentFromPostDict[0]["comment"], "test comment 2")

        # check field value after update
        commentFromPost.update(comment="new test comment 2")
        self.assertEqual(commentFromPostDict[0]["comment"], "new test comment 2")

    # Get Comment object, delete and check count
    def testDeleteComment(self):
        """
        Get both comment object and delete one of them, test whether there are any comment objects left
        """
        # For regular comment
        # Check count = 1
        comment=Comment.objects.filter(id=HOST+"authors/test1/posts/1/comments/1")
        commentDict=comment.values()
        self.assertEqual(commentDict.count(),1)

        # Check count after delete = 0
        Comment.objects.get(id=HOST+"authors/test1/posts/1/comments/1").delete()
        self.assertEqual(commentDict.count(),0)

        # For post comment
        # Check count = 1
        commentFromPost=Comment.objects.filter(id=HOST+"authors/test1/posts/1/comments/")
        commentFromPostDict=commentFromPost.values()
        self.assertEqual(commentFromPostDict.count(),1)

        # Check count after delete = 0
        Comment.objects.get(id=HOST+"authors/test1/posts/1/comments/").delete()
        self.assertEqual(commentFromPostDict.count(),0)

# Testing Like model
class LikeModelTests(TestCase):
    # Create/ POST Like model
    def setUp(self):
        author1=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        post1=Post.objects.create(id=HOST+"authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=author1, categories=["web","tutorial"], published=datetime.datetime.now(tz=timezone.utc), visibility="VISIBLE", unlisted=False)
        comment1=Comment.objects.create(id=HOST+"authors/test1/posts/1/comments/1", author=author1, comment="test comment 1", contentType="text/plain", published=datetime.datetime.now(tz=timezone.utc), parentPost=post1)
        like=Like.objects.create(id=HOST+"authors/test1/posts/1/comments/1/likes/1",likeType="post", author=author1, parentPost=post1, parentComment=comment1, published=datetime.datetime.now(tz=timezone.utc))

    # Get the Like object, check its values
    def testGetLikeFields(self):
        """
        Get one like object and test whether the fields are valid or not
        """
        like=Like.objects.filter(id=HOST+"authors/test1/posts/1/comments/1/likes/1")
        likeDict=like.values()
        testDict=likeDict[0]

        # test data and published time (indepdent)
        testLikeDate=testDict.pop('published')

        # Test Date: see is post built within today
        self.assertLess(testLikeDate,utc.localize(datetime.datetime.today()))

        # Test rest of the data
        expectedData={'id': HOST+"authors/test1/posts/1/comments/1/likes/1", 'likeType': 'post', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'parentPost_id': 'http://127.0.0.1:8000/authors/test1/posts/1', 'parentComment_id': 'http://127.0.0.1:8000/authors/test1/posts/1/comments/1'}
        self.assertEqual(testDict,expectedData)

    # NO PUT/update to test since like can't be updated

    # Get Like object, delete and check count
    def testDeleteLike(self):
        """
        Get like object and delete it, test whether there are any like objects left
        """
        like=Like.objects.filter(id=HOST+"authors/test1/posts/1/comments/1/likes/1")
        likeDict=like.values()

        # Check count = 1
        self.assertEqual(likeDict.count(),1)

        # Check count after delete = 0
        Like.objects.get(id=HOST+"authors/test1/posts/1/comments/1/likes/1").delete()
        self.assertEqual(likeDict.count(),0)


# Testing Inbox model
class InboxModelTests(TestCase):
    # Create/ POST inbox model
    def setUp(self):
        author1=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id=HOST+"authors/test2", host=HOST, displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg")
        post1=Post.objects.create(id=HOST+"authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=author1, categories=["web","tutorial"], published=datetime.datetime.now(tz=timezone.utc), visibility="VISIBLE", unlisted=False)
        comment1=Comment.objects.create(id=HOST+"authors/test1/posts/1/comments/1", author=author1, comment="test comment 1", contentType="text/plain", published=datetime.datetime.now(tz=timezone.utc), parentPost=post1)
        like1=Like.objects.create(id=HOST+"authors/test1/posts/1/comments/1/likes/1",likeType="post", author=author1, parentPost=post1, parentComment=comment1, published=datetime.datetime.now(tz=timezone.utc))        

        setUpDate=datetime.datetime.now(tz=timezone.utc)
        fR1=FollowRequest.objects.create(sender=author1,target=author2, date=setUpDate)

        # add the Posts using .add(TBA)
        Inbox.objects.create(inboxID=HOST+"authors/test1/inbox/1", author=author1)

    # Get the Post object, check its values
    def testGetInboxFields(self):
        """
        Get one inbox object and test whether the fields are valid or not
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        inbox=Inbox.objects.filter(author=author1)
        inboxDict=inbox.values()

        expectedData={'inboxID': 'http://127.0.0.1:8000/authors/test1/inbox/1', 'author_id': 'http://127.0.0.1:8000/authors/test1'}
        self.assertEqual(inboxDict[0],expectedData)

    # NO PUT/update to test since like can't be updated (based on our open API)
    # Get Inbox object, delete and check count
    def testDeleteInbox(self):
        """
        Get inbox object and delete it, test whether there are any inbox objects left
        """
        author1=Author.objects.get(id=HOST+"authors/test1")
        inbox=Inbox.objects.filter(author=author1)
        inboxDict=inbox.values()

        # Check count = 1
        self.assertEqual(inboxDict.count(),1)

        # Check count after delete = 0
        Inbox.objects.get(author=author1).delete()
        self.assertEqual(inboxDict.count(),0)

# Bonus Tests: for serializer (author only)
class AuthorSerializerTests(TestCase):
    def setUp(self):
        self.authorAttributes={
            "id": HOST+"authors/test1",
            "host": HOST,
            "displayName": "sampleTestAuthor",
            "github": "https://github.com/testUser",
            "profileImage": "http://sampleUserImage.com/1.jpg",
        }
        testAuthor=Author.objects.create(**self.authorAttributes)
        self.AuthorSerializer=AuthorSerializer(instance=testAuthor)

    # Test to see are the serializer's field matched when creating through serializer
    def testSerializerFields(self):
        """
        create an author object through AuthorSerializer, test is object created and check its values
        """
        authorData=self.AuthorSerializer.data

        self.assertEqual(authorData["id"], HOST+"authors/test1")
        self.assertEqual(authorData["host"], HOST)
        self.assertEqual(authorData["displayName"], "sampleTestAuthor")
        self.assertEqual(authorData["github"], "https://github.com/testUser")
        self.assertEqual(authorData["profileImage"], "http://sampleUserImage.com/1.jpg")