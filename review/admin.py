from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'tailor', 'rating', 'timestamp')  # Main columns
    search_fields = ('user__username', 'product__name', 'tailor__business_name')  # Searchable fields
    list_filter = ('rating', 'timestamp')  # Filtering options
    ordering = ('-timestamp',)  # Show latest reviews first

admin.site.register(Review, ReviewAdmin)
