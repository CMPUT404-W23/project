from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# sampleFollowersDict={
#     "200":openapi.Response(
#         description="OK",
#         examples={
#             "application/json": {
#             "type": "followers",
#             "items": [
#                 {
#                     "id": "https://socialdistcmput404.herokuapp.com/authors/2",
#                     "host": "https://socialdistcmput404.herokuapp.com/",
#                     "displayName": "2",
#                     "github":"http://github.com/laracroft",
#                     "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
#                     "type": "author",
#                     "url": "https://socialdistcmput404.herokuapp.com/authors/2"
#                 },
#                 {
#                     "id": "https://socialdistcmput404.herokuapp.com/authors/3",
#                     "host": "https://socialdistcmput404.herokuapp.com",
#                     "displayName": "3",
#                     "github":"http://github.com/laracroft",
#                     "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
#                     "type": "author",
#                     "url": "https://socialdistcmput404.herokuapp.com/authors/3"
#                 }
#             ]
#         }
#         }
#     ),
#     "404": openapi.Response(
#         description="Error: Not Found",
#     ),
# }