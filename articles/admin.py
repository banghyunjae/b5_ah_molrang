from django.contrib import admin
from articles.models import Product

# Register your models here.
class ProductDisplayAdmin(admin.ModelAdmin):
    list_display = ('writer','product', 'content', 'price', 'image', 'total_quantity','inventory_status')
    list_display_links = ('product',)
    fields = ('writer','product', 'content', 'price', 'image', 'total_quantity','inventory_status')
    list_filter = ('inventory_status',)
    search_fields = ('product',)
    readonly_fields = ('inventory_status',)


admin.site.register(Product, ProductDisplayAdmin)    