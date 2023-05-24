from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'quantity', 'selected',
                    'get_product_title', 'get_product_image', 'total_price']

    def get_product_title(self, obj):
        return obj.product.product

    def get_product_image(self, obj):
        if obj.product.image:
            return obj.product.image.url
        return None

    def total_price(self, obj):
        return obj.total_price

    get_product_title.short_description = 'Product Title'
    get_product_image.short_description = 'Product Image'
    total_price.short_description = 'Total Price'
