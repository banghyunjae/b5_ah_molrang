from django.db import models
from django.conf import settings
from articles.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}'의 장바구니"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product} - {self.quantity}"

    def subtotal(self):
        return self.product.price * self.quantity
