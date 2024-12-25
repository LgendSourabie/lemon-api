from rest_framework import permissions
from lemon_menuitems.utils import *

class IsManagerOrNot(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method in ['POST','DELETE','PATCH','PUT']:
            return is_user_in_group(request=request, group_name='Manager')

class IsSingleManagerOrNot(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method == 'GET':
            return True
        elif request.method in ['POST','DELETE','PATCH','PUT']:
            return is_user_in_group(request=request, group_name='Manager')

class IsCustomerOrNot(permissions.BasePermission):

    def has_permission(self, request, view):

        is_not_manager = not is_user_in_group(request=request, group_name='Manager')
        is_not_delivery_crew = not is_user_in_group(request=request, group_name='Delivery crew')

        if request.method in ['GET','POST', 'DELETE']:
            return bool(is_not_delivery_crew and is_not_manager)



