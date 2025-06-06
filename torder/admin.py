from django.contrib import admin
from .models import TOrders

class TOrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'tailor', 'order_date', 'status', 'delivery_date')
    search_fields = ('buyer__username', 'tailor__business_name', 'status')
    list_filter = ('status', 'order_date', 'delivery_date')
    ordering = ('-order_date',)  # Recent orders first

admin.site.register(TOrders, TOrdersAdmin)
