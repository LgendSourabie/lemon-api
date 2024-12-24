from rest_framework import permissions
from lemon_menuitems.utils import *

class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in ['GET','POST','DELETE','PATCH','PUT']:
            return is_user_in_group(request=request, group_name='Manager')
        

class IsSingleManager(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['GET','POST','DELETE','PATCH','PUT']:
            return is_user_in_group(request=request, group_name='Manager')