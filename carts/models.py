from django.db import models
from django.conf import settings
from articles.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s 장바구니"

    def total(self):
        return sum(item.subtotal() for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.product.price * self.quantity
