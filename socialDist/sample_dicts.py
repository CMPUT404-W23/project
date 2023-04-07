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

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Dicts for sample responses (used in swagger/ Open API)

sampleGETAuthorDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDauthor",
                "github": "https://sampleUser1.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
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
                "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDauthor",
                "github": "https://sampleUser1.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
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

samplePUTAuthorDict={
    "201":openapi.Response(
        description="Created",
        examples={
            "application/json": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDauthor",
                "github": "https://sampleUser1.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
            }
        }
    ),
    "400": openapi.Response(
        description="Bad Request",
    ),
    "409": openapi.Response(
        description="Conflict",
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
                "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDauthor",
                "github": "https://sampleUser1.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
            },
            {
                "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDTest",
                "github": "https://sampleUser2.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
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
                "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDTest",
                "github": "https://sampleUser2.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
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
            "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6",
            "title": "UUID post",
            "source": "testSource",
            "origin": "testOrigin",
            "description": "hello UUID",
            "content": "testPost",
            "contentType": "text/plain",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "jasonk",
                "github": "https://sampleUser.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/2"
            },
            "published": "2023-03-31T04:21:01.583364Z",
            "visibility": "FRIENDS",
            "categories": "hellooo",
            "unlisted": False,
            "type": "post",
            "count": 0,
            "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6/comments/"
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

sampleDELETEPostDict={
    "200":openapi.Response(
        description="OK",
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
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "title": "UUID testing heroku",
                    "source": "UUID heroku",
                    "origin": "string",
                    "description": "UUID Post",
                    "content": "heroku 2.0",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T02:08:01.730885Z",
                    "visibility": "VISIBLE",
                    "categories": "string",
                    "unlisted": True,
                    "type": "post",
                    "count": 1,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6",
                    "title": "UUID post",
                    "source": "test Soruce",
                    "origin": "test origin",
                    "description": "hello UUID",
                    "content": "test content",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T04:21:01.583364Z",
                    "visibility": "FRIENDS",
                    "categories": "hellooo",
                    "unlisted": False,
                    "type": "post",
                    "count": 0,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6/comments/"
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
            "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6",
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
            "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6/comments/",
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
            "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
            "content": "UUID test comment on heroku",
            "contentType": "text/plain",
            "published": "2023-03-31T02:12:59.861038Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDTest",
                "github": "https://sampleUser.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
            },
            "type": "comment"
        }
        }
    ),
    "401":openapi.Response(
        description="Unauthorized",
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
            "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
            "content": "UUID test comment on heroku",
            "contentType": "text/plain",
            "published": "2023-03-31T02:12:59.861038Z",
            "author": {
                "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDTest",
                "github": "https://sampleUser.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
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
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
                    "content": "UUID test comment on heroku",
                    "contentType": "text/plain",
                    "published": "2023-03-31T02:12:59.861038Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "type": "comment"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9dasfdasefase94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
                    "content": "UUID test comment on heroku 2",
                    "contentType": "text/plain",
                    "published": "2023-03-31T02:12:59.861038Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9dasfdasefase94f7c2"
                    },
                    "type": "comment"
                }
            ],
            "post": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1",
            "id": "https://socialdistcmput404.herokuapp.com/authors/1/posts/1/comments/"
        }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

samplePOSTListCommentsDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "comments",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
                    "content": "UUID test comment on heroku",
                    "contentType": "text/plain",
                    "published": "2023-03-31T02:12:59.861038Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "type": "comment"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9dasfdasefase94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
                    "content": "UUID test comment on heroku 2",
                    "contentType": "text/plain",
                    "published": "2023-03-31T02:12:59.861038Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9dasfdasefase94f7c2"
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
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/6dbaed7a-b4de-48b1-915f-261dfcb643c7",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDauthor",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
                    },
                    "published": "2023-03-31T02:16:51.190627Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "summary": "UUIDauthor likes your post",
                    "type": "Like"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/1c83fa57-0086-4a84-a654-f88a53041c3e",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T04:40:24.413884Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "summary": "UUIDTest likes your post",
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

