from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    해당 객체의 소유자만 수정할 수 있는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용합니다.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 카트 또는 카트 아이템의 소유자에게만 허용합니다.
        return obj.user == request.user


class IsCartOwner(permissions.BasePermission):
    """
    해당 카트의 소유자만 접근할 수 있는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    해당 카트 또는 카트 아이템의 소유자 또는 관리자만 접근하고 수정할 수 있는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        # 관리자 사용자는 모든 접근 권한을 가집니다.
        if request.user.is_staff or request.user.is_superuser:
            return True

        # 카트 또는 카트 아이템의 소유자만 접근하고 수정할 수 있습니다.
        return obj.user == request.user
