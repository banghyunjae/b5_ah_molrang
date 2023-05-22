from rest_framework import serializers
from articles.models import Product

class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    inventory_status = serializers.SerializerMethodField()
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y년 %m월 %d일 %p %I:%M")
    
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y년 %m월 %d일 %p %I:%M")
    
    def get_inventory_status(self, obj):
        if obj.inventory_status == True:
            if obj.total_quantity <= 5:
                return f"품절 임박! 남은 수량 : {obj.total_quantity}"
            return f"남은 수량 : {obj.total_quantity}"
        else:
            return "Sold Out"
    
    class Meta:
        model = Product
        fields = "__all__"

        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product', 'content', 'price', 'user', 'image', 'total_quantity')