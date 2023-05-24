from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the cart or cart item
        return obj.user == request.user


class IsCartOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of the cart to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
