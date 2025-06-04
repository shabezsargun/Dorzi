from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product  # Assuming product app is named 'product'

# Create your models here.
User = get_user_model()
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField(blank=True, null=True)  
    number = models.CharField(max_length=20, blank=True, null=True) 
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ] 
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='S')  # Added size field

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price
