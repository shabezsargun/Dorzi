from django.db import models
from tailor.models import Tailor
from django.contrib.auth.models import User

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    availability = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=100, blank=True, null=True)
    orders = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# Product Image Model (Fixed)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")  # Fixed related_name
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"Image for {self.product.name}"

# User Activity Model
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=[('view', 'View'), ('click', 'Click'), ('order', 'Order')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} {self.product.name if self.product else 'Deleted Product'}"
