from django.contrib import admin
from .models import Tailor, TailorCoverImage

# Inline for TailorCoverImage to show cover images in Tailor admin
class TailorCoverImageInline(admin.TabularInline):
    model = TailorCoverImage
    extra = 1
    readonly_fields = ('uploaded_at',)
    fields = ('image', 'uploaded_at')

# Custom Tailor admin
@admin.register(Tailor)
class TailorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'category', 'subcategory', 'expertise', 'price', 'average_rating', 'is_available')
    list_filter = ('expertise', 'category', 'is_available')
    search_fields = ('business_name', 'user__username', 'category', 'subcategory')
    readonly_fields = ('average_rating',)
    inlines = [TailorCoverImageInline]

    fieldsets = (
        ('Business Information', {
            'fields': ('user', 'business_name', 'business_location', 'phone', 'NID', 'profile_picture', 'is_available')
        }),
        ('Expertise & Services', {
            'fields': ('expertise', 'expertise_details', 'category', 'subcategory', 'services_offered', 'price')
        }),
        ('Additional Info', {
            'fields': ('average_rating', 'purchased_products')
        }),
    )

    # Show cover images in Tailor list view (optional thumbnail display)
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;">'
        return 'No Image'
    display_profile_picture.allow_tags = True
    display_profile_picture.short_description = 'Profile Picture'

# Custom TailorCoverImage admin (optional, if you want to manage separately)
@admin.register(TailorCoverImage)
class TailorCoverImageAdmin(admin.ModelAdmin):
    list_display = ('tailor', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
