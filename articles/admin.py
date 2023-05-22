from django.contrib import admin
from articles.models import Product

# Register your models here.
class ProductDisplayAdmin(admin.ModelAdmin):
    list_display = ('product', 'content', 'price', 'image', 'total_quantity','inventory_status')
    list_display_links = ('product',)
    fields = ('product', 'content', 'price', 'image', 'total_quantity','inventory_status')
    list_filter = ('inventory_status',)
    search_fields = ('product',)


admin.site.register(Product, ProductDisplayAdmin)    