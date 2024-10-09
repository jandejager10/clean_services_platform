from django.db import models

from products.models import Product  # Import the Product model

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)  # Link cart to user
    items = models.ManyToManyField(Product, through='CartItem')  # Many-to-Many relationship with products
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of cart creation

    def __str__(self):
        return f"Cart for {self.user.username}"  # Example cart string

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
