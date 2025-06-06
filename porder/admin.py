from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'quantity', 'price', 'status', 'order_date', 'delivery_date')
    search_fields = ('buyer__username', 'product__name', 'status')
    list_filter = ('status', 'order_date')

admin.site.register(Order, OrderAdmin)
