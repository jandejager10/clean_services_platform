from django.db import models
from django.conf import settings

from products.models import Product  # Import the Product model


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)  # Link cart to user
    items = models.ManyToManyField(Product, through='CartItem')  # Many-to-Many relationship with products
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of cart creation

    def __str__(self):
        return f"Cart for {self.user.username}"  # Example cart string

    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

    def get_vat(self):
        return self.get_subtotal() * settings.VAT_RATE

    def get_total_with_vat(self):
        return self.get_subtotal() + self.get_vat()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
