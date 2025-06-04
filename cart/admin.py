from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_total_price')
    search_fields = ('user__username',)
    list_filter = ('created_at',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'get_total_price')
    search_fields = ('cart__user__username', 'product__name')
    list_filter = ('product',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Item Total'
