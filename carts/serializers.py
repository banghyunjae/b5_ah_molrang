from rest_framework import serializers
from .models import Cart, CartItem
from articles.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'price', 'content',
                  'writer', 'quantity', 'is_selected']

    def get_price(self, obj):
        return obj.product.price

    def get_content(self, obj):
        return obj.product.content

    def get_writer(self, obj):
        return obj.product.writer.username


class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
