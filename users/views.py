from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from users.serializers import CustomTokenObtainPairSerializer, UserSerializer


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료 ^^"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        """ 회원 정보를 수정합니다. """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"massage":"수정완료"}, status= status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ 회원 탈퇴 기능입니다. """
        user= request.user
        user.is_active = False
        user.save()
        return Response({'message': '삭제완료'})

class CustomTokenObtainPairView(TokenObtainPairView):   #이게 로그인 기능이라서, 로그인 코드를 쓸 필요가 없었다는 것.
    serializer_class = CustomTokenObtainPairSerializer