from django.contrib import admin
from .models import Cart, CartItem



class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added', 'get_cart_items_count')
    search_fields = ('cart_id',)
    readonly_fields = ('date_added',)

    def get_cart_items_count(self, obj):
        return obj.cartitem_set.count()
    get_cart_items_count.short_description = 'Number of items'


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active', 'get_variations', 'get_sub_total')
    list_editable = ('quantity', 'is_active')
    list_filter = ('product', 'is_active', 'cart')
    search_fields = ('product__product_name', 'cart__cart_id')

    def get_sub_total(self, obj):
        return obj.sub_total()
    get_sub_total.short_description = 'Subtotal'

    def get_variations(self, obj):
        return ", ".join([str(v) for v in obj.variations.all()])
    get_variations.short_description = 'Variations'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
