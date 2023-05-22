from rest_framework import serializers
from articles.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product', 'content', 'price', 'image')