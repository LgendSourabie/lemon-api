from rest_framework import permissions
from lemon_menuitems.utils import *


class IsSingleManagerOrNot(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        is_not_manager = not is_user_in_group(request=request, group_name='Manager')
        is_not_delivery_crew = not is_user_in_group(request=request, group_name='Delivery crew')

        if request.method == 'GET':
            return bool(is_not_delivery_crew and is_not_manager) # Only customer can get single order
        elif request.method == 'DELETE':
            return not is_not_manager # Only manager can delete an order
        elif request.method == 'PUT':
            return not is_not_manager
        elif request.method == 'PATCH':
            return bool((not is_not_manager) or (not is_not_delivery_crew and 'delivery_crew' not in request.data))

class IsCustomerOrNot(permissions.BasePermission):

    def has_permission(self, request, view):

        is_not_manager = not is_user_in_group(request=request, group_name='Manager')
        is_not_delivery_crew = not is_user_in_group(request=request, group_name='Delivery crew')

        if request.method == 'GET':
            return True                 # every user can see all orders but they have different views 
        if request.method == 'POST':
            return bool(is_not_delivery_crew and is_not_manager) # only customers can place orders



