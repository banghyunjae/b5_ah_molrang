from dataclasses import field
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from articles.serializers import ProductSerializer, WishListSerializer, ReviewListSerializer, ProductListSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

class UserProfileSerializer(serializers.ModelSerializer):
    product_set = ProductListSerializer(many=True) # 작성한 물품 불러오기
    review_set = ReviewListSerializer(many= True) # 내가 쓴 리뷰 불러오기
    wishes = WishListSerializer(many= True)  # 찜한 상품 불러오기


    class Meta:
        model = User
        fields = ("id", "email","product_set", "wishes", "review_set")
