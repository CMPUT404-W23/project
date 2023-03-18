from rest_framework import permissions
from . import models

# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

# verify that connecting node is allowed to connect
class RemotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        local_hosts = ['127.0.0.1:8000', 'socialdistcmput404.herokuapp.com', 'localhost:8000']
        try:
            server = models.Server.objects.get(serverAddress="https://"+request.get_host())
        except models.Server.DoesNotExist:
            return False
        if request.method not in permissions.SAFE_METHODS:
            return request.get_host() in local_hosts
        return True

#TODO: implement inbox permissions
class InboxPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
            


