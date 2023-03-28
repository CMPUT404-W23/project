from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Dicts for sample responses (used in swagger/ Open API)
sampleGETAuthorDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1",
            "host": "https://socialdistcmput404.herokuapp.com/",
            "displayName": "1",
            "github": "https://sampleUser.github.com",
            "profileImage": "http://sampleUserImage.com/1.jpg",
            "type": "author",
            "url": "https://socialdistcmput404.herokuapp.com/authors/1"
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

samplePOSTAuthorDict={
    "201":openapi.Response(
        description="Created",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1",
            "host": "https://socialdistcmput404.herokuapp.com/",
            "displayName": "1",
            "github": "https://sampleUser.github.com",
            "profileImage": "http://sampleUserImage.com/1.jpg",
            "type": "author",
            "url": "https://socialdistcmput404.herokuapp.com/authors/1"
        }
        }
    ),
    "400": openapi.Response(
        description="Bad Request",
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),

}

sampleListAuthorDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json":{
            "type": "authors",
            "items": [
                {
                "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "2",
                "github": "https://sampleUser2.github.com",
                "profileImage": "sampleUser2Image.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                },
                {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github": "https://sampleUser.github.com",
                "profileImage": "sampleUserImage.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
                }
            ]
            }
        }
    ),
    "404": openapi.Response(
        description="Error: Author Not Found",
    ),
}

sampleGETPostDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
            "title": "testTitle",
            "source": "testSource",
            "origin": "testOrigin",
            "description": "testDescr",
            "content": "testPost",
            "contentType": "text/plain",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github": "https://sampleUser.github.com",
                "profileImage": "http://sampleUserImage.com/2.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
            },
            "published": "2023-03-22T19:15:07Z",
            "visibility": "VISIBLE",
            "categories": "test",
            "unlisted": False,
            "type": "post",
            "count": 0,
            "comments": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
            }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

samplePOSTPostDict={
    "201":openapi.Response(
        description="Created",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
            "title": "testTitle",
            "source": "testSource",
            "origin": "testOrigin",
            "description": "testDescr",
            "content": "testPost",
            "contentType": "text/plain",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github": "https://sampleUser.github.com",
                "profileImage": "http://sampleUserImage.com/2.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
            },
            "published": "2023-03-22T19:15:07Z",
            "visibility": "VISIBLE",
            "categories": "test",
            "unlisted": False,
            "type": "post",
            "count": 0,
            "comments": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
            }
        }
    ),
    "400": openapi.Response(
        description="Bad Request",
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleDELETEDict={
    "200":openapi.Response(
        description="OK",
    ),
    "400": openapi.Response(
        description="Bad Request",
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleListPostsDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "posts",
            "items": [
                {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
                "title": "testTitle",
                "source": "testSource",
                "origin": "testOrigian",
                "description": "testDescr",
                "content": "testPost",
                "contentType": "text/plain",
                "author": {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                    "host": "https://socialdistcmput404.herokuapp.com/",
                    "displayName": "1",
                    "github": "https://sampleUser.github.com",
                    "profileImage": "sampleUserImage.jpg",
                    "type": "author",
                    "url": "https://socialdistcmput404.herokuapp.com/authors/1"
                },
                "published": "2023-03-22T19:15:07Z",
                "visibility": "VISIBLE",
                "categories": "test",
                "unlisted": False,
                "type": "post",
                "count": 2,
                "comments": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
                },
                {
                "id": "string",
                "title": "string",
                "source": "string",
                "origin": "string",
                "description": "string",
                "content": "string",
                "contentType": "text/plain",
                "author": {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                    "host": "https://socialdistcmput404.herokuapp.com/",
                    "displayName": "1",
                    "github": "https://sampleUser.github.com",
                    "profileImage": "sampleUserImage.jpg",
                    "type": "author",
                    "url": "https://socialdistcmput404.herokuapp.com/authors/1"
                },
                "published": "2023-03-27T00:20:07.768000Z",
                "visibility": "VISIBLE",
                "categories": "string",
                "unlisted": True,
                "type": "post",
                "count": 0,
                "comments": "string/comments/"
                },
            ]
            }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleImagePostGETDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
            "title": "imagePostTitle",
            "source": "imagePostSource",
            "origin": "imagePostOrigin",
            "description": "",
            "content": "base64string for image itself",
            "contentType": "image/jpg;base64",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github": "https://sampleUser.github.com",
                "profileImage": "sampleUserImage.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
            },
            "published": "2023-03-22T19:15:07Z",
            "visibility": "VISIBLE",
            "categories": "test",
            "unlisted": False,
            "type": "post",
            "count": 2,
            "comments": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
            }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleGETCommentDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/1",
            "content": "test comment",
            "contentType": "text/plain",
            "published": "2023-03-22T19:15:51Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github": "https://sampleUser.github.com",
                "profileImage": "sampleUserImage.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
            },
            "type": "comment"
}
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

