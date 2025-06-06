from django.db import models
from django.contrib.auth.models import User

class Tailor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tailor')
    business_name = models.CharField(max_length=255)
    business_location = models.TextField()

    EXPERTISE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    expertise_details = models.CharField(max_length=20, blank=True, null=True)
    expertise = models.CharField(max_length=20, choices=EXPERTISE_CHOICES, default='beginner')

    # Category examples: Punjabi, Shirt, Pant, Women's Dress
    category = models.CharField(
        max_length=20,
        choices=[
            ('punjabi', 'Punjabi'),
            ('shirt', 'Shirt'),
            ('pant', 'Pant'),
            ('women_dress', 'Women\'s Dress'),
        ],
        blank=True,
        null=True,
        default='None'
    )

    # Subcategory details like "Short Punjabi", "Formal Shirt", etc.
    subcategory = models.CharField(
        max_length=50,
        choices=[
            # Punjabi
            ('short_punjabi', 'Short Punjabi'),
            ('long_punjabi', 'Long Punjabi'),
            ('designer_punjabi', 'Designer Punjabi'),

            # Shirt
            ('formal_shirt', 'Formal Shirt'),
            ('casual_shirt', 'Casual Shirt'),
            ('half_sleeve_shirt', 'Half Sleeve Shirt'),

            # Pant
            ('formal_pant', 'Formal Pant'),
            ('jeans', 'Jeans'),
            ('cargo_pant', 'Cargo Pant'),

            # Women’s Dress
            ('salwar_kameez', 'Salwar Kameez'),
            ('lehenga', 'Lehenga'),
            ('blouse', 'Blouse'),
            ('saree_fall_pleat', 'Saree Fall & Pleat'),
        ],
        blank=True,
        null=True,
        default='None'
    )

    # Services offered - default will be "None"
    services_offered = models.TextField(
    blank=True,
    null=True,
    default="None"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    NID = models.CharField(max_length=20, unique=True)
    purchased_products = models.JSONField(default=list)

    profile_picture = models.ImageField(upload_to="tailor_profiles/", blank=True, null=True)
    average_rating = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"


class TailorCoverImage(models.Model):
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='cover_images')
    image = models.ImageField(upload_to="tailor_covers/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cover for {self.tailor.business_name}"
