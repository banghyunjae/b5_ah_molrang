from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    소유자만 수정할 수 있는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsCartOwner(permissions.BasePermission):
    """
    카트의 소유자만 접근할 수 있는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    카트 또는 카트 아이템의 소유자 또는 관리자만 접근하고 수정할 수 있는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.user == request.user