samplePOSTCommentDict={
    "201":openapi.Response(
        description="Created",
        examples={
            "application/json": {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/1",
            "content": "test comment",
            "contentType": "text/plain",
            "published": "2023-03-22T19:15:51Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github": "https://sampleUser.github.com",
                "profileImage": "sampleUserImage.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
            },
            "type": "comment"
}
        }
    ),
    "400": openapi.Response(
        description="Bad Request",
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleListCommentsDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "comments",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments",
                    "content": "test comment",
                    "contentType": "text/plain",
                    "published": "2023-03-22T19:15:51Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "1",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "sampleUserImage.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1"
                    },
                    "type": "comment"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/1",
                    "content": "test comment",
                    "contentType": "text/plain",
                    "published": "2023-03-22T19:15:51Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "1",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "sampleUserImage.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1"
                    },
                    "type": "comment"
                }
            ],
            "post": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleListLikesPostDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "likes",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/1/likes",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "2",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "sampleUserImage.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                    },
                    "published": "2023-03-23T23:46:00Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
                    "summary": "2 likes this",
                    "type": "Like"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/3/likes",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "2",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "sampleUserImage.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                    },
                    "published": "2023-03-23T23:46:00Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
                    "summary": "2 likes this",
                    "type": "Like"
                }
            ]
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleListLikesPostDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "likes",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/1/comments/1/likes",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "2",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "sampleUserImage.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                    },
                    "published": "2023-03-23T04:43:20Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/2/posts/1/comments/1",
                    "summary": "2 likes this",
                    "type": "Like"
                }
            ]
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleListLikedDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type":"liked",
            "items":[
                {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "summary": "Lara Croft Likes your post",         
                    "type": "Like",
                    "author":{
                        "type":"author",
                        "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "host":"http://127.0.0.1:5454/",
                        "displayName":"Lara Croft",
                        "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "github":"http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
                }
            ]
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleFollowersDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "followers",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                    "host": "https://socialdistcmput404.herokuapp.com/",
                    "displayName": "2",
                    "github":"http://github.com/laracroft",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                    "type": "author",
                    "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/3",
                    "host": "https://socialdistcmput404.herokuapp.com",
                    "displayName": "3",
                    "github":"http://github.com/laracroft",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                    "type": "author",
                    "url": "https://socialdistcmput404.herokuapp.com/authors/3"
                }
            ]
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleInboxDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
    "type": "inbox",
    "author": "https://socialdistcmput404.herokuapp.com/authors/1",
    "items": [
        {
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
            "title": "testTitle",
            "source": "testSource",
            "origin": "testOrigian",
            "description": "testDescr",
            "content": "testPost",
            "contentType": "text/plain",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "1",
                "github":"http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1"
            },
            "published": "2023-03-22T19:15:07Z",
            "visibility": "VISIBLE",
            "categories": "test",
            "unlisted": False,
            "type": "post",
            "count": 2,
            "comments": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
        }
    ]
}
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleListEveryPostDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "posts",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/1",
                    "title": "Title",
                    "source": "source",
                    "origin": "testOrigian",
                    "description": "...",
                    "content": "...",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "2",
                        "github":"http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                    },
                    "published": "2023-03-22T21:31:25Z",
                    "visibility": "VISIBLE",
                    "categories": "test",
                    "unlisted": False,
                    "type": "post",
                    "count": 2,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/1/comments/"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/2",
                    "title": "title 2",
                    "source": "test 2",
                    "origin": "2",
                    "description": "2",
                    "content": "2222",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "2",
                        "github":"http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                    },
                    "published": "2023-03-22T21:38:54Z",
                    "visibility": "VISIBLE",
                    "categories": "test",
                    "unlisted": False,
                    "type": "post",
                    "count": 1,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/2/comments/"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
                    "title": "testTitle",
                    "source": "testSource",
                    "origin": "testOrigian",
                    "description": "testDescr",
                    "content": "testPost",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "1",
                        "github":"http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1"
                    },
                    "published": "2023-03-22T19:15:07Z",
                    "visibility": "VISIBLE",
                    "categories": "test",
                    "unlisted": False,
                    "type": "post",
                    "count": 2,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
                }
            ]
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

testDict={
  "content": "swagger test string",
  "contentType": "text/plain",
  "parentPost": "https://socialdistcmput404.herokuapp.com/authors/2/posts/1/",
  "published": "2023-03-27T18:18:57.059Z",
   "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "jasonk",
                "github": "",
                "profileImage": "",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/2"
            },
}