from django.db import models
from django.contrib.auth.models import User  # Importing User model
from django.utils.timezone import now
from tailor.models import Tailor

class TOrders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='torders')
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='torders')
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=11, blank=True, null=True)  # Allowing null or blank values
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Status choices added
    size = models.CharField(max_length=20)
    fabrics = models.CharField(max_length=50)  # Increased max_length for flexibility
    description = models.TextField()  # Typo fixed from `torder_description`
    measurement = models.JSONField(default=dict, blank=True, null=True)  # Changed to JSONField for better structuring
    delivery_date = models.DateField(blank=True, null=True)  # Fixed default=None issue
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username} to {self.tailor.business_name}"
