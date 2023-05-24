from django.db import models
from users.models import User
from articles.models import Product


class Cart(models.Model):
    """
    장바구니 모델입니다. 유저와 1대1 관계를 가집니다.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 사용자와의 관계 설정
    created_at = models.DateTimeField(auto_now_add=True)  # 장바구니 생성일


class CartItem(models.Model):
    """
    장바구니_상품 모델입니다. 장바구니에 여러가지의 상품을 등록할 수 있습니다.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # 장바구니와의 관계 설정
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)  # 상품과의 관계 설정
    quantity = models.PositiveIntegerField(default=1)  # 상품 수량, 기본값은 1
    selected = models.BooleanField(default=False)  # 선택 여부 필드 추가

    @property
    def total_price(self):
        return self.quantity * self.product.price

    @property
    def product_image(self):
        return self.product.image.url

    @property
    def product_title(self):
        return self.product.title
