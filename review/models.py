from django.db import models
from tailor.models import *
from product.models import *
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')  # Reviewer (Buyer)
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='tailor_reviews')  # Tailor being reviewed
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')  # Product being reviewed
    rating = models.IntegerField()  # Rating out of 5
    comment = models.CharField(max_length=1024,default=None)  # Increased max length for detailed reviews
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto add review date

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate reviews by same user on same product

    def save(self, *args, **kwargs):
        # Ensure rating is between 1-5
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name} - {self.rating}/5"
