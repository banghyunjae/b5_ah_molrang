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


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin users to access and modify the cart or cart item.
    """

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Only the owner of the cart or cart item can access and modify it
        return obj.user == request.user
