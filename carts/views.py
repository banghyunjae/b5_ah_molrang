from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .permissions import IsOwnerOrReadOnly, IsCartOwner
from rest_framework.permissions import IsAuthenticated
from articles.models import Product


class CartListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.save(user=request.user)

            # Add items to the cart
            items_data = request.data.get('items', [])
            for item_data in items_data:
                product_id = item_data.get('product')
                quantity = item_data.get('quantity', 1)
                product = Product.objects.get(pk=product_id)
                CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCartOwner]

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        cart = self.get_object(pk)
        self.check_object_permissions(request, cart)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        self.check_object_permissions(request, cart)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def put(self, request, pk):
        cart_item = self.get_object(pk)
        self.check_object_permissions(request, cart_item)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object(pk)
        self.check_object_permissions(request, cart_item)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
