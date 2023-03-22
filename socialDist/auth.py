from rest_framework import permissions
from . import models

# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

HOST="socialcmput404.herokuapp.com"

# verify that connecting node is allowed to connect 
class RemotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # local test purposes only
        # TODO REMOVE THIS 
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

# used for inbox views
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
        


