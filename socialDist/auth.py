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

from rest_framework import permissions
from . import models

# Sources:
# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

HOST="socialcmput404.herokuapp.com"

# Permission class used for most endpoints to restrict remote node access
class RemotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Special permission for admin users, can use API without auth token
        if request.user.is_authenticated and request.user.is_staff:
            return True
        try:
            authorization = request.headers['Authorization']
            authorizationArr = authorization.split()
            if authorizationArr[0] != "Token":
                return False
            server = models.Server.objects.get(serverKey=authorizationArr[1])
            if request.method not in permissions.SAFE_METHODS and not server.isLocalServer:
                return False
            return True
        except:
            return False

# Permission class used for the inbox endpoints to restrict remote node access
class InboxPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            authorization = request.headers['Authorization']
            authorizationArr = authorization.split()
            if authorizationArr[0] != "Token":
                return False
            server = models.Server.objects.filter(serverKey=authorizationArr[1])
            #TODO: modify to match inbox permissions
            if request.method not in permissions.SAFE_METHODS and not server.isLocalServer:
                return False
            return True
        except:
            return False
        


