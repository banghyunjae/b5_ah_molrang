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
        # 현재 사용자의 장바구니 아이템을 필터링합니다.
        cart_items = CartItem.objects.filter(
            cart__user=request.user).distinct()
        # CartItemSerializer를 사용하여 장바구니 아이템을 직렬화합니다.
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 전송된 데이터를 기반으로 CartItemListSerializer를 생성합니다.
        serializer = CartItemListSerializer(data=request.data)
        if serializer.is_valid():
            # 현재 사용자의 카트를 가져오거나 생성합니다.
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            # 카트에 이미 해당 상품이 있는지 확인합니다.
            cart_item = cart.cart_items.filter(product=product).first()
            if cart_item:
                # 이미 상품이 있는 경우 수량을 업데이트합니다.
                cart_item.quantity = quantity
                cart_item.save()
            else:
                # 상품이 없는 경우 새로운 CartItem을 생성합니다.
                CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartRetrieveUpdateDestroyView(APIView):
    """
    특정 장바구니 조회, 수정, 삭제를 담당합니다.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # 주어진 pk에 해당하는 카트를 가져옵니다.
        cart = self.get_object(pk)
        # CartSerializer를 사용하여 카트를 직렬화합니다.
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        # 주어진 pk에 해당하는 카트를 가져옵니다.
        cart = self.get_object(pk)
        # 전송된 데이터를 기반으로 CartSerializer를 생성합니다.
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # 주어진 pk에 해당하는 카트를 가져옵니다.
        cart = self.get_object(pk)
        # 카트에 속한 모든 아이템을 삭제합니다.
        cart.cart_items.all().delete()
        # 카트 자체를 삭제합니다.
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemRetrieveUpdateDestroyView(APIView):
    """
    특정 장바구니 아이템 조회, 수정, 삭제를 담당합니다.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # 주어진 pk에 해당하는 카트 아이템을 가져옵니다.
        cart_item = self.get_object(pk)
        # CartItemSerializer를 사용하여 카트 아이템을 직렬화합니다.
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        # 주어진 pk에 해당하는 카트 아이템을 가져옵니다.
        cart_item = self.get_object(pk)
        # 전송된 데이터를 기반으로 CartItemSerializer를 생성합니다.
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # 주어진 pk에 해당하는 카트 아이템을 가져옵니다.
        cart_item = self.get_object(pk)
        # 카트 아이템을 삭제합니다.
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartTotalPriceView(APIView):
    """
    장바구니 아이템들의 총 가격을 계산하여 반환합니다.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 사용자의 장바구니 아이템을 필터링합니다.
        cart_items = CartItem.objects.filter(
            cart__user=request.user).distinct()
        # 장바구니 아이템의 가격을 모두 합산합니다.
        total_price = sum(item.product.price *
                          item.quantity for item in cart_items)
        return Response({"total_price": total_price})


class CartItemSelectionView(APIView):
    """
    특정 장바구니 아이템의 선택 여부를 설정하거나 해제합니다.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # 주어진 pk에 해당하는 카트 아이템을 가져옵니다.
        cart_item = CartItem.objects.get(pk=pk)
        # 카트 아이템의 선택 여부를 True로 설정합니다.
        cart_item.is_selected = True
        cart_item.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # 주어진 pk에 해당하는 카트 아이템을 가져옵니다.
        cart_item = CartItem.objects.get(pk=pk)
        # 카트 아이템의 선택 여부를 False로 설정합니다.
        cart_item.is_selected = False
        cart_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
