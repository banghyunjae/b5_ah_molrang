from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Product
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from articles.serializers import ProductSerializer, ProductCreateSerializer


# 상품목록과 작성
class ProductView(APIView):
    # 상품 목록
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = ProductCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()