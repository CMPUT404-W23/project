import json, datetime
from django.utils.timezone import make_aware
from rest_framework import status
from ..serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikeSerializer, ServerSerializer, InboxSerializer
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Author, Post, Comment, Like, Server, Inbox, UserFollowing, FollowRequest
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# BACK-END tests for models

HOST="https://socialdistcmput404.herokuapp.com/"

# Create your tests for models here.
# AUTHOR MODEL: Fully Test
class AuthorModelTests(TestCase):
    # Setup author profiles
    def setUp(self):
        Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        Author.objects.create(id="http://127.0.0.1:8000/authors/test2", host="http://127.0.0.1:8000/", displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg")

    # Test author model to ensure its fields exist
    def testOneAuthor(self):
        # retrieve setted up author
        author=Author.objects.filter(id="http://127.0.0.1:8000/authors/test1")
        authorDict=author.values()
        
        self.assertEqual(authorDict[0]["host"],"http://127.0.0.1:8000/")
        self.assertEqual(authorDict[0]["displayName"],"tester1")
        self.assertEqual(authorDict[0]["github"],"http://github.com/test1")
        self.assertEqual(authorDict[0]["profileImage"],"https://i.imgur.com/test1.jpeg")

    # test list of author models (more than 1 author), and check their fields
    def testMutlipleAuthors(self):
        # Get the authors and check their values
        author=Author.objects.all().filter(host="http://127.0.0.1:8000/")
        authorDict=author.values()

        self.assertEqual(authorDict.count(),2)

        self.assertEqual(authorDict[0]["id"],"http://127.0.0.1:8000/authors/test1")
        self.assertEqual(authorDict[0]["displayName"],"tester1")
        self.assertEqual(authorDict[0]["github"],"http://github.com/test1")
        self.assertEqual(authorDict[0]["profileImage"],"https://i.imgur.com/test1.jpeg")

        self.assertEqual(authorDict[1]["id"],"http://127.0.0.1:8000/authors/test2")
        self.assertEqual(authorDict[1]["displayName"],"tester2")
        self.assertEqual(authorDict[1]["github"],"http://github.com/test2")
        self.assertEqual(authorDict[1]["profileImage"],"https://i.imgur.com/test2.jpeg")

    # test object model fields can be updated
    def testUpdateAuthorFields(self):
        author=Author.objects.filter(id="http://127.0.0.1:8000/authors/test1")
        authorDict=author.values()

        # check field value before
        self.assertEqual(authorDict[0]["github"],"http://github.com/test1")
        
        # check field value after update
        author.update(github="http://github.com/test3")
        self.assertEqual(authorDict[0]["github"],"http://github.com/test3")

    def testDeleteAuthor(self):
        # get 2 authors
        author=Author.objects.all().filter(host="http://127.0.0.1:8000/")

        authorDict=author.values()
        # check there are 2 authors
        self.assertEqual(authorDict.count(),2)
        # delete the second one
        Author.objects.get(id="http://127.0.0.1:8000/authors/test2").delete()
        authorDict=author.values()
        # Only 1 author left
        self.assertEqual(authorDict.count(),1)

#  TODO: update server test case due to updates in server

# Testing Server model
class ServerModelTests(TestCase):
    def setUp(self):
        author=Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        Server.objects.create(serverAddress="http://127.0.0.1:8000/authors/", serverKey="1", isLocalServer=True)

    # Get the server object, check its values
    def testGetServerFields(self):
        server=Server.objects.filter(serverKey="1")
        serverDict=server.values()
        
        self.assertEqual(serverDict[0]["serverAddress"],"http://127.0.0.1:8000/authors/")
        self.assertEqual(serverDict[0]["serverKey"],"1")
        self.assertEqual(serverDict[0]["isLocalServer"],True)


    # Get a server object, update its fields (server address), then check the updated fields
    def testUpdateServerField(self):
        server=Server.objects.filter(serverKey="1")
        serverDict=server.values()

        # check field value before
        self.assertEqual(serverDict[0]["serverAddress"],"http://127.0.0.1:8000/authors/")
        server.update(serverAddress="https://socialdistcmput404.herokuapp.com/")
        
        # check field value after update
        self.assertEqual(serverDict[0]["serverAddress"],"https://socialdistcmput404.herokuapp.com/")

    # Get the server object, check count, delete the object
    def testDeleteServer(self):
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
        author1=Author.objects.get(id=HOST+"authors/test1")
        userFollowing=UserFollowing.objects.filter(user_id=author1)
        userFollowingDict=userFollowing.values()

        self.assertEqual(userFollowingDict[0]["user_id_id"],HOST+"authors/test1")
        self.assertEqual(userFollowingDict[0]["following_user_id_id"],HOST+"authors/test2")

    # Get the UserFollowing object, update its fields, then check the updated fields
    def testUpdateUserFollowingFields(self):
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
        # user1=User.objects.create_user(username="test1", email="test1@gmail.com", password='1')
        # user2=User.objects.create_user(username="test2", email="test2@gmail.com", password='2')

        # Create subsquent authors
        author1=Author.objects.create(id=HOST+"authors/test1", host=HOST, displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        author2=Author.objects.create(id=HOST+"authors/test2", host=HOST, displayName="tester2", github="http://github.com/test2", profileImage="https://i.imgur.com/test2.jpeg")

        setUpDate=datetime.datetime.now()

        FollowRequest.objects.create(sender=author1,target=author2, date=setUpDate)
    
    # Get the FollowRequest object, check its values
    def testGetFollowRequestFields(self):
        author1=Author.objects.get(id=HOST+"authors/test1")
        followRequest=FollowRequest.objects.filter(sender=author1)
        followRequestDict=followRequest.values()

        self.assertEqual(followRequestDict[0]["sender_id"],HOST+"authors/test1")  
        self.assertEqual(followRequestDict[0]["target_id"],HOST+"authors/test2") 
        self.assertLess(followRequestDict[0]["date"],datetime.datetime.today())

"""
    # Get the FollowRequest object, update its fields, then check the updated fields
    def testUpdateFollowRequestFields(self):
        user1=User.objects.get(username="test1")
        followRequest=FollowRequest.objects.filter(sender=user1)
        newSetUpDate=datetime.date(2023, 3, 1)

        # check field value before
        followRequestDict=followRequest.values()
        self.assertEqual(followRequestDict[0]["date"],datetime.datetime(2023, 3, 5, 0, 0, tzinfo=datetime.timezone.utc))

        # check field value after update
        followRequest.update(date=newSetUpDate)
        self.assertEqual(followRequestDict[0]["date"],datetime.datetime(2023, 3, 1, 0, 0, tzinfo=datetime.timezone.utc))

    # Get UserFollowing object, delete and check count
    def testDeleteFollowRequest(self):

        user1=User.objects.get(username="test1")
        followRequest=FollowRequest.objects.filter(sender=user1)

        # Check count = 1
        followRequestDict=followRequest.values()
        self.assertEqual(followRequestDict.count(),1)

        # Check count after delete = 0
        FollowRequest.objects.get(sender=user1).delete()
        self.assertEqual(followRequestDict.count(),0)

# Testing Post model
class PostModelTests(TestCase):
    # Create/ POST Post model
    def setUp(self):
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        Post.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=author1, categories=["web","tutorial"], published=datetime.date(2023, 3, 5), visibility="VISIBLE", unlisted=False)

    # Get the Post object, check its values
    def testGetPostFields(self):
        author1=Author.objects.get(id="http://127.0.0.1:8000/authors/test1")
        post=Post.objects.filter(author=author1)
        postDict=post.values()

        expectedDict={'published': datetime.datetime(2023, 3, 5, 0, 0, tzinfo=datetime.timezone.utc), 'id': 'http://127.0.0.1:8000/authors/test1/posts/1', 'title': 'test title', 'source': 'http://test.com', 'origin': 'http://whereitcamefrom.com/posts/zzzzz', 'description': 'test description', 'contentType': 'text/plain', 'content': 'test content', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'categories': "['web', 'tutorial']", 'visibility': 'VISIBLE', 'unlisted': False}
        self.assertEqual(postDict[0], expectedDict)

    # Get the Post object, update its fields, then check the updated fields
    def testUpdatePostFields(self):
        author1=Author.objects.get(id="http://127.0.0.1:8000/authors/test1")
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
        author1=Author.objects.get(id="http://127.0.0.1:8000/authors/test1")
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
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        post1=Post.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=author1, categories=["web","tutorial"], published=datetime.date(2023, 3, 5), visibility="VISIBLE", unlisted=False)
        
        # Create author and post before creating comment 
        # Create 2 commment objects (1 for regular comment, 1 for post comment)
        comment=Comment.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/1", author=author1, content="test content 1", contentType="text/plain", published=datetime.date(2023, 3, 5), parentPost=post1)
        commentFromPost=Comment.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/", author=author1, content="test content 2", contentType="text/plain", published=datetime.date(2023, 3, 3), parentPost=post1)

    # Get both Comment objects, check their values
    def testGetCommentFields(self):
        author1=Author.objects.get(id="http://127.0.0.1:8000/authors/test1")
        post1=Post.objects.get(id="http://127.0.0.1:8000/authors/test1/posts/1")

        # check regular comment
        comment=Comment.objects.filter(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/1")
        commentDict=comment.values()
        expectedData={'published': datetime.datetime(2023, 3, 5, 0, 0, tzinfo=datetime.timezone.utc), 'id': 'http://127.0.0.1:8000/authors/test1/posts/1/comments/1', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'content': 'test content 1', 'contentType': 'text/plain', 'parentPost_id': 'http://127.0.0.1:8000/authors/test1/posts/1'}

        self.assertEqual(commentDict[0],expectedData)

        # check post comment
        commentFromPost=Comment.objects.filter(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/")
        commentFromPostDict=commentFromPost.values()

        expectedDataFromPost={'published': datetime.datetime(2023, 3, 3, 0, 0, tzinfo=datetime.timezone.utc), 'id': 'http://127.0.0.1:8000/authors/test1/posts/1/comments/', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'content': 'test content 2', 'contentType': 'text/plain', 'parentPost_id': 'http://127.0.0.1:8000/authors/test1/posts/1'}
        
        self.assertEqual(commentFromPostDict[0],expectedDataFromPost)
    
    # Get the Comment object, update its fields, then check the updated fields
    def testUpdateCommentFields(self):
        comment=Comment.objects.filter(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/1")
        commentDict=comment.values()

        # For regular comment
        # check field value before
        self.assertEqual(commentDict[0]["content"], "test content 1")

        # check field value after update
        comment.update(content="new test content 1")
        self.assertEqual(commentDict[0]["content"], "new test content 1")

        # For post comment
        # check field value before
        commentFromPost=Comment.objects.filter(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/")
        commentFromPostDict=commentFromPost.values()
        self.assertEqual(commentFromPostDict[0]["content"], "test content 2")

        # check field value after update
        commentFromPost.update(content="new test content 2")
        self.assertEqual(commentFromPostDict[0]["content"], "new test content 2")

    # Get Comment object, delete and check count
    def testDeleteComment(self):
        # For regular comment
        # Check count = 1
        comment=Comment.objects.filter(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/1")
        commentDict=comment.values()
        self.assertEqual(commentDict.count(),1)

        # Check count after delete = 0
        Comment.objects.get(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/1").delete()
        self.assertEqual(commentDict.count(),0)

        # For post comment
        # Check count = 1
        commentFromPost=Comment.objects.filter(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/")
        commentFromPostDict=commentFromPost.values()
        self.assertEqual(commentFromPostDict.count(),1)

        # Check count after delete = 0
        Comment.objects.get(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/").delete()
        self.assertEqual(commentFromPostDict.count(),0)

# Testing Like model
class LikeModelTests(TestCase):
    # Create/ POST Like model
    def setUp(self):
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        post1=Post.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1", title="test title", source="http://test.com", origin="http://whereitcamefrom.com/posts/zzzzz", description="test description", contentType="text/plain", content="test content", author=author1, categories=["web","tutorial"], published=datetime.date(2023, 3, 5), visibility="VISIBLE", unlisted=False)
        comment1=Comment.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1/comments/1", author=author1, content="test content 1", contentType="text/plain", published=datetime.date(2023, 3, 5), parentPost=post1)

        like=Like.objects.create(summary="I like you", likeType="post", author=author1, parentPost=post1, parentComment=comment1, published=datetime.date(2023, 3, 5))

    # Get the Like object, check its values
    def testGetLikeFields(self):
        like=Like.objects.filter(summary="I like you")
        likeDict=like.values()
        expectedData={'published': datetime.datetime(2023, 3, 5, 0, 0, tzinfo=datetime.timezone.utc), 'id': '', 'summary': 'I like you', 'likeType': 'post', 'author_id': 'http://127.0.0.1:8000/authors/test1', 'parentPost_id': 'http://127.0.0.1:8000/authors/test1/posts/1', 'parentComment_id': 'http://127.0.0.1:8000/authors/test1/posts/1/comments/1'}

        self.assertEqual(likeDict[0],expectedData)

    # NO PUT/update to test since like can't be updated

    # Get Like object, delete and check count
    def testDeleteLike(self):
        like=Like.objects.filter(summary="I like you")
        likeDict=like.values()

        # Check count = 1
        self.assertEqual(likeDict.count(),1)

        # Check count after delete = 0
        Like.objects.get(summary="I like you").delete()
        self.assertEqual(likeDict.count(),0)

# Testing Inbox model
class InboxModelTests(TestCase):
    # Create/ POST inbox model
    def setUp(self):
        author1=Author.objects.create(id="http://127.0.0.1:8000/authors/test1", host="http://127.0.0.1:8000/", displayName="tester1", github="http://github.com/test1", profileImage="https://i.imgur.com/test1.jpeg")
        post1=Post.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/1", title="test title1", source="http://test.com", origin="http://testorigin1.com/posts/", description="test description 1", contentType="text/plain", content="test content 1", author=author1, categories=["web","tutorial"], published=datetime.date(2023, 3, 5), visibility="VISIBLE", unlisted=False)
        post2=Post.objects.create(id="http://127.0.0.1:8000/authors/test1/posts/2", title="test title2", source="http://test.com", origin="http://testorigin2.com/posts/", description="test description 2", contentType="text/plain", content="test content 2", author=author1, categories=["web","tutorial"], published=datetime.date(2023, 3, 6), visibility="PRIVATE", unlisted=True)

        # add the Posts using .add(TBA)
        inbox=Inbox.objects.create(inboxID="http://127.0.0.1:8000/authors/test1/inbox/1", author=author1)
        inbox.posts.add(post1, post2)

    # Get the Post object, check its values
    def testGetInboxFields(self):
        author1=Author.objects.get(id="http://127.0.0.1:8000/authors/test1")
        inbox=Inbox.objects.filter(author=author1)
        inboxDict=inbox.values()

        expectedData={'inboxID': 'http://127.0.0.1:8000/authors/test1/inbox/1', 'author_id': 'http://127.0.0.1:8000/authors/test1'}
        self.assertEqual(inboxDict[0],expectedData)

    # NO PUT/update to test since like can't be updated

    # Get Inbox object, delete and check count
    def testDeleteInbox(self):
        author1=Author.objects.get(id="http://127.0.0.1:8000/authors/test1")
        inbox=Inbox.objects.filter(author=author1)
        inboxDict=inbox.values()

        # Check count = 1
        self.assertEqual(inboxDict.count(),1)

        # Check count after delete = 0
        Inbox.objects.get(author=author1).delete()
        self.assertEqual(inboxDict.count(),0)

    # MORE TESTS LATER FOR API VIEWS (TBA)
"""