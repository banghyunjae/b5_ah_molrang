from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Product, Review
from rest_framework import status
from articles.permissions import IsAdminOrReadOnly
from articles.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


# 상품목록과 작성 - 아직 권한 설정은 안했어요
class ProductView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    # 상품 목록
    def get(self, request):
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 상품 등록
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 상품 상페페이지 보기, 수정, 삭제 - 아직 권한 설정은 안했어요
class ProductDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    # 상품 상세페이지
    def get(self, request, id_product):
        product = get_object_or_404(Product, id=id_product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정하기
    def put(self, request, id_product):
        product = get_object_or_404(Product, id=id_product)
        # 본인이 작성한 글이 맞다면
        if request.user == product.writer:
            serializer = ProductCreateSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 본인의 게시글이 아니라면
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 삭제하기
    def delete(self, request, id_product):
        product = get_object_or_404(Product, id=id_product)
        # 본인이 작성한 글이 맞다면
        if request.user == product.writer:
            product.delete()
            return Response(
                {"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        # 본인의 게시글이 아니라면
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class ReviewView(APIView):
    def get(self, request, id_product):
        reviews = Review.objects.filter(product_id=id_product)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_reviews = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(paginated_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)

    # 등록
    def post(self, request, id_product):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product_id=id_product, writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    # 수정
    def put(self, request, id_product, id_review):
        review = get_object_or_404(Review, id=id_review, product_id=id_product)

        if request.user == review.writer:
            serializer = ReviewCreateSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 삭제
    def delete(self, request, id_product, id_review):
        review = get_object_or_404(Review, id=id_review, product_id=id_product)

        if request.user == review.writer:
            review.delete()
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class WishView(APIView):
    def post(self, request, id_product):
        product = get_object_or_404(Product, id=id_product)
        if request.user in product.wishes.all():
            product.wishes.remove(request.user)
            return Response("찜취소했습니다.", status=status.HTTP_200_OK)

        else:
            product.wishes.add(request.user)
            return Response("찜했습니다.", status=status.HTTP_200_OK)