sampleListLikesCommentDict={
    "200":openapi.Response(
        description="OK",
        examples={
            "application/json": {
            "type": "likes",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/6dbaed7a-b4de-48b1-915f-261dfcb643c7",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDauthor",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
                    },
                    "published": "2023-03-31T02:16:51.190627Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/112bce3e-194c-40f0-a167-e737181b7d71",
                    "summary": "UUIDauthor likes your comment",
                    "type": "Like"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/1c83fa57-0086-4a84-a654-f88a53041c3e",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T04:40:24.413884Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                    "summary": "UUIDTest likes your comment",
                    "type": "Like"
                },
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
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/6dbaed7a-b4de-48b1-915f-261dfcb643c7",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDauthor",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
                    },
                    "published": "2023-03-31T02:16:51.190627Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/112bce3e-194c-40f0-a167-e737181b7d71",
                    "summary": "UUIDauthor liked your comment",
                    "type": "Like"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/1c83fa57-0086-4a84-a654-f88a53041c3e",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T04:40:24.413884Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                    "summary": "UUIDTest liked your comment",
                    "type": "Like"
                },
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
                "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                "host": "https://socialdistcmput404.herokuapp.com/",
                "displayName": "UUIDauthor",
                "github": "https://sampleUser1.github.com",
                "profileImage": "http://sampleUserImage.com/1.jpg",
                "type": "author",
                "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                    "host": "https://socialdistcmput404.herokuapp.com/",
                    "displayName": "UUIDTest",
                    "github": "https://sampleUser2.github.com",
                    "profileImage": "http://sampleUserImage.com/1.jpg",
                    "type": "author",
                    "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                }
            ]
        }
        }
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleDELETEFollowersDict={
    "200":openapi.Response(
        description="OK",
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
            "author": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
            "items": [
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "title": "UUID testing heroku",
                    "source": "UUID heroku",
                    "origin": "string",
                    "description": "UUID Post",
                    "content": "heroku 2.0",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T02:08:01.730885Z",
                    "visibility": "VISIBLE",
                    "categories": "string",
                    "unlisted": True,
                    "type": "post",
                    "count": 1,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6",
                    "title": "UUID post",
                    "source": "test Source",
                    "origin": "test Origin",
                    "description": "hello UUID",
                    "content": "test Content",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "jasonk",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/2"
                    },
                    "published": "2023-03-31T04:21:01.583364Z",
                    "visibility": "FRIENDS",
                    "categories": "hellooo",
                    "unlisted": False,
                    "type": "post",
                    "count": 0,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6/comments/"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/6dbaed7a-b4de-48b1-915f-261dfcb643c7",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDauthor",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/1641802d-c565-45b2-b4f7-ec08504038c8"
                    },
                    "published": "2023-03-31T02:16:51.190627Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "summary": "UUIDauthor liked your post",
                    "type": "Like"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/likes/1c83fa57-0086-4a84-a654-f88a53041c3e",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T04:40:24.413884Z",
                    "object": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "summary": "UUIDTest liked your post",
                    "type": "Like"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/39c779b5-ac73-44da-84a1-8d451ff370f3",
                    "content": "UUID test comment on heroku",
                    "contentType": "text/plain",
                    "published": "2023-03-31T02:12:59.861038Z",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "type": "comment"
                }
            ]
        }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized",
    ),
    "404": openapi.Response(
        description="Error: Not Found",
    ),
}

sampleDELETEInboxDict={
    "200":openapi.Response(
        description="OK",
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
                    "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71",
                    "title": "UUID testing heroku",
                    "source": "UUID heroku",
                    "origin": "string",
                    "description": "UUID Post",
                    "content": "heroku 2.0",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T02:08:01.730885Z",
                    "visibility": "VISIBLE",
                    "categories": "string",
                    "unlisted": True,
                    "type": "post",
                    "count": 1,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2/posts/112bce3e-194c-40f0-a167-e737181b7d71/comments/"
                },
                {
                    "id": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6",
                    "title": "UUID post",
                    "source": "test Soruce",
                    "origin": "test origin",
                    "description": "hello UUID",
                    "content": "test content",
                    "contentType": "text/plain",
                    "author": {
                        "id": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2",
                        "host": "https://socialdistcmput404.herokuapp.com/",
                        "displayName": "UUIDTest",
                        "github": "https://sampleUser.github.com",
                        "profileImage": "http://sampleUserImage.com/1.jpg",
                        "type": "author",
                        "url": "https://socialdistcmput404.herokuapp.com/authors/ba109973-9c56-4e06-9e2e-9d4bef94f7c2"
                    },
                    "published": "2023-03-31T04:21:01.583364Z",
                    "visibility": "FRIENDS",
                    "categories": "hellooo",
                    "unlisted": False,
                    "type": "post",
                    "count": 0,
                    "comments": "https://socialdistcmput404.herokuapp.com/authors/2/posts/ef29e6f2-8302-4f5d-901c-cc47ae2daca6/comments/"
                },
                
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