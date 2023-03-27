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

# This file contains functions that assists the API 

from .serializers import AuthorSerializer
from .models import Comment, Author, Like
from functools import reduce

# Constructs an author JSON object to be returned by the API
# Parameters:
#   author data - serialized form of Author object
# Returns: dict representing an author JSON object
def construct_author_object(author_data):
    returnDict = dict(author_data)
    returnDict["type"] = "author"
    returnDict["url"] = returnDict["id"]
    return returnDict

# Constructs a list of authors JSON object to be returned by the API
# Parameters:
#   author_list_data - list of serialized form of Author objects
# Returns: dict representing a list of authors JSON object
def construct_list_of_authors(author_list_data):
    returnList = []
    for author_serial in author_list_data:
            returnList.append(construct_author_object(author_serial))
    authorListDict = {}
    authorListDict["type"] = "authors"
    authorListDict["items"] = returnList
    return authorListDict

# Constructs a paginated list of authors JSON object to be returned by the API
# Parameters:
#   author_list_data - list of serialized form of Author objects
#   pageNum - page number, 1-indexed
#   sizeNum - number of elements on page
# Returns: dict representing a paginated list of authors JSON object
def construct_paginated_list_of_authors(author_list_data, pageNum, sizeNum):
    # Page and size beyond limits of authors
    if (pageNum - 1) * sizeNum > len(author_list_data):
        return {}
    author_list = list(author_list_data)
    index = (pageNum - 1) * sizeNum
    finalIndex = pageNum * sizeNum
    returnList = []
    while index < finalIndex:
        if index + 1 > len(author_list):
            break
        returnList.append(construct_author_object(author_list[index]))
        index += 1
    authorListDict = {}
    authorListDict["type"] = "authors"
    authorListDict["page"] = pageNum
    authorListDict["size"] = sizeNum
    authorListDict["items"] = returnList
    return authorListDict

# Constructs a post JSON object to be returned by the API
# Parameters:
#   post_data - serialized form of Post object
#   author - Author object of posts
# Returns: dict representing a post JSON object
def construct_post_object(post_data, author):
    postDict = dict(post_data)
    postDict["type"] = "post"
    serialzer = AuthorSerializer(author) 
    postDict["author"] = construct_author_object(serialzer.data)
    postDict["count"] = len(Comment.objects.filter(parentPost=postDict["id"]))
    postDict["comments"] = postDict["id"] + "/comments/"
    return postDict

# Constructs a list of public posts originating from an author
# in a JSON object to be returned by the API
# Parameters:
#   post_list_data - list of serialized form of Post objects
#   author - Author object of posts
# Returns: dict representing a list of posts JSON object
def construct_list_of_posts(post_list_data, author):
    postList = []
    for post_serial in post_list_data:
        postList.append(construct_post_object(post_serial, author))
    postListDict = {}
    postListDict["type"] = "posts"
    postListDict["items"] = postList
    return postListDict

# Constructs a paginated list of public posts originating from an author
# in a JSON object to be returned by the API
# Parameters:
#   author_list_data - list of serialized form of Posts objects
#   pageNum - page number, 1-indexed
#   sizeNum - number of elements on page
#   author - Author object of posts
# Returns: dict representing a paginated list of posts JSON object
def construct_list_of_paginated_posts(post_list_data, pageNum, sizeNum, author):
    # Page and size beyond limits of authors
    if (pageNum - 1) * sizeNum > len(post_list_data):
        return {}
    post_list = list(post_list_data)
    index = (pageNum - 1) * sizeNum
    finalIndex = pageNum * sizeNum
    postList = []
    while index < finalIndex:
        if index + 1 > len(post_list):
            break
        postList.append(construct_post_object(post_list[index], author))
        index += 1
    postListDict = {}
    postListDict["type"] = "posts"
    postListDict["page"] = pageNum
    postListDict["size"] = sizeNum
    postListDict["items"] = postList
    return postListDict

# Constructs a list of all public, listed posts on server
# in a JSON object to be returned by the API
# Parameters:
#  author_post_list_data_pair - list of pairs, with author and serialzed post object paired
# Returns: dict representing a list of all public, listed posts on server JSON object
# Source:
# https://www.tutorialsteacher.com/articles/how-to-flatten-list-in-python
def construct_list_of_all_posts(author_post_list_data_pair):
     return {
        "type": "posts",
        "items": reduce(lambda a, b:a+b, [[construct_post_object(post_serial, author) for post_serial in post_list_data] for author, post_list_data in author_post_list_data_pair]),
     }
# Constructs a comment JSON object to be returned by the API
# Parameters:
#   comment_data - serialized form of Comment object
#   author - Author object of comment
# Returns: dict representing a comment JSON object
def construct_comment_object(comment_data, author):
    commentDict = dict(comment_data)
    author_serialzer = AuthorSerializer(author)
    commentDict["type"] = "comment"
    commentDict["author"] = construct_author_object(author_serialzer.data)
    del commentDict["parentPost"]
    return commentDict

