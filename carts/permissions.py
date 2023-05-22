from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    장바구니 소유자만 쓰기 작업을 허용하는 권한 설정 클래스
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS 요청은 항상 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 장바구니 소유자인 경우에만 쓰기 작업 허용
        return obj.cart.user == request.user
