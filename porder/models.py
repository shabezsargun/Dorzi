from django.db import models
from django.contrib.auth.models import User
from tailor.models import *
from product.models import *
from review.models import *

class Order(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='porder')  # Buyer (Customer)
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='porder', default=None)  # Tailor
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='porder')  # Ordered Product
    quantity = models.IntegerField()  # Number of products
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per product
    order_date = models.DateTimeField(auto_now_add=True)  # Order timestamp
    delivery_date = models.DateField(null=True, blank=True)  # Expected delivery date
    address = models.TextField()  # Delivery Address
    number = models.CharField(max_length=11, default=None)  # Contact Number
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='S')  # Added size field
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, related_name='porder', null=True, blank=True)  # Optional Review

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Order Status

    def get_total_price(self):
        """Calculate total order price."""
        return self.quantity * self.price

    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username} ({self.product.name})"
