from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available', 'created_date')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('category', 'is_available')
    search_fields = ('product_name', 'description')
    ordering = ('-created_date',)

admin.site.register(Product, ProductAdmin)
