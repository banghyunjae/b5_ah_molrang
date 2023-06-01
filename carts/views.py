from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemListSerializer
from .permissions import IsOwnerOrAdmin
from django.http import Http404


class CartListCreateView(APIView):
    """
    장바구니 목록 조회 및 생성을 담당합니다.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(
            cart__user=request.user).distinct()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemListSerializer(data=request.data)
        if serializer.is_valid():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            cart_item = cart.cart_items.filter(product=product).first()
            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartRetrieveUpdateDestroyView(APIView):
    """
    장바구니 조회, 수정, 삭제를 담당합니다.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        cart.cart_items.all().delete()
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemRetrieveUpdateDestroyView(APIView):
    """
    장바구니 아이템 조회, 수정, 삭제를 담당합니다.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartTotalPriceView(APIView):
    """
    장바구니 아이템들의 총 가격을 계산하여 반환합니다.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(
            cart__user=request.user).distinct()
        total_price = sum(item.product.price *
                          item.quantity for item in cart_items)
        return Response({"total_price": total_price})


class CartItemSelectionView(APIView):
    """
    장바구니 아이템의 선택 여부를 설정하거나 해제합니다.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.is_selected = True
        cart_item.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.is_selected = False
        cart_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