# Constructs a list of comments on a post in 
# a JSON object to be returned by the API
# Parameters:
#   comment_data - list of serialized form of Comment objects
#   post - parent Post object
# Returns: dict representing a list of comments JSON object
def construct_list_of_comments(comment_list_data, post):
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

# Constructs a paginated list of comments on a post in 
# a JSON object to be returned by the API
# Parameters:
#   comment_data - list of serialized form of Comment objects
#   pageNum - page number, 1-indexed
#   sizeNum - number of elements on page
#   post - parent Post object
# Returns: dict representing a list of comments JSON object
def construct_paginated_list_of_comments(comment_list_data, pageNum, sizeNum, author, post):
    if (pageNum - 1) * sizeNum > len(comment_list_data):
        return {}
    comment_list = list(comment_list_data)
    index = (pageNum - 1) * sizeNum
    finalIndex = pageNum * sizeNum
    commentList = []
    while index < finalIndex:
        if index + 1 > len(comment_list):
            break
        commentList.append(construct_comment_object(comment_list[index], author))
        index += 1
    commentListDict = {}
    commentListDict["type"] = "comments"
    commentListDict["page"] = pageNum
    commentListDict["size"] = sizeNum
    commentListDict["items"] = commentList
    commentListDict["post"] = post.id
    commentListDict["id"] = post.id + "/comments/"
    return commentListDict

# Constructs a like JSON object to be returned by the API
# Parameters:
#   like_data - serialized form of Like object
#   parentObject - parent object (Post or Comment)
#   author - Author object of like
# Returns: dict representing a like JSON object
def construct_like_object(like_data, parentObject, author):
    likeDict = dict(like_data)
    author_serialzer = AuthorSerializer(author)
    likeDict["author"] = construct_author_object(author_serialzer.data)
    likeDict["object"] = parentObject
    likeDict["summary"] = author.displayName + " likes this"
    likeDict["type"] = "Like"
    return likeDict

# Constructs a list of likes for a specfic post or comment
# as a JSON object to be returned by the API
# Parameters:
#   like__list_data - list of serialized form of Like objects
#   parentObjectID - parent object ID (Post or Comment)
# Returns: dict representing a list of likes JSON object
def construct_list_of_likes(like_list_data, parentObjectID):
    likeList = []
    for like_serial in like_list_data:
        likeAuthor = Author.objects.get(pk=like_serial["author"])
        likeList.append(construct_like_object(like_serial, parentObjectID, likeAuthor))
    likeListDict = {}
    likeListDict["type"] = "likes"
    likeListDict["items"] = likeList
    return likeListDict

# Constructs a list of likes on public posts/comments for
# a specfic author as a JSON object to be returned by the API
# Parameters:
#   liked_list_data - list of serialized form of Like objects
#   author - Author object of author
# Returns: dict representing a liked JSON object
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

# Constructs a list of followers of a specfic author 
# as a JSON object to be returned by the API
# Parameters:
#   follower_list_data - list of serialized form of Author objects
#   author - Author object of author
# Returns: dict representing a list of follwers JSON object
def construct_list_of_followers(follower_list_data):
    authorList = []
    for author_serial in follower_list_data:
        authorList.append(construct_author_object(author_serial))
    followerListDict = {}
    followerListDict["type"] = "followers"
    followerListDict["items"] = authorList
    return followerListDict

# Constructs a follow request object to be sent to the inbox of the request
# follower
# Parameters:
#   follow_request_data - serialized form of Follow Request object
#   author - sending author
#   actor - target author
# Returns: dict representing a Follow Request object
def construct_follow_request_object(follow_request_data, author, actor):
    # summary is already in the data
    followRequestDict=dict(follow_request_data)
    author_serialzer = AuthorSerializer(author)
    actor_serializer=AuthorSerializer(actor)
    followRequestDict["type"]="Follow"
    # get the object from follower_request
    followRequestDict["actor"]=construct_author_object(actor_serializer.data)
    followRequestDict["object"]=construct_author_object(author_serialzer.data)
    followRequestDict["summary"]= actor.displayName + " wants to follow " + author.displayName
    del followRequestDict["sender"]
    del followRequestDict["target"]
    del followRequestDict["date"]
    return followRequestDict

# Function that detrimines if the actor is a follower of the target or not
# Parameters:
#   actor - Author object of actor
#   target - Author object of target
# Returns: True if actor is a follower of target
def is_follower(actor, target):
    if actor.is_authenticated:
        return False
    if actor.is_staff:
        return True
    try:
        target.followers.all().get(user_id=actor.author)
        return True
    except:
        return False
