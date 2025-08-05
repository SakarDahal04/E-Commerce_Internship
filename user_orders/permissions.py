from rest_framework.permissions import BasePermission


class PermManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
class IsObjectOwner(PermManager):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user

class IsOrderItemOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user
    
class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user