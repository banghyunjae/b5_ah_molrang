from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'quantity', 'selected',
                    'product_title', 'product_image', 'total_price']

    def product_title(self, obj):
        return obj.product.title

    def product_image(self, obj):
        return obj.product.image.url

    def total_price(self, obj):
        return obj.total_price

    product_title.short_description = 'Product Title'
    product_image.short_description = 'Product Image'
    total_price.short_description = 'Total Price'
