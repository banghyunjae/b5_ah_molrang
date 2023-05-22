from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    product_title = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'price', 'total_price',
                  'product_image', 'product_title']

    def get_total_price(self, instance):
        return instance.total_price

    def get_product_image(self, instance):
        return instance.product_image

    def get_product_title(self, instance):
        return instance.product_title


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
