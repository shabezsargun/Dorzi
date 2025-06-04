from django.contrib import admin
from .models import Contact

# Register the Contact model with the admin interface
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')
    list_filter = ('name',)
    ordering = ('name',)
