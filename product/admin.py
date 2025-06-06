from django.contrib import admin
from .models import Product, ProductImage, UserActivity

# Product Admin Panel
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'tailor', 'price', 'availability', 'orders', 'popularity', 'date')
    search_fields = ('name', 'tailor__business_name', 'category')
    list_filter = ('category', 'date', 'availability')
    ordering = ('-date',)  # Show newest products first

# Product Image Admin Panel
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    search_fields = ('product__name',)

# User Activity Admin Panel (If Needed)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'action', 'timestamp')
    search_fields = ('user__username', 'product__name')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)

# Register Models in Django Admin
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(UserActivity, UserActivityAdmin)  # Remove if not needed
