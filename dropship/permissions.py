from rest_framework import permissions
from dropship.models import *


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user and request.user.groups.filter(name="IsProjectManager"):
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user and request.user.groups.filter(name="IsAdmin") or request.user:
            return True
        return False
