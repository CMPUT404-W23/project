# MIT License

# Copyright (c) 2023 Warren Lim

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

from .serializers import AuthorSerializer
from .models import Comment, Author, Like, Post

def construct_author_object(author_data):
    returnDict = dict(author_data)
    returnDict["type"] = "author"
    returnDict["url"] = returnDict["id"]
    return returnDict

def construct_list_of_authors(author_list_data):
    returnList = []
    for author_serial in author_list_data:
            returnList.append(construct_author_object(author_serial))
    authorListDict = {}
    authorListDict["type"] = "authors"
    authorListDict["items"] = returnList
    return authorListDict

def construct_post_object(post_data, author):
    postDict = dict(post_data)
    postDict["type"] = "post"
    serialzer = AuthorSerializer(author) 
    postDict["author"] = construct_author_object(serialzer.data)
    postDict["count"] = len(Comment.objects.filter(parentPost=postDict["id"]))
    postDict["comments"] = postDict["id"] + "/comments/"
    return postDict

def construct_list_of_posts(post_list_data, author):
    postList = []
    for post_serial in post_list_data:
        postList.append(construct_post_object(post_serial, author))
    postListDict = {}
    postListDict["type"] = "posts"
    postListDict["items"] = postList
    return postListDict

def construct_list_of_all_posts(author_post_list_data_pair):
    return {
        "type": "posts",
        "items": [[construct_post_object(post_serial, author) for post_serial in post_list_data] for author, post_list_data in author_post_list_data_pair],
    }
    

def construct_comment_object(comment_data, author):
    commentDict = dict(comment_data)
    author_serialzer = AuthorSerializer(author)
    commentDict["type"] = "comment"
    commentDict["author"] = construct_author_object(author_serialzer.data)
    return commentDict

def construct_list_of_comments(comment_list_data, author, post):
    commentList = []
    for comment_serial in comment_list_data:
        commentAuthor = Author.objects.get(pk=comment_serial["author"])
        commentList.append(construct_comment_object(comment_serial, commentAuthor))
    commentListDict = {}
    commentListDict["type"] = "comments"
    commentListDict["items"] = commentList
    commentListDict["post"] = post.id
    commentListDict["id"] = post.id + "/comments/"
    return commentListDict

def construct_like_object(like_data, parentObject, author):
    likeDict = dict(like_data)
    author_serialzer = AuthorSerializer(author)
    likeDict["author"] = construct_author_object(author_serialzer.data)
    likeDict["object"] = parentObject
    return likeDict

def construct_list_of_likes(like_list_data, parentObjectID):
    likeList = []
    for like_serial in like_list_data:
        likeAuthor = Author.objects.get(pk=like_serial["author"])
        likeList.append(construct_like_object(like_serial, parentObjectID, likeAuthor))
    likeListDict = {}
    likeListDict["type"] = "likes"
    likeListDict["items"] = likeList
    return likeListDict

def construct_list_of_liked(liked_list_data, author):
    likeList = []
    for like_serial in liked_list_data:
        like = Like.objects.get(pk=like_serial["id"])        
        if like.likeType == "Post":
            if like.parentPost.visibility != "VISIBLE":
                continue
            likeList.append(construct_like_object(like_serial, like.parentPost.id, author))
        else: 
            if like.parentComment.parentPost.visibility != "VISIBLE":
                continue
            likeList.append(construct_like_object(like_serial, like.parentComment.id, author))
    likeListDict = {}
    likeListDict["type"] = "liked"
    likeListDict["items"] = likeList
    return likeListDict

def construct_list_of_followers(follower_list_data):
    authorList = []
    for author_serial in follower_list_data:
        authorList.append(construct_author_object(author_serial))
    followerListDict = {}
    followerListDict["type"] = "followers"
    followerListDict["items"] = authorList
    return followerListDict

def construct_follow_request_object(follow_request_data, author, actor):
    # summary is already in the data
    followRequestDict=dict(follow_request_data)
    author_serialzer = AuthorSerializer(author)
    actor_serializer=AuthorSerializer(actor)
    followRequestDict["type"]="Follow"
    # get the object from follower_request
    followRequestDict["actor"]=construct_author_object(actor_serializer.data)
    followRequestDict["object"]=construct_author_object(author_serialzer.data)
    return followRequestDict
