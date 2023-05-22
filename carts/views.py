from rest_framework import viewsets
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer
from .permissions import IsOwnerOrReadOnly


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # 총합계를 표시하는 로직
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_price = sum(cart.calculate_total_price() for cart in queryset)
        data = {
            'total_price': total_price,
            'results': self.get_serializer(queryset, many=True).data
        }
        return Response(data)
